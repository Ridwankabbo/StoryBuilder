from django.urls import path
from . import views
urlpatterns = [
    path('story-list/', views.StoryListView.as_view(), name='story-list'),
    path('story-details/<int:pk>/', views.StoryDetails.as_view(), name='story-details'),
<<<<<<< HEAD
=======
    path('sentence/', views.SentenceView.as_view(), name='Sentence')
>>>>>>> development
]
