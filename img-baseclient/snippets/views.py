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