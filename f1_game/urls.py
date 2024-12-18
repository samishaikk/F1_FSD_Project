from django.urls import path
from . import views
from .views import landing_page_view

urlpatterns = [
    path('', landing_page_view, name='landing_page'),
    path('team-selection/', views.team_selection_view, name='team_selection'),
    path('race-setup/', views.race_setup_view, name='race_setup'),
    path('start-race/', views.start_race_view, name='start_race'),
    path('race-strategy/', views.race_strategy_view, name='race_strategy'),
    path('race-finish/', views.race_finish_view, name='race_finish'),
    path('build-team/', views.build_team_view, name='build_team'),
    path('race-strategy-info/', views.race_strategy_view, name='race_strategy_info'),
    path('team-management/', views.team_management_view, name='team_management'),
    path('tracks-races/', views.tracks_races_view, name='tracks_races'),
    path('f1-rules/', views.f1_rules_view, name='f1_rules'),
    path('teams-drivers/', views.teams_drivers_view, name='teams_drivers'),
    path('pit-stops-strategies/', views.pit_stops_strategies_view, name='pit_stops_strategies'),
    path('points-championships/', views.points_championships_view, name='points_championships'),
    path('physics-car/', views.physics_car_view, name='physics_car'),
]
