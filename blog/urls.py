from django.urls import path, include
from django.conf.urls import url
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views
import notifications.urls

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/new/', views.post_new, name='post_new'),
    path('signup/', views.signup, name='signup'),
    path('approve/', views.post_approve, name='post_approve'),
    path('messagechat', views.messagechat, name='messagechat'),
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    #path('chat/', views.chat, name='chat'),

    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
]
