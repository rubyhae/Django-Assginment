
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import QuerySet, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.template.context_processors import request

from todo.form import TodoForm, TodoUpdateform
from todo.models import Todo
from django.urls import reverse


# Create your views here.

# 할 일 리스트
@login_required()
def todo_list (request):
    todo_list = Todo.objects.filter(user=request.user)

    # 검색 대상 설정
    q = request.GET.get('q')
    if q:
        todo_list = todo_list.filter(
            Q(title__icontains=q) |
            Q(info__icontains=q)
        )
    # 한 페이지당 10개
    paginator =Paginator(todo_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'q':q,
    }
    print(page_obj)
    return render(request,'todo_list.html',context)

# 특정 할 일 보기
@login_required()
def todo_info(request,todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    context = {
            'todo' : todo,}
    return render(request,'todo_info.html', context)


# 할 일 추가
@login_required()
def todo_create(request):
    form = TodoForm(request.POST or None)
    if form.is_valid():
        todo = form.save(commit=False) # 유저추가해야해서 아직 wait
        todo.user = request.user
        todo.save()
        return redirect(reverse('todo_info',kwargs={'todo_id':todo.pk}))
    context = {
        'form':form
    }
    return render(request, 'todo_create.html',context)

# 할 일 수정
@login_required()
def todo_update(request,todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user = request.user)
    form = TodoUpdateform(request.POST or None , instance=todo)
    if form.is_valid():
        form.save()
        return redirect(reverse('todo_info',kwargs={'todo_id':todo.pk}))
    context = {
        'form':form,
        'todo':todo
    }
    return render(request,'todo_update.html',context)

# 할 일 삭제
@login_required()
def todo_delete(request,todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user =request.user)
    todo.delete()
    return redirect(reverse('todo_list'))
