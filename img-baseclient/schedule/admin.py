from django.contrib import admin

from .models import ProjectTeam, Engineer, Sprint, Pairing, SprintPairing


# admin.site.register(Engineer)
# admin.site.register(Sprint)
# admin.site.register(SprintPairing)
# admin.site.register(Pairing)

@admin.register(ProjectTeam)
class ProjectTeamAdmin(admin.ModelAdmin):
    list_display = ("project_team", "team_lead", "go_live_date", "next_start_date")

@admin.register(Engineer)
class EngineerAdmin(admin.ModelAdmin):
    list_display = ("full_name", "last_name", "first_name", "available_for_sprint") # , "avg_team_points_assigned", "avg_team_points_completed"
    list_filter = ('project_team',)

@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    list_display = ("sprint_name", "sprint_start_date","sprint_duration", "assigned_points", "completed_points", "completion_percentage", "sprint_status")


@admin.register(Pairing)
class PairingAdmin(admin.ModelAdmin):
    list_display = ("pairing_name", "total_sprint_pairings", "avg_assigned_points", "avg_completed_points")

#"team_member1", "team_member2", 

@admin.register(SprintPairing)
class SprintPairingAdmin(admin.ModelAdmin):
    list_display = ("sprint_pairing", "pairing_name", "assigned_points", "completed_points", "completion_percentage")

      #NOT WORKING!!!
    #list_filter = ('sprint__project_team',)

      #  ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),

