from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from polls.models import Choice, Question, Vote


class IndexView(generic.ListView):
    """Home page, contain list of questions that have been published."""
    template_name = "polls/index.html"
    context_object_name = "question_list"

    def get_queryset(self):
        """Return the list of published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")


def detail(request, question_id):
    """Display the choice for a poll and allow voting."""
    try:
        question = Question.objects.get(pk=question_id)
        # Check if the question is published or not
        if not question.is_published():
            messages.error(request, "Question not found")
            return HttpResponseRedirect(reverse('polls:index'))
        # Check if the question is still in vote session
        if not question.can_vote():
            messages.error(request, "Section closed for voting")
            return HttpResponseRedirect(reverse('polls:index'))
    except (KeyError, Question.DoesNotExist):
        messages.error(request, "Question not found")
        return HttpResponseRedirect(reverse('polls:index'))
    return render(request, 'polls/detail.html', context={'question': question})


class ResultsView(generic.DetailView):
    """Result page, contain result vote from user for questionZz."""
    model = Question
    template_name = "polls/results.html"


@login_required
def vote(request, question_id):
    """
    Handle when the user click vote.
    If user does not select any choice, send back detail page with error message.
    Otherwise, add votes for that choice and send back results page.
    """
    question = get_object_or_404(Question, pk=question_id)
    if not question.can_vote():
        messages.error(request, "Section closed for voting")
        return HttpResponseRedirect(reverse('polls:index'))
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except(KeyError, Choice.DoesNotExist):
        messages.error(request, "You did not select a choice.")
        return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))

    # Reference to the current user
    current_user = request.user
    # Get the user's vote
    try:
        vote = Vote.objects.get(user=current_user, choice__question = question)
        vote.choice = selected_choice
        vote.save()
        messages.success(request, (f'Your vote was changed to' + selected_choice.choice_text))
    except (KeyError, Vote.DoesNotExist):
        # does not have a vote yet
        Vote.objects.create(user=current_user, choice=selected_choice)
        messages.success(request, ('Your voted for' + selected_choice.choice_text))

    selected_choice.save()
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
