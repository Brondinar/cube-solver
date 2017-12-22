from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Question, Choice
from django.utils import timezone

# Create your models here.
class Index_View(ListView):
    template_name = 'polls_djbook_tutorial/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class Detail_View(DetailView):
    model = Question
    template_name = 'polls_djbook_tutorial/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class Results_View(DetailView):
    model = Question
    template_name = 'polls_djbook_tutorial/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls_djbook_tutorial/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls_djbook_tutorial:results', args=(question.id,)))