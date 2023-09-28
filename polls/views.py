from django.shortcuts import render, get_object_or_404, redirect
from django.http import  HttpResponseRedirect
from .models import Question, Choice
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .forms import QuestionForm, ChoiceForm
from django.forms import formset_factory
from django.db import transaction

# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
        :5
    ]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)

# def vote(request, question_id):
#     return HttpResponse("You're voting on question %s." % question_id)

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def add_question(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        choice_forms = [ChoiceForm(request.POST, prefix=f'choice_{i}') for i in range(3)]  # Assuming at least three choices are required

        if question_form.is_valid() and all([form.is_valid() for form in choice_forms]):
            question = question_form.save()
            for form in choice_forms:
                choice = form.save(commit=False)
                choice.question = question
                choice.save()
            return redirect('polls:index')  # Redirect to a success page or a different URL after adding the question and choices
    else:
        question_form = QuestionForm()
        choice_forms = [ChoiceForm(prefix=f'choice_{i}') for i in range(3)]  # Initial forms for rendering

    return render(request, 'polls/add.html', {'question_form': question_form, 'choice_forms': choice_forms})