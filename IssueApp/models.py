from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.utils import timezone
from django.core.mail import send_mail
from django.urls import reverse
import uuid
import datetime

from django.conf import settings
from django.utils.crypto import get_random_string
from invitations.models import Invitation as BaseInvitation
# import datetime

# from django.utils.translation import gettext as _

class NameField(models.CharField):
    def get_prep_value(self, value):
        return str(value).lower()

class Project(models.Model):
    project_name = models.CharField(max_length=150,unique=True)
    description = models.TextField(blank=True)
    contributors = models.ManyToManyField(User ,related_name="contributors")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_projects")
    project_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.project_name    

class TeamInvitation(BaseInvitation):
    team = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='invitations')
    used = models.BooleanField(default=False)
    username = models.CharField(max_length=150, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    
    # def key_expired(self):
    #     expiration_date = self.sent + datetime.timedelta(
    #         days=settings.INVITATION_EXPIRY,
    #     )
    #     return expiration_date <= timezone.now()
    def key_expired(self):
        print(f"Sent field value: {self.sent}")  # Debug print
        if self.sent is None:
            # Handle None case
            return True
        expiration_date = self.sent + datetime.timedelta(days=1)
        return expiration_date < timezone.now()
    
    def send_invitation(self, request):
        invite_url = request.build_absolute_uri(reverse('accept_invitation', kwargs={'key': self.key}))
        if self.username and self.password:
            message = (
                f'You have been invited to join the project {self.team.project_name}. '
                f'Use the following credentials to sign up:\nUsername: {self.username}\nPassword: {self.password}\n'
                f'Click the link to accept the invitation: {invite_url}\n'
            )
        else:
            message = (
                f'You have been invited to join the project {self.team.project_name}. '
                f'Click the link to accept the invitation and log in with your existing credentials: {invite_url}\n'
            )
        
        send_mail(
            'You are invited to join a project',
            message,
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return f"Invite to {self.team.project_name} for {self.email}"
           

class CreateIssue(models.Model):
    status_choice = (('New', 'New'),
              ('In Progress', 'In Progress'),
              ('Fixed', 'Fixed'),
              ('Closed', 'Closed'),
              ('Reopened', 'Reopened'))

    priority_choice = (('Low', 'Low'),
               ('Medium', 'Medium'),
               ('High', 'High'),
              )
    project_name = models.CharField(max_length=150)
    issue_name = models.CharField(max_length=150)
    issue_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    issue_description = models.TextField(blank=False)
    issue_image = models.ImageField(upload_to="screenshorts",default="default-bug.png")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_issues")
    assigned_to = models.ManyToManyField(User)
    issue_status = models.CharField(choices = status_choice, max_length=150, default='New')
    issue_severity = models.CharField(choices = priority_choice, max_length=150, default='High')
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    fields =('project_name', 'issue_name','issue_image','issue_description','created_by',
                'assigned_to','issue_status','issue_severity')

    def __str__(self):
        return self.issue_name


    


    

    


