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
from django.urls import path
from . import views

urlpatterns = [
    path('', views.debug),
    path('upload', views.upload),
    path('upload/openings', views.upload_openings),
    path('<slug:name>/percentages', views.percentages),
    path('<slug:name>/percentages/compare', views.compare_percentages),
    path('<slug:name>/percentages/events', views.event_percentages),
    path('<slug:name>/percentages/events/compare', views.compare_events),
    path('<slug:name>/percentages/openings', views.opening_percentages),
    path('<slug:name>/percentages/openings/compare', views.compare_openings),
    path('<slug:name>/percentages/openings/best-worst', views.openings_best_worst),
    path('<slug:name>/percentages/terminations', views.termination_percentages),
    path('<slug:name>/percentages/terminations/compare', views.compare_terminations),
    path('<slug:name>/percentages/throws-comebacks', views.throw_comeback_percentages),
    path('<slug:name>/percentages/endgames', views.endgame_percentages),
    path('<slug:name>/percentages/endgames/compare', views.endgame_percentages_compare),
    path('<slug:name>/percentages/endgames/material', views.endgame_percentages_material),
    path('<slug:name>/percentages/endgames/material/compare', views.endgame_percentages_material_compare),
    path('<slug:name>/percentages/endgames/material/wdl', views.endgame_percentages_material_wdl),
    path('<slug:name>/percentages/endgames/material/wdl/compare', views.endgame_percentages_material_wdl_compare),
    path('<slug:name>/percentages/endgames/material/predicted', views.endgame_percentages_material_predicted_wdl),
    path('<slug:name>/percentages/endgames/material/predicted/compare',
         views.endgame_percentages_material_predicted_wdl_compare),
    path('<slug:name>/percentages/endgames/tablebase', views.endgame_percentages_tablebase),
    path('<slug:name>/percentages/endgames/tablebase/compare', views.endgame_percentages_tablebase_compare),
    path('<slug:name>/percentages/endgames/tablebase/predicted', views.endgame_percentages_tablebase_predicted_wdl),
    path('<slug:name>/percentages/endgames/tablebase/predicted/compare',
         views.endgame_percentages_tablebase_predicted_wdl_compare),
    path('<slug:name>/accuracy', views.accuracy),
    path('<slug:eco>/stats', views.opening_stats),
]
