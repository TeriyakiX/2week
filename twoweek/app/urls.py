from django.urls import path, include
from django.views.generic import RedirectView
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('', include('django.contrib.auth.urls')),
    path('', RedirectView.as_view(url='login', permanent=True)),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('error/', views.get_error, name='error'),
    path('profile/applications', views.view_applications.as_view(), name='profile_applications'),
    path('profile/main_applications', views.profile_main_applications.as_view(), name='profile_main_applications'),
    path('profile/applications/create', views.create_application.as_view(), name='profile_applications_create'),
    path('profile/applications/<int:pk>/', views.detail_application.as_view(), name='profile_application_detail'),
    path('profile/applications/<int:pk>/delete', views.delete_application.as_view(), name='profile_application_delete'),
    path('profile/applications/<int:pk>/update', views.update_application.as_view(), name='profile_application_update')
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)