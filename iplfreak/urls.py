from iplfreak import views
from django.urls import path


urlpatterns = [
    path('seasons/<int:year>/', views.season_details, name='season_details'),
    path('seasons/<int:year>/<int:match_id>/', views.match_details, name='match_details'),
    path('seasons/<int:year>/points-table/', views.points_table, name='points_table'),
    path('login/', views.LoginController.as_view(), name='login'),
    path('signup/', views.SignupController.as_view(), name='signup'),
    path('logout/', views.logout_user, name='logout')
]
