from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
import todo
from django.urls import reverse
from todo.form import TodoForm, TodoUpdateForm
from todo.models import Todo

@login_required()
def todo_list(request):
    todos= Todo.objects.filter(user=request.user).order_by('created_at')
    q = request.GET.get('q') # GET 요청으로부터 q에 담긴 쿼리 파라미터를 가져옴
    if q:
     todos = todos.filter(
         Q(title__icontains=q) |
         Q(description__icontains=q)
     )
    paginator = Paginator(todos, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'todos/todo_list.html', context)

@login_required()
def todo_info(request,todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    context = {
        'todo': todo.__dict__  # items 메서드를 사용하기 위해 딕셔너리 형태로 context를 넘겨줍니다.
    }
    return render(request, 'todos/todo_info.html',context)

@login_required()
def todo_create(request):
    form = TodoForm(request.POST or None)
    if form.is_valid():
        todo = form.save(commit=False)
        todo.user = request.user
        todo.save()
        return redirect(reverse('todo_info',kwargs={'todo_id' : todo.pk}))
    context = {'form': form}
    return render(request,'todos/todo_create.html',context)

@login_required()
def todo_update(request,todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    form = TodoUpdateForm(request.POST or None, instance=todo)
    if form.is_valid():
        form.save()
        return redirect(reverse('todo_info', kwargs={'todo_id' : todo.pk}))
    context = {
        'todo': todo,
        'form': form
    }
    return render(request, 'todos/todo_update.html', context)

@login_required()
def todo_delete(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    todo.delete()
    return redirect(reverse('todo_list'))