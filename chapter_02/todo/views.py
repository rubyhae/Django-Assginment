from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from todo.forms import TodoForm, TodoUpdateForm
from todo.models import Todo
from django.db.models import Q

# 랜더링 함수 작성하기 : To.do 모델의 제목을 가지고 와야함. 장고 ORM을 사용한다.
'''
QuerySet 쿼리셋 : Django ORM에서 제공하는 데이터 타입으로, 데이터베이스에서 전달받은 객체 목록이다.
구조는 list와 같지만, 파이썬의 기본 자료구조가 아니기때문에, 파이썬 파일에서 읽고 쓰기 위해선 자료형 변환을 해줘야 한다.

1. select
- objects.all() : 해당 테이블에 모든 데이터 조회, QuerySet 타입으로 반환
- objects.get() : 하나의 row만 조회, 주로 pk컬럼으로 조회, 
결과가 1건 이상일 경우 에러 발생, QeuerySet 타입이 아닌 객체 타입으로 반환
- objects.filter() : 특정 조건에 맞는 데이터만 조회, QuerySet 타입으로 반환
- objects.exclude() : 특정 조건 제외한 데이터들만 조회, QuerySet 타입으로 반환
- objects.count() : 쿼리 셋에 포함된 데이터의 개수를 리턴
- objects.exists() : 해당 테이블에 데이터가 있는 지 확인후 있으면 True 없으면 False 반환
- objects.values() : QuerySet의 내용을 딕셔너리 형태로 반환, 인자 값에 아무것도 없다면 해당 클래스의 모든 필드, 값을 보여주고,
인자 값에 특정 필드를 입력하면 입력한 필드에 대한 값들이 반환된다.
(예: Todo.objects.values() => {'id' : 1 , 'name' : '아이스크림'},..
 Todo.objects.values('name') => {'name' : '아이스크림'},{'name' : '과자'},...)

- objects.values_list() : values()와 같은 기능을 하나, 반환형태가 리스트이다.
- objects.order_by() : 특정 필드 기준으로 정렬할 때 사용, 필드명 앞에 -이 붙으면 내림차순 의미

2.insert
- objects.create() : 한가지 생성
- objects.bulk_create() : 여러개의 objects 한꺼번에 생성

__icontain : 특정 문자가 포함된 것을 찾을 때에 대소문자를 구분하지 않고 찾음.


'''


# todo_list
@login_required()
def todo_list(request):
    todo_list = Todo.objects.filter(user=request.user).order_by('created_at')
    q = request.GET.get('q')
    if q:
        todo_list = todo_list.filter(Q(title__icontains=q) | Q(description__icontains=q))
    paginator = Paginator(todo_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'todo/todo_list.html', context)


# todo_info
@login_required()
def todo_info(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)  # 투두 모델의 id 인것들만 객체로 가지고 오겠다라는 뜻.
    context = {
        'todo': todo.__dict__
    }  # 투두는 모델의 인스턴스이고, 투두.__dict__은 투두 객체 속성을 포함해 딕셔너리로 반환한다.
    return render(request, 'todo/todo_info.html', context)


@login_required()
def todo_create(request):
    form = TodoForm(request.POST or None)
    if form.is_valid():  # 폼의 유효성을 체크한다.
        todo = form.save(commit=False)
        todo.user = request.user
        todo.save()
        return redirect(reverse('todo_info', kwargs={'todo_id': todo.pk}))
    context = {
        'form': form
    }
    return render(request, 'todo/todo_create.html', context)


@login_required()
def todo_update(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    form = TodoUpdateForm(request.POST or None, instance=todo)
    if form.is_valid():
        form.save()
        return redirect(reverse('todo_info', kwargs={'todo_id': todo.pk}))
    context = {
        'form': form
    }
    return render(request, 'todo/todo_update.html', context)


@login_required()
def todo_delete(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    todo.delete()
    return redirect(reverse('cbv_todo_list'))
