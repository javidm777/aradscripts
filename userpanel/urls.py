from django.urls import path
from . import views
from .views import create_content_website

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('websites/', views.user_panel, name='user_panel'),
    path('add_website/', views.add_website, name='add_website'),
    path('add_phrase/', views.add_phrase, name='add_phrase'),
    path('delete_website/<int:website_id>/', views.delete_website,
         name='delete_website'),
    path('fetch_content/', views.fetch_content, name='fetch_content'),
    path('process/', views.process, name='process'),
    path('update/', views.run_update_script_view, name='run_update_script_view'),
    path('remove/', views.remove_link, name='remove_link'),
    path('create-content/', create_content_website,
         name='create_content_website'),
    path('process_dot/', views.process_dots_text,
         name='process_dots_text'),

]
