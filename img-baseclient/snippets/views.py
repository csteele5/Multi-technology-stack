from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages

from .models import Snippet

from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])

# temporary list until the database is updated
preferred_languages = ['python', 'js', 'php', 'postgresql', 'sql', 'html']

@login_required
def snippet_list_view(request):

    language_filter = None
    filter_all_languages = 0
    if request.method == 'POST':
        language_filter = request.POST.get('filter_language')
        if request.POST.get('filter_all_languages'):
            filter_all_languages = 1

    filter_search = None
    if request.method == 'POST':
        filter_search = request.POST.get('filter_search')


    language_list = {}
    for language in LANGUAGE_CHOICES:
        (key, value) = language
        if filter_all_languages == 1:
            language_list[key] = value
        elif key in preferred_languages:
            language_list[key] = value

    if language_filter is not None and language_filter != '':
        if filter_search is not None and filter_search != '':
            qs = Snippet.objects.filter(title__icontains=filter_search, language=language_filter) | Snippet.objects.filter(code__icontains=filter_search, language=language_filter) 
        else:
            qs = Snippet.objects.filter(language = language_filter) 
    else:
        if filter_search is not None and filter_search != '':
            qs = Snippet.objects.filter(title__icontains=filter_search) | Snippet.objects.filter(code__icontains=filter_search)
        else:
            qs = Snippet.objects.all()[:20] 
    
    if filter_search is None:
        filter_search = ''

    template_name = 'snippets/list.html'
    context = {
                'object_list': qs,
                'language_list': language_list,
                'language_filter': language_filter,
                'filter_all_languages': filter_all_languages,
                'filter_search': filter_search,
              }
    return render(request, template_name, context) 

@login_required
def snippet_detail_view(request, id):
    obj = get_object_or_404(Snippet, id=id)
    language_list = {}
    for language in LANGUAGE_CHOICES:
        (key, value) = language
        language_list[key] = value
    
    style_list = {}
    for style in STYLE_CHOICES:
        (key, value) = style
        style_list[key] = value    


    context = {
        'object': obj,
        'language_list': language_list,
        'style_list': style_list
        }
    #context['language'] = ProjectTeam.objects.filter(id=obj.language.id)
    #context['team_list'] = Engineer.objects.filter(project_team=obj.project_team, available_for_sprint=True)
    #context['pairing_list'] = SprintPairing.objects.filter(sprint=obj.id)
    return render(request, "snippets/snippet_detail.html", context)

@login_required
def snippet_update_view(request, id):
    obj = get_object_or_404(Snippet, id=id)
    if request.method == 'POST':
        title = request.POST.get('inputTitle')
        code = request.POST.get('inputCode')
        language = request.POST.get('inputLanguage')
        style = request.POST.get('inputStyle')
        linenos = 0
        if request.POST.get('inputLinenos'):
            linenos = 1

        # inputLinenos
        obj.title = title
        obj.code = code 
        obj.language = language 
        obj.style = style  
        obj.linenos = linenos
        obj.save()

        messages.add_message(request, messages.SUCCESS, 'The code snippet has been updated.')
    else:
       messages.add_message(request, messages.WARNING, 'The code snippet was not updated.') 

    return redirect(reverse('snippets:snippet-detail', kwargs={'id':obj.id}))    


@login_required
def snippet_create_view(request):

    newlanguage = 'python'
    newstyle = 'friendly'
    
    if request.method == 'POST':
        newlanguage = request.POST.get('newlanguage')
        newstyle = request.POST.get('newstyle')

    language_list = {}
    for language in LANGUAGE_CHOICES:
        (key, value) = language
        language_list[key] = value
    
    style_list = {}
    for style in STYLE_CHOICES:
        (key, value) = style
        style_list[key] = value    

    context = {
        'newlanguage': newlanguage,
        'newstyle': newstyle,
        'language_list': language_list,
        'style_list': style_list
        }

    return render(request, "snippets/snippet_create.html", context)


@login_required
def snippet_save_view(request):    
    if request.method == 'POST':
        title = request.POST.get('inputTitle')
        code = request.POST.get('inputCode')
        language = request.POST.get('inputLanguage')
        style = request.POST.get('inputStyle')
        #owner = request.POST.get('inputOwner')
        linenos = 0
        if request.POST.get('inputLinenos'):
            linenos = 1
     
        obj = Snippet(title=title, code=code, language=language, style=style, linenos=linenos, owner=request.user)

        obj.save()

        messages.add_message(request, messages.SUCCESS, 'The code snippet has been created.')
    else:
       messages.add_message(request, messages.WARNING, 'The code snippet was not created.') 

    return redirect(reverse('snippets:snippet-detail', kwargs={'id':obj.id}))    


@login_required
def snippet_delete_view(request, id):
    obj = get_object_or_404(Snippet, id=id)
    if request.method == "POST":
        obj.delete()
        messages.add_message(request, messages.SUCCESS, 'The code snippet has been deleted.')
    else:
        messages.add_message(request, messages.WARNING, 'The code snippet was not deleted.') 

    # return redirect("snippets/")
    return redirect(reverse('snippets:snippet-list', kwargs={}))  