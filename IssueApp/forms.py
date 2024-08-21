from django import forms
from .models import *


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
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

   
    
        
# class ProjectForm(forms.ModelForm):
    
#     class Meta:
#         model = Project
#         fields = ('project_name', 'created_by', 'contributors')
#         exclude = ("created_by","contributors" )
        
#     contributors = forms.ModelMultipleChoiceField(
#         queryset=User.objects.all(),
#         widget=forms.CheckboxSelectMultiple
#     )
    

class ProjectForm(forms.ModelForm):
    contributors_emails = forms.CharField(
        max_length=255,
        help_text="Enter email addresses separated by commas",
        required=False
    )

    class Meta:
        model = Project
        fields = ['project_name', 'created_by']

   