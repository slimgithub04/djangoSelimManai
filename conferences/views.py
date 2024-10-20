from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import conference
from django.views.generic import ListView,DetailView

def conferenceList(request):
    liste=conference.objects.order_by('-start_date')
    return render(request,'conferences/conferenceList.html',{'conferenceList': liste})


class ConferenceListView(ListView):
    model=conference
    template_name='conferences/conference_list.html'
    context_object_name="conferences"
    def get_queryset(self):
        return conference.objects.order_by('-start_date')
    
    
class DetailViewConference(DetailView):
    model=conference
    template_name='conferences/conference_detail_view.html'
    context_object_name="conferences"

    