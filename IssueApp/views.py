from django.http import HttpResponse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
import string
import random
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import csrf_exempt
#from . models import CustomUser as User
from . models import *
from .forms import *
from . tokens import generate_token
from issuetracker import settings


# Create your views here.
@login_required(login_url='/login')
def projects(request):
    user = request.user
    contributed_projects = Project.objects.filter(contributors=user)
    created_projects = Project.objects.filter(created_by=user)
    all_projects = contributed_projects | created_projects
    #users = User.objects.all()
    context = {'project':all_projects, 'user':user}
    return render(request, 'index.html', context)

@login_required(login_url='/login')
def send_team_invite(request, pk):
    project = Project.objects.get(project_id=pk)

    if request.method == 'POST':
        email = request.POST.get('email')
        user_exists = User.objects.filter(email=email).exists()


        # Check if an invitation has already been sent
        existing_invitation = TeamInvitation.objects.filter(
            email=email, 
            team=project,
            used=False).first()
        print(project.contributors.filter(email=email))
        if project.contributors.filter(email=email).exists():
            messages.error(request, "This user is already part of the project")
            return redirect(request.path)
    
        if existing_invitation:
            messages.error(request, "An invitation has already been sent to this email address for this project.")
            return redirect(request.path)
        
        if user_exists:
            # For existing users, no need to generate credentials
            username = None
            password = None
        else:
            # Generate a random username and password for new users
            username = get_random_string(length=8, allowed_chars=string.ascii_lowercase)
            password = get_random_string(length=12, allowed_chars=string.ascii_letters + string.digits + string.punctuation)
            
            # Create the user with the generated username and password
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_active = False
            user.save()
        
        
        # Create the invitation
        invitation = TeamInvitation.create(
            email=email,
            team=project,
            inviter=request.user,
            username=username,
            password=password
        )
        
        
        # Send the invitation email
        invitation.send_invitation(request)
        
        messages.success(request, "Invitation sent successfully!")
    
    context = {'project': project}
    return render(request, 'send_team_invite.html', context)
    
@csrf_exempt
def accept_invitation(request, key):
    invitation = TeamInvitation.objects.get(key=key)
    
    try:
        invitation = TeamInvitation.objects.get(key=key)
    except TeamInvitation.DoesNotExist:
        return HttpResponse("Invalid invitation key.")

    if invitation.accepted :
        #print(f"Invitation details: {user}")
        return HttpResponse("This invitation has already been used.")

    if invitation.key_expired():
        return HttpResponse("This invitation has already expired.")

    try:
        user = User.objects.get(email=invitation.email)
    #     #print(f"Invitation details: {user}")
    except User.DoesNotExist:
    #     #print(f"Invitation details: {invitation.email}")
        return HttpResponse("User matching invitation not found.")

    if invitation.username and invitation.password:
        user.is_active = False
        if request.method == 'POST':
            password = request.POST['password']
            password2 = request.POST['password2']
            if password != password2:
                messages.success(request,'Passwords do not match !')
                return render(request, 'passwordreset.html')
            else:
                user.set_password(password)
                user.is_active = True
                user.save()
                invitation.accepted = True
                invitation.save()
            messages.success(request, "Your password has been successfully changed. You can now log in.")
            return redirect('/login')
        
    
        #return render(request, 'passwordreset.html')
    else:
        existing_user = User.objects.filter(email=invitation.email).exists()
        if existing_user:
            invitation.accepted = True
            invitation.save()
            # messages.success(request, "Invitation accepted successfully with existing credentials!")
            return redirect('/login')
    return render(request, 'passwordreset.html')
    
  
@login_required(login_url='/login')   
def create_project(request):
    created_by = request.user
    project = Project(created_by=created_by)
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        if project_form.is_valid():
            # Handle contributors
            project = project_form.save(commit=False)
            project.created_by = request.user
            project.save() 
            emails = request.POST.get('contributors_emails', '')
            emails = [email.strip() for email in emails.split(',') if email.strip()]
            users = User.objects.filter(email__in=emails)
            non_existing_emails = set(emails) - set(user.email for user in users)

            if non_existing_emails:
                messages.error(request, f"The following email addresses do not correspond to any users: {', '.join(non_existing_emails)}")
                return redirect(request.path)
            else:
                project.contributors.add(*users)
                project_form.save()
                messages.success(request, "Project successfully created")
                return redirect('projects')
    else:
        project_form = ProjectForm(instance=project)
    context = {
                'create_project' : project_form
                }
    return render(request, "createProjects.html", context)
    
@login_required(login_url='/login')   
def updateProject(request, pk):
    model = Project() 
    project_contributors = User.objects.all()
    project = Project.objects.get(project_id = pk)
    project_update = ProjectForm(instance = project)
    if request.method == 'POST':
        project_update = ProjectForm(request.POST, instance=project)
        if project_update.is_valid():
            project_update.save()
            messages.success(request, "Project successfully updated")
            return redirect('projects')
    context = {"project" : project,
                'project_contributors' : project_contributors,
                'model':model,
                'project_update' : project_update,
                }
    return render(request, "projectupdate.html", context)

