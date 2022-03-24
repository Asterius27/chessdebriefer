"""ChessDebriefer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.debug),
    path('upload', views.upload),
    path('upload/openings', views.upload_openings),
    path('<slug:name>/percentages', views.percentages),
    path('<slug:name>/percentages/compare', views.compare_percentages),
    path('<slug:name>/percentages/events', views.event_percentages),
    path('<slug:name>/percentages/events/compare', views.compare_events),
    path('<slug:name>/percentages/openings', views.opening_percentages),
    path('<slug:name>/percentages/openings/compare', views.compare_openings),
    path('<slug:name>/percentages/terminations', views.termination_percentages),
    path('<slug:name>/percentages/terminations/compare', views.compare_terminations),
    path('<slug:name>/accuracy', views.accuracy),
    path('<slug:eco>/stats', views.opening_stats),
]
