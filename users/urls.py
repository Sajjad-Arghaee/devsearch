from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name = 'login'),
    path('register/', views.registerUser, name = 'register'),
    path('logout/', views.logoutUser, name = 'logout'),
    path('account/', views.account, name='account'),
    path('inbox/', views.inbox, name='inbox'),
    path('message/<str:pk>/', views.view_message, name='message'),
    path('send-message/<str:pk>/', views.send_message, name='send-message'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('delete-skill/<str:pk>', views.deleteSkill, name='delete-skill'),
    path('edit-skill/<str:pk>', views.editSkill, name='edit-skill'),
    path('add-skill', views.addSkill, name='add-skill'),
    path('<str:name>/', views.profile, name='profile'),
    path('', views.index, name='index'),
]
