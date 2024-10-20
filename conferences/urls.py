from django.urls import path 
from .views import *

urlpatterns = [
    path('list/', conferenceList,name="listconf"),
    path('listViewConference/', ConferenceListView.as_view(),name="ConferenceListView"),
    path('details/<int:pk>/', DetailViewConference.as_view(),name='conference_detail')
]