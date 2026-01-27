from django.contrib import admin
from .models import Goal, SubGoal, Skill, Resource

class GoalAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at", "deadline_at", "status"]


class SubGoalAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at", "status"]


class SkillAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at", "status"]


class ResourceAdmin(admin.ModelAdmin):
    list_display = ["skill__name", "name"]


admin.site.register(Goal, GoalAdmin)
admin.site.register(SubGoal, SubGoalAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Resource, ResourceAdmin)