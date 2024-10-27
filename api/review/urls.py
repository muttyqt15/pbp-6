from django.urls import path
from .views import all_review, main_review, create_review, delete_review_ajax, edit_review_ajax, like_review_ajax, show_json, show_json_by_id

app_name = 'review'

urlpatterns = [
    path('', all_review, name='all_review'), 
    path('main/', main_review, name='main_review'), 
    path('create/', create_review, name='create_review'),
    path('edit/ajax/<uuid:id>/', edit_review_ajax, name='edit_review_ajax'), 
    path('delete/ajax/<uuid:id>/', delete_review_ajax, name='delete_review_ajax'),
    path('like/<uuid:id>/', like_review_ajax, name='like_review_ajax'),
    path('json/', show_json, name='show_json'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
]