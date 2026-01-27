from django.contrib import admin
from .models import DailyReview, DailyReviewSkill, WeeklyReview, MonthlyReview

class DailyReviewAdmin(admin.ModelAdmin):
    list_display = ["created_at"]


class DailyReviewSkillAdmin(admin.ModelAdmin):
    list_display = ["skill__name", "daily_review__created_at", "time_spent"]


class WeeklyReviewAdmin(admin.ModelAdmin):
    list_display = ["created_at", "start_date", "end_date"]


class MonthlyReviewAdmin(admin.ModelAdmin):
    list_display = ["month", "year"]


admin.site.register(DailyReview, DailyReviewAdmin)
admin.site.register(DailyReviewSkill, DailyReviewSkillAdmin)
admin.site.register(WeeklyReview, WeeklyReviewAdmin)
admin.site.register(MonthlyReview, MonthlyReviewAdmin)