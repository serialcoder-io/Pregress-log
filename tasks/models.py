from django.db import models
from django.utils.translation import gettext_lazy as _
from django_quill.fields import QuillField
import uuid

class StatusChoices(models.TextChoices):
    PENDING = 'pending', _('Pending')
    IN_PROGRESS = 'in_progress', _('In Progress')
    FINISHED = 'finished', _('Finished')

class Goal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_('ID'))
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="goals")
    name = models.CharField(verbose_name=_('goal name'), max_length=50)
    description = QuillField(verbose_name=_('description'), blank=True, null=True)
    created_at = models.DateTimeField(verbose_name=_('date created'), auto_now_add=True)
    started_at = models.DateTimeField(verbose_name=_('start date'), null=True, blank=True)
    completed_at = models.DateTimeField(verbose_name=_('end date'),  null=True, blank=True)
    deadline_at = models.DateTimeField(verbose_name=_('deadline'), null=True, blank=True)
    status = models.CharField(verbose_name=_('status'), max_length=20, choices=StatusChoices, default=StatusChoices.PENDING)

    @property
    def total_time_spent(self):
        return sum(subgoal.total_time_spent for subgoal in self.subgoals.all())

    class Meta:
        db_table = 'goal'
        unique_together = ('user', 'name')

    def __str__(self):
        return self.name
    

class SubGoal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_('ID'))
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name="subgoals")
    name = models.CharField(verbose_name=_('subgoal name'), max_length=50)
    description = QuillField(verbose_name=_('description'), blank=True, null=True)
    created_at = models.DateTimeField(verbose_name=_('date created'), auto_now_add=True)
    started_at = models.DateTimeField(verbose_name=_('start date'), null=True, blank=True)
    completed_at = models.DateTimeField(verbose_name=_('end date'),  null=True, blank=True)
    deadline_at = models.DateTimeField(verbose_name=_('deadline'), null=True, blank=True)
    status = models.CharField(verbose_name=_('status'), max_length=20, choices=StatusChoices, default=StatusChoices.PENDING)

    @property
    def total_time_spent(self):
        return sum(skill.total_time_spent for skill in self.skills.all())

    class Meta:
        db_table = 'subgoal'
        unique_together = ('goal', 'name')

    def __str__(self):
        return f"{self.name} ({self.goal.name})"
    

class Skill(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_('ID'))
    subgoal = models.ForeignKey(SubGoal, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(verbose_name=_('skill name'), max_length=50)
    description = QuillField(verbose_name=_('description'), blank=True, null=True)
    created_at = models.DateTimeField(verbose_name=_('date created'), auto_now_add=True)
    started_at = models.DateTimeField(verbose_name=_('start date'), null=True, blank=True)
    completed_at = models.DateTimeField(verbose_name=_('end date'),  null=True, blank=True)
    status = models.CharField(verbose_name=_('status'), max_length=20, choices=StatusChoices, default=StatusChoices.PENDING)
    
    @property
    def total_time_spent(self):
        return self.daily_reviews_skill.aggregate(
            total=models.Sum('time_spent')
        )['total'] or 0

    class Meta:
        db_table = 'skill'
        unique_together = ('subgoal', 'name')

    def __str__(self):
        return f"{self.name} ({self.subgoal.name})"
    

class Resource(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_('ID'))
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="resources")
    name = models.CharField(verbose_name=_('Resource name'), max_length=50)
    url = models.URLField()

    class Meta:
        db_table = 'resource'
        constraints = [
            models.UniqueConstraint(
                fields=['skill', 'name', 'url'],
                name='unique_resource_per_skill'
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.skill.name})"