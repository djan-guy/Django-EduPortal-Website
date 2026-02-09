from django import forms
from django.forms import inlineformset_factory
from .models import Quiz, Question

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['course', 'name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
        }

QuestionFormSet = inlineformset_factory(
    Quiz,
    Question,
    fields=('text', 'option_a', 'option_b', 'option_c', 'correct_answer', 'marks'),
    extra=1,
    can_delete=True,
)
