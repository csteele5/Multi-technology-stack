from datetime import datetime, date, timedelta
from math import *
import itertools

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class ProjectTeam(models.Model):
    project_team = models.CharField(max_length=50)
    team_lead = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    go_live_date = models.DateField('go live date')

    def __str__(self):
        name = self.project_team 
        return name
    class Meta:
        verbose_name_plural = "Project Teams"

    @property
    def next_start_date(self):
        #get the week of the last sprint, or now, whichever is later, and calculate a start date of the following monday
        start_after_date = datetime.date(datetime.now())
        project_sprints = Sprint.objects.filter(project_team=self)

        for sprint in project_sprints:
            if sprint.sprint_start_date > start_after_date:
                start_after_date = sprint.sprint_start_date
        
        # new_start_date is the monday after the start_after_date
        onDay = lambda date, day: date + timedelta(days=(day-date.weekday()-1)%7+1)
        start_date = onDay(start_after_date, 0)

        return start_date

    def schedule_future_sprints(self, weeks):
        # create the number of sprints (week long)
        new_sprint_start = self.next_start_date
        for x in range(weeks):
            sprint_start_date = new_sprint_start + timedelta(days=(x)*7)
            sprint_end_date = sprint_start_date + timedelta(days=4)
            project_team = self
            # create sprint
            new_sprint = Sprint(project_team=project_team, sprint_start_date=sprint_start_date, sprint_end_date=sprint_end_date)
            new_sprint.save()
            # schedule the engineers for each week
            new_sprint.refresh_all_pairing_options()
            new_sprint.create_pairing_assignments()


        
        return {
                "weeks": weeks,
                "self": self,
                }

