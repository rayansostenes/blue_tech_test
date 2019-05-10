from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='API')

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', schema_view),
    path('auth/login/', auth_views.LoginView.as_view(template_name='auth/login.html')),
    path('auth/logout/', auth_views.LogoutView.as_view()),
    path('api/auth/', include('apps.auth.urls')),
    path('api/polls/', include('apps.polls.urls')),
]

if settings.DEBUG and 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls))
    ] + urlpatterns
