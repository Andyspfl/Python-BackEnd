from django import forms

class CreateNewTask(forms.Form):

    title = forms.CharField(label='Título de la tarea', max_length=200)
    description = forms.CharField(label='Descripción de la tarea', widget=forms.Textarea, required=False)
class CreateNewProject(forms.Form):
    name = forms.CharField(label="nombre del project", max_length=100)
