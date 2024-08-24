from datetime import timezone
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.db.models import F
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from polls.models import Choice, Question


class IndexView(generic.ListView):
    """Home page, contain list of questions that have been published within 1 day."""
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


def detail(request, question_id):
    """Detail page, contain choices for question."""
    question = get_object_or_404(Question, pk=question_id)
    if question.pub_date > timezone.now():
        raise Http404('Question not found.')
    return render(request, 'polls/detail.html', context={'question': question})


class ResultsView(generic.DetailView):
    """Result page, contain result vote from user for questionZz."""
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    """
    Handle when the user click vote.
    If user does not select any choice, send back detail page with error message.
    Otherwise, add votes for that choice and send back results page.
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        context = {
            "question": question,
            "error_message": "You didn't select a choice.",
        }
        return render(request, "polls/detail.html", context)
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
