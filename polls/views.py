from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from polls.models import Choice, Question, Vote
import logging


logger = logging.getLogger("polls")

def get_client_ip(request):
    """Get the visitor’s IP address using request headers."""
    if request:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
    else:
        ip = 'Unknown'
    return ip

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip_addr = get_client_ip(request)
    logger.info(f"{user.username} logged in from {ip_addr}")

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    ip_addr = get_client_ip(request)
    logger.info(f'{user.username} logged out from {ip_addr}')

@receiver(user_login_failed)
def log_login_failed(sender, credentials, request, **kwargs):
    ip_addr = get_client_ip(request)
    username = credentials.get('username', 'Unknown')
    logger.warning(f"Failed login attempt for {username} from {ip_addr}")


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
            logger.error(f"Non-existent question {question_id}")
            return HttpResponseRedirect(reverse('polls:index'))
        # Check if the question is still in vote session
        if not question.can_vote():
            messages.error(request, "Section closed for voting")
            logger.error(f"Someone try to vote closed question {question_id}")
            return HttpResponseRedirect(reverse('polls:index'))
    except (KeyError, Question.DoesNotExist):
        messages.error(request, "Question not found")
        logger.error(f"Non-existent question {question_id} %s")
        return HttpResponseRedirect(reverse('polls:index'))

    # Get user's vote
    current_user = request.user
    choice = None
    if current_user.is_authenticated:
        try:
            vote = Vote.objects.get(user=current_user, choice__question=question)
            choice = vote.choice
        except (KeyError, Vote.DoesNotExist):
            pass
    context = {'question': question, "selected_choice": choice}
    return render(request, 'polls/detail.html', context=context)


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
        logger.error(f"User try to vote for closed question {question_id}")
        return HttpResponseRedirect(reverse('polls:index'))
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except(KeyError, Choice.DoesNotExist):
        messages.error(request, "You did not select a choice.")
        logger.error("User did not select the choice to vote.")
        return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))

    # Reference to the current user
    current_user = request.user
    # Get the user's vote
    try:
        vote = Vote.objects.get(user=current_user, choice__question = question)
        vote.choice = selected_choice
        vote.save()
        messages.success(request, f'Your vote was changed to {selected_choice.choice_text}')
    except (KeyError, Vote.DoesNotExist):
        # does not have a vote yet
        Vote.objects.create(user=current_user, choice=selected_choice)
        messages.success(request, f'You voted for {selected_choice.choice_text}')

    selected_choice.save()
    logger.info(
        f'User {request.user.username} submitted a vote for choice {selected_choice.id} on question {question.id}')
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
