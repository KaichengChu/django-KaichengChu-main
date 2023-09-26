from django import forms
from .models import Question, Choice

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']

ChoiceFormSet = forms.inlineformset_factory(
    Question,  
    Choice,    
    fields=['choice_text'],  
    extra=3
)
