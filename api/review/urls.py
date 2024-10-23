from django.urls import path
from .views import create_review, detail

app_name = 'review'

urlpatterns = [
    path('', create_review, name='create_review'),  
    path('<uuid:id>/', detail, name='review_detail'),
]