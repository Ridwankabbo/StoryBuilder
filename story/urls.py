from django.urls import path
from . import views
urlpatterns = [
    path('story-list/', views.StoryListView.as_view(), name='story-list'),
    path('story-details/', views.StoryDetails.as_view(), name='story-details'),
    path('sentence/', views.SentenceView.as_view(), name='Sentence'),
    path('story-contributors/', views.ContirbuterRequestView.as_view(), name='story-contributiors')
]
