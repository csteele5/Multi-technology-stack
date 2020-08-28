from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages

from .models import Snippet

@login_required
def snippet_list_view(request):

    qs = Snippet.objects.all()[:10] 

    
    template_name = 'snippets/list.html'
    context = {
                'object_list': qs,
                # 'language_list': languages,
                # 'language_filter': language_filter,
              }
    return render(request, template_name, context) 

@login_required
def snippet_detail_view(request, id):
    obj = get_object_or_404(Snippet, id=id)
    context = {
        'object': obj
        }
    #context['project'] = ProjectTeam.objects.filter(id=obj.project_team.id)
    #context['team_list'] = Engineer.objects.filter(project_team=obj.project_team, available_for_sprint=True)
    #context['pairing_list'] = SprintPairing.objects.filter(sprint=obj.id)
    return render(request, "snippets/snippet_detail.html", context)
