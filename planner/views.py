from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import BusinessPlan
from .ai import generate_business_plan, AIError


def home(request):
    if request.method == "POST":
        idea_text = (request.POST.get("idea_text") or "").strip()
        if not idea_text:
            messages.error(request, "Please describe your business idea first.")
            return redirect("home")
        try:
            plan_text = generate_business_plan(idea_text)
            plan = BusinessPlan.objects.create(
                idea_text=idea_text, plan_markdown=plan_text
            )
        except AIError as e:
            messages.error(request, str(e))
            return redirect("home")
        except Exception as e:
            # Surface unexpected errors (DB writes, etc.) instead of a blank 500.
            messages.error(request, f"Something went wrong: {type(e).__name__}: {e}")
            return redirect("home")
        return redirect("plan_detail", pk=plan.pk)
    recent = BusinessPlan.objects.all()[:6]
    return render(request, "planner/home.html", {"recent": recent})


def plan_detail(request, pk):
    plan = get_object_or_404(BusinessPlan, pk=pk)
    return render(request, "planner/detail.html", {"plan": plan})
