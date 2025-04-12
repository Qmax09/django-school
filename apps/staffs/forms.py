from django import forms
from ..corecode.models import Subject
from .models import Staff

class StaffForm(forms.ModelForm):
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-inline"}),  # Исправленный виджет
        required=False
    )

    class Meta:
        model = Staff
        fields = "__all__"

