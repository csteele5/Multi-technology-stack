from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages

from .models import Sprint, ProjectTeam, Engineer, SprintPairing

@login_required
def sprint_list_view(request):
    # list out objects 
    # could be search
    weeks_to_build = 0
    team_next_sprint_start_date = ''
    build_results = ''
    selected_team_name = ''
    if request.POST.get('weeks_to_build'):
        try:
            weeks_to_build = int(request.POST.get('weeks_to_build'))
        except ValueError:
            # scope is all
            weeks_to_build = 0 # redundant, but need something in the except   
    
    team_filter = 0
    if request.POST.get('project_team'):
        try:
            team_filter = int(request.POST.get('project_team'))
        except ValueError:
            # scope is all
            team_filter = 0 # redundant, but need something in the except    

    if team_filter > 0:
        # get team_next_sprint_start_date from team
        project_team = get_object_or_404(ProjectTeam, id=team_filter)
        team_next_sprint_start_date = project_team.next_start_date
        selected_team_name = project_team
        
        if weeks_to_build > 0:
            # initiate build

            if weeks_to_build == 1:
                duration_text = "1 week"
            else:
                duration_text = str(weeks_to_build) + ' weeks'
            #duration_text += ' PRE Start at :'+ str(team_next_sprint_start_date)
            build_results = project_team.schedule_future_sprints(weeks_to_build)
            # duration_text = build_results
            #duration_text += ' POST '

            messages.add_message(request, messages.SUCCESS, 'The project sprints have been scheduled and assigned for ' + duration_text + '.')
            
            # refresh sprint date
            project_team = get_object_or_404(ProjectTeam, id=team_filter)
            team_next_sprint_start_date = project_team.next_start_date



        qs = Sprint.objects.filter(project_team=team_filter)
        
        #featured_filter = request.GET.get('featured')
        #query = Unit.listType.filter(unitType=featured_filter)
    else:
        qs = Sprint.objects.all()  #[:10] 

    # this must be streamined.  Too many objects to loop through
    pairing_list = SprintPairing.objects.all()

    teams = ProjectTeam.objects.all()
    template_name = 'schedule/list.html'
    context = {
                'object_list': qs,
                'projectteam_list': teams,
                'team_filter': team_filter,
                'team_next_sprint_start_date': team_next_sprint_start_date,
                'selected_team_name': selected_team_name,
                'build_results': build_results,
                'pairing_list': pairing_list
              }
    return render(request, template_name, context) 

@login_required
def sprint_detail_view(request, id):
    obj = get_object_or_404(Sprint, id=id)
    context = {
        'object': obj
        }
    #context['project'] = ProjectTeam.objects.filter(id=obj.project_team.id)
    context['team_list'] = Engineer.objects.filter(project_team=obj.project_team, available_for_sprint=True)
    context['pairing_list'] = SprintPairing.objects.filter(sprint=obj.id)
    return render(request, "schedule/sprint_detail.html", context)

@login_required
def pair_build_view(request, id):
    obj = get_object_or_404(Sprint, id=id)
    obj.refresh_all_pairing_options()
    obj.create_pairing_assignments()

    messages.add_message(request, messages.SUCCESS, 'Pair coding assignments have been created for this sprint.')

    return redirect(reverse('schedule:sprint-detail', kwargs={'id':id}))
    

@login_required
def pair_update_view(request, id):
    obj = get_object_or_404(SprintPairing, id=id)
    if request.method == 'POST':
        try:
            assigned_points = int(request.POST.get('inputAssignedPoints'))
        except:
            assigned_points = 0
        try:
            completed_points = int(request.POST.get('inputCompletedPoints'))
        except:
            completed_points = 0

    obj.assigned_points = assigned_points
    obj.completed_points = completed_points  
    obj.save()

    obj.sprint.update_story_statistics()


    messages.add_message(request, messages.SUCCESS, 'Pair statistics have been updated for this sprint.')

    return redirect(reverse('schedule:sprint-detail', kwargs={'id':obj.sprint.id}))

# @login_required
# def sprint_automate_view(request, id):
#     obj = get_object_or_404(ProjectTeam, id=id)
#     if request.method == 'POST':
#         try:
#             sprints_to_schedule = request.POST.get('inputNewSprintCount')
#         except:
#             sprints_to_schedule = 0

#     obj.schedule_future_sprints(sprints_to_schedule)


#     messages.add_message(request, messages.SUCCESS, 'The project sprints have been scheduled and assigned.')

#     return redirect(reverse('schedule:sprint-list', kwargs={'project_team':id}))