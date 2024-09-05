from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('register',views.register,name='register'),
    # path('register_company',views.register_company,name='register_company'),
    path('profile/<str:pk>',views.profile,name='profile'),
    path('send_team_invite/<str:pk>',views.send_team_invite, name='send_team_invite'),
    path('invitations/accept-invite/<str:key>', views.accept_invitation, name='accept_invitation'),
    path('projects',views.projects,name='projects'),
    path('create_project',views.create_project,name='create_project'),
    path('updateProject/<str:pk>',views.updateProject,name='updateProject'),
    path('userIssues',views.userIssues,name='userIssues'),
    path('updateIssues/<str:pk>',views.updateIssues,name='updateIssues'),
    path('deleteProject/<str:pk>',views.deleteProject,name='deleteProject'),
    path('deleteIssues/<str:pk>',views.deleteIssues,name='deleteIssues'),
    path('issuesDescription/<str:pk>',views.issuesDescription,name='issuesDescription'),
    path('project/<str:pk>',views.issue_page,name='issues'),
    path('create_issues/<str:pk>',views.create_issues,name='create_issues'),
    path('login',views.sign_in,name='login'),
    path('logout',views.sign_out,name='logout'),
    path('activate/<str:uidb64>/<str:token>',views.activate,name='activate'),
    path('passwordreset',views.password_reset,name='passwordreset'),
    path('reset/<str:uidb64>/<str:token>',views.reset,name='reset'),
    path('',views.landing_page,name='landing'),

]+ static(settings.MEDIA_URL,
document_root=settings.MEDIA_ROOT)