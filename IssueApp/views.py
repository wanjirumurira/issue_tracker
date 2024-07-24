from django.http import HttpResponse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import csrf_exempt
#from . models import CustomUser as User
from . models import *
from .forms import *
from . tokens import generate_token
from issuetracker import settings


# Create your views here.
#@login_required(login_url='/login')
def projects(request):
    project = Project.objects.all()
    users = User.objects.all()
    context = {'project':project, 'users':users}
    return render(request, 'index.html', context)
    
#@login_required(login_url='/login')   
def create_project(request):
    created_by = request.user.username
    #data = {'created_by' : created_by}
    project = Project(created_by=created_by)
    if request.method == 'POST':
        project_form = ProjectForm(request.POST, instance=project)
        if project_form.is_valid():
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
                print("the user is :", user)
                print(user.check_password(password))
                #user.save()
             
                subject = "Welcome to Issue Tracker Login!!!"
                message = "Hello {username}! \n \
                Welcome to our Issue Tracker Website.\
                You have successfully registered with Issue Trackerl.We have sent you a confirmation email. \
                Pleaseconfirm your email address in order to activate your account."
                from_email = settings.EMAIL_HOST_USER
                to_user = user_email
                send_mail(subject, message, from_email, [to_user], fail_silently = True,)
                
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
            return redirect('/')
        else:
            messages.error(request, "Passwords don't match")
            return redirect ('/')
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
        print("please work : ", user)
        print(password)
        print(user)
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
       user = User.objects.get(email=user_email)
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
            password = request.POST('password')
            password2 = request.POST('password')
            if password != password2:
                messages.success(request,'Passwords do not match !')
                return render(request, 'passwordreset.html')
            else:
                user_new_password = User.objects.create(password=password)
                user.is_active = True
                user_new_password.save()
                messages.success(request, 'Password reset successfully.')
                return redirect ('/login')


   
       

