from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Worker, Task, Position


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "position",
        )
        widgets = {
            "position": forms.CheckboxSelectMultiple(),
        }



class WorkerPositionUpdateForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ["position"]
        widgets = {
            "position": forms.CheckboxSelectMultiple,
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            "assignees": forms.CheckboxSelectMultiple,
            "deadline": forms.DateInput(attrs={"type": "date"}),
        }


class WorkerSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by username",
            }
        )
    )


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by task name",
            }
        )
    )


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['name']


class PositionSearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, label="Search Workers")
