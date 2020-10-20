"""social_media URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static 
from .views import home
from accounts.views import login_view,register_view,logout_view
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home-view'),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    path('posts/', include('posts.urls', namespace='posts')),
    path('accounts/login/', login_view, name='login_view'),
    path('accounts/signup/', register_view, name='signup_view'),
    path('accounts/logout/', logout_view, name='logout_view'),
    path('accounts/password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html', html_email_template_name='registration/password_reset_email.html'), name='password_reset'),
    path('accounts/password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('accounts/password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('accounts/password-change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
    path('accounts/password-change-done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)