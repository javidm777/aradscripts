from django.urls import path
from . import views
from .views import create_content_website

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('websites/', views.user_panel, name='user_panel'),
    path('add_website/', views.add_website, name='add_website'),
    path('add_phrase/', views.add_phrase, name='add_phrase'),
    path('delete_website/<int:website_id>/', views.delete_website,
         name='delete_website'),
    path('fetch_content2/', views.fetch_content2, name='fetch_content2'),
    path('process/', views.process, name='process'),
    path('update/', views.run_update_script_view, name='run_update_script_view'),
    path('remove/', views.remove_links2, name='remove_link'),
    path('create-content/', create_content_website,
         name='create_content_website'),
    path('process_dot/', views.process_dots_text,
         name='process_dots_text'),
    path('update/', views.update_wordpress, name='update_wordpress'),
    path('get_content/', views.temp1, name='get_content'),
    path('login/', views.custom_login, name='custom_login'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('temp1/', views.temp1, name='temp1'),
    path('update_profile/<int:user_id>', views.update_profile,
         name='update_profile'),
    path('update_website/<int:website_id>', views.update_website,
         name='update_website'),
    path('website_panel/<int:website_id>', views.website_panel,
         name='website_panel')

]
