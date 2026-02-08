from django.urls import path
from . import views
urlpatterns = [
    path('story-list/', views.StoryListView.as_view(), name='story-list'),
    path('story-details/<int:pk>/', views.StoryDetails.as_view(), name='story-details'),
    path('<int:pk>/sentence/', views.AddSentence.as_view(), name='AddSentence')
]
