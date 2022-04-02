from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
                  path('', views.signin, name='signin'),
                  path('register/', views.signup, name='register'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
