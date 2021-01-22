"""animation_assistance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include,re_path
from align_tap.urls import router as align_tap_router
from django.views.static import serve
from django.conf import settings
from align_tap import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(align_tap_router.urls)),
    path('api/align/', views.align_image,name="align"),
    path('api/download/', views.DownloadList),
    # path('api/align2/',CreateProcessedImageView.as_view() ,name="create_align"),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    re_path('media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path('api/(?P<group>.+)/$', views.ImageList.as_view()),
]