@login_required(login_url='/login')
def deleteProject(request,pk):
    project = Project.objects.get(project_id = pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {'project': project}
    return render(request,'deleteproject.html', context)

@login_required(login_url='/login')
def issue_page(request, pk):
    project_name = Project.objects.get(project_name = pk)
    issues = CreateIssue.objects.filter(project_name = project_name)
    
    context = {
                'issues' : issues ,
                'project' : project_name,
    
    }
    return render(request, "issues.html", context)

@login_required(login_url='/login')
def userIssues(request):
    user = User.objects.filter(username = request.user.username)
    issues = CreateIssue.objects.filter(assigned_to__in = user)  
    print(issues)
    context = {
                'issues' : issues ,
    
    }
    return render(request, "userIssues.html", context)

@login_required(login_url='/login')
def create_issues(request, pk):
    created_by = request.user.username
    project_name = Project.objects.get(project_name = pk)
    issue = CreateIssue(project_name = project_name, created_by = created_by)
    if request.method == 'POST':
        issue_form = IssueForm(request.POST, request.FILES, instance=issue)
        if issue_form.is_valid():
            issue_form.save()
            messages.success(request, "Issue successfully created")
            return redirect('issues',pk = project_name)
    else:
        issue_form = IssueForm(instance=issue)
    context = {
                'create_issue' : issue_form,
                'project_name' : project_name
                }
    
    return render(request, "createIssue.html", context)


@login_required(login_url='/login')  
def updateIssues(request,pk):
    model = CreateIssue()
    project_contributors = User.objects.all()
    issue = CreateIssue.objects.get(issue_id = pk)
    issue_update = IssueForm(instance=issue)
    if request.method == 'POST':
        issue_update = IssueForm(request.POST, instance=issue)
        if issue_update.is_valid():
            issue_update.save()
            messages.info(request, "Issue successfully updated")
            return redirect('issues',pk=issue.project_name)
          
    context = {"issue":issue,
                'project_contributors' : project_contributors,
                'model':model,
                'issue_update':issue_update,
                }
    return render(request,'issuesupdate.html', context)

@login_required(login_url='/login')
def issuesDescription(request,pk):
    issue = CreateIssue.objects.get(issue_id = pk)
    context = {'issue':issue}
    return render(request,'issueDescription.html', context)

@login_required(login_url='/login')
def deleteIssues(request,pk):
    issue = CreateIssue.objects.get(issue_id = pk)
    if request.method == 'POST':
        issue.delete()
        return redirect('issues', pk=issue.project_name)
    context = {'issue':issue}
    return render(request,'deleteissue.html', context)

@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        user_email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is Already Taken')
            elif User.objects.filter(email=user_email).exists():
                messages.error(request, 'Email is Already Taken')
            elif not username.isalnum():
                messages.error(request, 'Username must be alpha-Numeric!')
            elif len(username) > 15:
                messages.error(request, 'Username must be under 15 characters')
            else:
                user = User.objects.create_user(username=username, email=user_email, password=password)
                # user.set_password(password)
                user.is_active = False
                user.save()
                #Email Address Confirmation 
                current_site = get_current_site(request)
                email_subject = "Confirm your email - Issue Tracker"
                context = {
                    'name':username,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': generate_token.make_token(user)
                }
                message2 = render_to_string('email.html',context)
                email = EmailMessage(
                    email_subject,
                    message2,
                    settings.EMAIL_HOST_USER,
                    [user_email],
                )
                
                email.send()
                messages.success(request, "Your Account has beem successfully created. We have sent you a confirmation email \
                                 .Please confirm your email in order to activate your account.")
            return redirect('/register')
        else:
            messages.error(request, "Passwords don't match")
            return redirect ('/register')
    return render (request,'register.html')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        print(uid)
        my_user = User.objects.get(pk=uid)
        print(my_user)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        my_user = None

    if my_user is not None and  generate_token.check_token(my_user, token):
        my_user.is_active = True
        my_user.save()
        print("My user is while registering ", my_user)
        login(request, my_user)
        return redirect('/login')
    else:
        return render(request, 'activation_failed.html')

@csrf_exempt
def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('projects')
        else:
            messages.error(request, "Invalid Password or Username")
            return redirect('login')
    return render(request,'signin.html')
        
def sign_out(request):
    logout(request)
    return redirect('login')
    
def password_reset(request):
    if request.method == 'POST':
       user_email = request.POST['email']
       try:
           user = User.objects.get(email=user_email)
       except User.DoesNotExist:
            return HttpResponse('If this email address is known to us, an email will be sent to your account.')
       site = get_current_site(request)

       if user is not None:
        user.is_active = False
        # User needs to be inactive for the reset password duration
        user.save()
        email_subject = 'Password Reset - Issue Tracker'
        context = {
            'username' : user,
            'domain' : site.domain,
            'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
            'token' : generate_token.make_token(user)
        }
        message = render_to_string('passwordEmail.html',context)
        email = EmailMessage(email_subject,message, settings.EMAIL_HOST_USER,to=[user_email])
        email.send()
        return HttpResponse('If this mail address is known to us, an email will be sent to your account.')
    
    return render(request, 'passwordconfirmation.html')
         
def reset(request, uidb64, token):
    if request.method == 'POST':
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        if user is not None and generate_token.check_token(user, token):
            password = request.POST['password']
            password2 = request.POST['password']
            if password != password2:
                messages.success(request,'Passwords do not match !')
                return render(request, 'passwordreset.html')
            else:
                user.set_password(password)
                user.is_active = True
                user.save()
                messages.success(request, 'Password reset successfully.')
                return redirect ('/login')
    else:
        return render(request, 'passwordreset.html', {'uidb64': uidb64, 'token': token})
    
def landing_page(request):
    return render (request, 'landingPage.html')
   


