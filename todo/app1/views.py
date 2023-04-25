from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create your views here.
class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task", widget=forms.TextInput(attrs={"class" : "form-control"}))
    priority = forms.IntegerField(min_value = 1, max_value = 10, label="Priority", widget=forms.TextInput(attrs={'class': 'form-control'}))


def index(request):
    
    if "tasks" not in request.session:
        request.session["tasks"] = []

    request.session["tasks"] = sorted(request.session["tasks"], key= lambda x: x["Priority"], reverse=True)
    return render(request, "app1/index.html", context={
        "tasks" : request.session["tasks"]
    })

def add(request):
    if request.method == "POST":

        user_form = NewTaskForm(request.POST)
        if user_form.is_valid():
            task = user_form.cleaned_data["task"]
            priority = user_form.cleaned_data["priority"]

            request.session["tasks"] += [{"Task" : task, "Priority" : priority}]

            return HttpResponseRedirect(reverse("todo:index"))
        else:
            return render(request, "app1/add.html", context={
                "form" : user_form
            })    

    return render(request, "app1/add.html", context={
        "form" : NewTaskForm()
    })