from django.urls import path
from . import views
urlpatterns = [
    path('story-list/', views.StoryListView.as_view(), name='story-list'),
    path('story-details/', views.StoryDetails.as_view(), name='story-details'),
    path('sentence/', views.SentenceView.as_view(), name='Sentence'),
    path('story-contributors/', views.ContributionRequestView.as_view(), name='story-contributiors'),
    path('sotries/requests/respond/', views.ContributionRequestView.as_view(), name='respond-request')
]
