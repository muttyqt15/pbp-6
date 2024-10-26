from django.urls import path
from .views import all_review, main_review, create_review, delete_review, edit_review, show_json, show_json_by_id

app_name = 'review'

urlpatterns = [
    path('', all_review, name='all_review'), 
    path('main/', main_review, name='main_review'), 
    path('create/', create_review, name='create_review'), 
    path('edit/<uuid:id>/', edit_review, name='edit_review'), 
    path('delete/<uuid:id>/', delete_review, name='delete_review'),
    path('json/', show_json, name='show_json'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
]
