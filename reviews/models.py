from django.db import models
from django.utils.translation import gettext_lazy as _
from django_quill.fields import QuillField
import uuid

class DailyReviewSkill(models.Model):
    skill = models.ForeignKey('tasks.Skill', related_name="daily_reviews_skill", on_delete=models.CASCADE)
    daily_review = models.ForeignKey('reviews.DailyReview', related_name="daily_reviews_skill", on_delete=models.CASCADE)
    time_spent = models.DecimalField(
        verbose_name=_("Time spent in hours"),
        max_digits=5,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.skill.name} - {self.daily_review.created_at.date()} ({self.time_spent}h)"


    class Meta:
        unique_together = ('skill', 'daily_review')


class DailyReview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_('ID'))
    created_at = models.DateTimeField(verbose_name=_('date created'), auto_now_add=True)
    description = QuillField(verbose_name=_('description'), blank=True, null=True)
    skills = models.ManyToManyField('tasks.Skill', related_name='daily_reviews_for_skill', through=DailyReviewSkill)

    def __str__(self):
        return f"Daily Review {self.created_at.date()}"



class WeeklyReview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_('ID'))
    description = QuillField(verbose_name=_('description'), blank=True, null=True)
    created_at = models.DateTimeField(verbose_name=_('date created'), auto_now_add=True)
    start_date = models.DateTimeField() # from
    end_date = models.DateTimeField() # To
    subgoals = models.ManyToManyField(
        'tasks.SubGoal', 
        related_name='weekly_reviews_for_subgoal', 
    )

    def __str__(self):
        return f"Weekly Review {self.start_date.date()} → {self.end_date.date()}"



MONTH_CHOICES = [
    (1, _("January")),
    (2, _("February")),
    (3, _("March")),
    (4, _("April")),
    (5, _("May")),
    (6, _("June")),
    (7, _("July")),
    (8, _("August")),
    (9, _("September")),
    (10, _("October")),
    (11, _("November")),
    (12, _("December")),
]

month = models.PositiveSmallIntegerField(choices=MONTH_CHOICES)


class MonthlyReview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_('ID'))
    created_at = models.DateTimeField(verbose_name=_('date created'), auto_now_add=True)
    month = models.PositiveSmallIntegerField(choices=MONTH_CHOICES)
    year = models.PositiveSmallIntegerField()
    goals = models.ManyToManyField(
        'tasks.Goal', 
        related_name='monthly_reviews_for_goal', 
    )

    def __str__(self):
        month_name = dict(MONTH_CHOICES).get(self.month, "Unknown")
        return f"Monthly Review {month_name} {self.year}"
