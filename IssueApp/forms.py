from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CustomSelectMultiple(forms.ModelMultipleChoiceField):
      def label_from_instance(self, user):
         return '%s' % user

class IssueForm(forms.ModelForm): 
    class Meta:
        model = CreateIssue
        fields =('project_name','created_by','issue_name','issue_description','issue_image',
                'assigned_to','issue_status','issue_severity', )
        exclude = ("project_name" , "created_by" , )
        widgets = {
          'issue_description': forms.Textarea(attrs={'rows':6, 'cols':25}),
        }
    assigned_to = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required = False
    )
    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super(IssueForm, self).__init__(*args, **kwargs)
        if project:
            contributors = project.contributors.all()
            if contributors.exists():
                self.fields['assigned_to'].queryset = contributors
            else:
                self.fields['assigned_to'].widget = forms.HiddenInput()
                self.fields['assigned_to'].help_text = "This project has no members yet. You can assign the issue later when members are added."    

class ProjectForm(forms.ModelForm):
    
    class Meta:
        model = Project
        fields = ('project_name',)

   
class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'profile_image', 'occupation')
        widgets = {
            'profile_image': forms.ClearableFileInput(attrs={'multiple': True}),
        }

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'profile_image', 'occupation')