from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Prefetch, F, Window
from django.db.models.functions import RowNumber
from .models import Goal, SubGoal, Skill
from django.db.models import Count, Q, F, ExpressionWrapper, IntegerField, Value, Sum, FloatField
from django.db.models.functions import Coalesce, Cast


@login_required
def goals(request):
    goals = (
        request.user.goals
        .annotate(
            all_subgoals_count=Count("subgoals", distinct=True),
            finish_subgoals_count=Count(
                "subgoals",
                filter=Q(subgoals__status="finished"),
                distinct=True
            ),
            skills_count=Count("subgoals__skills", distinct=True),
            time_spent=Coalesce(
                Sum('subgoals__skills__daily_reviews_skill__time_spent'),
                Value(0),
                output_field=FloatField()
            ),
            progress=ExpressionWrapper(
                Cast(F('finish_subgoals_count'), IntegerField()) * 100
                / Coalesce(Cast(F('all_subgoals_count'), IntegerField()), Value(1)),
                output_field=IntegerField()
            )
        ).order_by("created_at")
    )


    paginator = Paginator(goals, 10)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj}

    if request.htmx:
        return render(request, "cotton/partials/goals_partial.html", context)
    return render(request, "tasks/goals.html", context)


@login_required
def goal_details(request, id):
    goal = get_object_or_404(Goal, id=id, user=request.user)
    skills_qs = Skill.objects.annotate(
        row_number=Window(
            expression=RowNumber(),
            partition_by=[F('subgoal_id')],
            order_by=F('created_at').asc()
        )
    ).filter(row_number__lte=5)

    skills_prefetch = Prefetch(
        'skills',
        queryset=skills_qs,
        to_attr='preview_skills'
    )

    subgoals = goal.subgoals.prefetch_related(skills_prefetch)
    paginator = Paginator(subgoals, 10)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj, "goal": goal}

    if request.htmx:
        return render(request, "cotton/partials/goal_details_partial.html", context)
    return render(request, "tasks/goal_details.html", context)