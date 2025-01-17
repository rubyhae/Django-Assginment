from django.shortcuts import render, get_object_or_404
from .models import Todo

def todo_list(request):
    todos = Todo.objects.all()
    return render(request, 'todo_list.html', {'todos': todos})

def todo_info(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    return render(request, 'todo_info.html', {'todo': todo})