class Engineer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    available_for_sprint = models.BooleanField(default=True)    
    # temporary attributes - to be function based calculations
    # avg_team_points_assigned = models.IntegerField(default=0)
    # avg_team_points_completed = models.IntegerField(default=0)
    project_team = models.ForeignKey(ProjectTeam, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Project Team")
  
    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.full_name
    class Meta:
        ordering = ['last_name']

class Sprint(models.Model):
    sprint_start_date = models.DateField('start date')
    sprint_end_date = models.DateField('end date')
    #current_date = models.DateField(**options)
    # sprint_name = 'Sprint WE ' + sprint_end_date.strftime('%b %d, %Y')
    # temporary attributes - to be function based calculations
    # readonly_fields = ('address_report',)
    assigned_points = models.IntegerField(default=0)
    completed_points = models.IntegerField(default=0)
    project_team = models.ForeignKey(ProjectTeam, on_delete=models.PROTECT)

    def __str__(self):
        name = self.sprint_name()
        return name

    def sprint_name(self):
        name = self.project_team.project_team + ' | WE ' + self.sprint_end_date.strftime('%b %d, %Y')
        return name

    def sprint_duration(self):
        delta = (self.sprint_end_date - self.sprint_start_date).days + 1
        return str(delta)+' Days'
    
    def sprint_status(self):
        status = 'Active'
        current_date = date.today()
        if current_date < self.sprint_start_date:
            status = 'Future'
        elif current_date > self.sprint_end_date: 
            status = 'Complete'
        return status

    def completion_percentage(self):
        percent = 0
        if self.assigned_points > 0:
            percent = "{0:.0f}%".format(self.completed_points/self.assigned_points * 100)
        return percent

    class Meta:
        ordering = ['-sprint_end_date']
    
    def get_absolute_url(self):
        return reverse("schedule:sprint-detail", kwargs={"id":self.id}) 

    def update_story_statistics(self):
        assigned_points = 0
        completed_points = 0

        assigned_pairs = SprintPairing.objects.filter(sprint=self.id)

        for pair in assigned_pairs:
            assigned_points += pair.assigned_points
            completed_points += pair.completed_points

        self.assigned_points = assigned_points
        self.completed_points = completed_points
        self.save()    

    
    def delete_pairing_assignments(self):
        pass

    def create_pairing_assignments(self):
        tech_count = 0

        project_techs = Engineer.objects.filter(project_team=self.project_team.id, available_for_sprint=True)
        for tech in project_techs:
            tech_count +=1
        # get current pairs (update must run before this)
        # Order by ttl_assignments desc, employee2 desc (null first)
        updated_pairs = Pairing.objects.all().order_by('total_sprint_pairings','-pair_member2')  #order these

        # loop through team list (random sort) and assign to project until all techs are assigned
        assigned_tech_list = []
        
        while len(assigned_tech_list) < tech_count:
            # loop through the newly created pairs, which are sorted by lowest usage and 2 person pairs first
            for new_pair in updated_pairs:
                # Parse out Engineers or None
                engineer1 = new_pair.pair_member1
                try:
                    engineer2 = new_pair.pair_member2
                except:
                    engineer2 = None

                # new_sprint_pair = SprintPairing(sprint=self, member1=engineer1)
                # new_sprint_pair.save()
                # assigned_tech_list.append(engineer1)
                # assigned_tech_list.append(engineer2)
                # assigned_tech_list.append(engineer1)
                # assigned_tech_list.append(engineer2)
                # assigned_tech_list.append(engineer1)
                # assigned_tech_list.append(engineer2)    
                # break
                # check if this is a one person team
                #assigned_tech_list.append({"engineer1": engineer1, "engineer2": engineer2, "eng1teamresults": check_tech_on_project_team(project_techs, engineer1), "eng2teamresults": check_tech_on_project_team(project_techs, engineer2)})

                create_pair = False
                # if engineer2, this is a pair, so always look for pairs
                if engineer2:
                    # verify neither of these engineers are in the assigned_tech_list
                    if not check_tech_in_list(assigned_tech_list, engineer1) and not check_tech_in_list(assigned_tech_list, engineer2):
                        if check_tech_in_list(project_techs, engineer1) and check_tech_in_list(project_techs, engineer2):
                            # if engineer1 in project_techs and engineer2 in project_techs:
                            create_pair = True

                    if create_pair:
                        # create a sprint pair with two members and add to assigned_eng_list
                        new_sprint_pair = SprintPairing(sprint=self, member1=engineer1, member2=engineer2)
                        new_sprint_pair.save()
                        assigned_tech_list.append(engineer1)
                        assigned_tech_list.append(engineer2)
                        

                # only assign a single tech if there is only one left to assign, otherwise keep looking for pairs
                elif tech_count - len(assigned_tech_list) == 1:
                    # is engineer1 on the project team and NOT in the assigned_eng_list
                    if not check_tech_in_list(assigned_tech_list, engineer1):
                        #if engineer1 in project_techs:
                        if check_tech_in_list(project_techs, engineer1): 
                            create_pair = True
                    
                    if create_pair:
                        # create a pair with just one member and add to assigned_eng_list
                        new_sprint_pair = SprintPairing(sprint=self, member1=engineer1)
                        new_sprint_pair.save()
                        assigned_tech_list.append(engineer1)
                
                if create_pair:
                    break

        return {
                "tech_count": tech_count,
                "assigned_tech_count": len(assigned_tech_list),
                "assigned_tech_list": assigned_tech_list,
                "project_techs": project_techs,
                }


    def refresh_all_pairing_options(self):

        all_available_techs = Engineer.objects.filter(available_for_sprint=True)

        possible_pairs = get_combinations_of_len(all_available_techs, 2)

        #delete all pair history
        Pairing.objects.all().delete()

        # for each possible pair, create a database entry with:
        # total assignments
        # average assigned points
        # average completed points
        pair_results = []

        for pair in possible_pairs:
            assignment_metrics = get_pair_assignment_metrics(pair)
            ttl_assignments = assignment_metrics['ttl_assignments']
            ttl_assigned_pts = assignment_metrics['ttl_assigned_pts']
            ttl_completed_pts = assignment_metrics['ttl_completed_pts']
            avg_assigned_pts = 0
            avg_completed_pts = 0

            if ttl_assignments > 0:
                avg_assigned_pts = round(ttl_assigned_pts / float(ttl_assignments), 2)
                avg_completed_pts = round(ttl_completed_pts / float(ttl_assignments), 2)

            # Parse out Engineers or None
            engineer1 = pair[0]
            try:
                engineer2 = pair[1]
            except:
                engineer2 = None

            # Add new possible pair result with stats to database
            new_pairing = Pairing(pair_member1=engineer1, pair_member2=engineer2, total_sprint_pairings=ttl_assignments, avg_assigned_points=avg_assigned_pts, avg_completed_points =avg_completed_pts)
            new_pairing.save()

            # This is just for debugging  - The output goes to the debugging page ONLY when uncommented         
            pair_results.append([pair, ttl_assignments, avg_assigned_pts, avg_completed_pts])  

        return {
                "possible_pair_count": len(possible_pairs),
                "possible_pairs": possible_pairs,
                }


def check_tech_in_list(tech_list, test_tech):
    tech_in_list = False
    for tech in tech_list:
        if tech.id == test_tech.id:
            tech_in_list = True
            break
    return tech_in_list


# global function for getting pair combinations
def get_combinations_of_len(in_list, dimension):
    out_list = []
    for i in range(1, dimension+1):
        out_list.extend(itertools.combinations(in_list, i))
    return out_list

#global function for getting pair metrics
def get_pair_assignment_metrics(pair):
    ttl_assignments = 0
    ttl_assigned_pts = 0
    ttl_completed_pts = 0
    # look for all of the assignments for this pair and increment the ttl
    # possibles are coming in one at a time as "pair" - 
    # the source must have solo options for this to work!!@
    # actuals are pulled in for comparison and are "assignments"
    assignments = SprintPairing.objects.all()
    engineer1 = pair[0]
    try:
        engineer2 = pair[1]
    except:
        engineer2 = None

    test = []
    for assignment in assignments:
        #test.append({"nullcheck": "Checking"})  and assignment.member2
        if (engineer2):
            if (assignment.member1 == engineer1 and assignment.member2 == engineer2) \
                or (assignment.member1 == engineer2 and assignment.member2 == engineer1):
                
                #test.append(assignment.pairing)
                #test.append({"nulltest": False})
                ttl_assignments += 1
                ttl_assigned_pts += assignment.assigned_points
                ttl_completed_pts += assignment.completed_points

        else:
            #test.append({"nulltest": True}) or assignment.pairing.member2 == engineer1
            if (assignment.member1 == engineer1 and not assignment.member2):
                #test.append(assignment.pairing)
                # test.append({"nulltest": True}) 
                # test.append({"member2": assignment.member2}) 
                ttl_assignments += 1
                ttl_assigned_pts += assignment.assigned_points
                ttl_completed_pts += assignment.completed_points

    return {
        "ttl_assignments": ttl_assignments,
        "ttl_assigned_pts": ttl_assigned_pts,
        "ttl_completed_pts": ttl_completed_pts
        } 

# pairings are across all possible projects
class Pairing(models.Model):
    pair_member1 = models.ForeignKey(
        Engineer, 
        on_delete=models.PROTECT, 
        related_name='pair_member_a', 
        verbose_name="Team Member A",
        limit_choices_to={
            'available_for_sprint': True
        }
    )
    pair_member2 = models.ForeignKey(Engineer, on_delete=models.PROTECT, null=True, blank=True, related_name='pair_member_b', verbose_name="Team Member B")
    #, on_delete=models.SET_DEFAULT

    # temporary attributes - to be function based calculations
    total_sprint_pairings = models.IntegerField(default=0)
    avg_assigned_points = models.IntegerField(default=0)
    avg_completed_points = models.IntegerField(default=0)

    def pairing_name(self):
        tname = ''
        if self.pair_member1 and self.pair_member2:
            if self.pair_member1.last_name >= self.pair_member2.last_name:
                tname = self.pair_member2.last_name + ' / ' + self.pair_member1.last_name  
            else:
                tname = self.pair_member1.last_name + ' / ' + self.pair_member2.last_name 

        elif self.pair_member1:
            tname = self.pair_member1.last_name + ' (solo)'
        elif self.pair_member2:
            tname = self.pair_member2.last_name + ' (solo)'
        else:
            tname = 'ERROR: No members!'

        return tname

    def __str__(self):
        name = self.pairing_name()
        return name

    class Meta:
        verbose_name_plural = "Engineer Pairings"

class SprintPairing(models.Model):
    sprint = models.ForeignKey(
        Sprint, 
        on_delete=models.CASCADE
    )
    member1 = models.ForeignKey(
        Engineer, 
        on_delete=models.PROTECT, 
        related_name='team_member_a', 
        verbose_name="Team Member A",
        limit_choices_to={
            'available_for_sprint': True
        }
    )
    member2 = models.ForeignKey(Engineer, on_delete=models.PROTECT, null=True, blank=True, related_name='team_member_b', verbose_name="Team Member B")
   
    assigned_points = models.IntegerField(default=0)
    completed_points = models.IntegerField(default=0)

    @property
    def project_team(self):
        name = self.sprint.project_team
        return name

    @property
    def sprint_name(self):
        name = self.sprint.sprint_name
        return name

    @property
    def pairing_name(self):
        tname = ''
        if self.member1 and self.member2:
            if self.member1.last_name >= self.member2.last_name:
                tname = self.member2.last_name + ' / ' + self.member1.last_name  
            else:
                tname = self.member1.last_name + ' / ' + self.member2.last_name 

        elif self.member1:
            tname = self.member1.last_name + ' (solo)'
        elif self.member2:
            tname = self.member2.last_name + ' (solo)'
        else:
            tname = 'ERROR: No members!'

        return tname

    @property
    def sprint_pairing(self):
        name = self.sprint_name()  #+ ': ' + self.pairing_name()
        return name

    def __str__(self):
        return self.sprint_pairing
    
    def completion_percentage(self):
        percent = 0
        if self.assigned_points > 0:
            percent = "{0:.0f}%".format(self.completed_points/self.assigned_points * 100)
        return percent

    class Meta:
        verbose_name_plural = "Sprint Assignments"

        
