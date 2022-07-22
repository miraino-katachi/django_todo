from django.shortcuts import render
from django import forms
# ログイン・ログアウト処理に利用
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import LoginForm,TodoForm
from .models import Todo
from django.utils import timezone
from django.shortcuts import redirect,get_object_or_404
from django.db.models import Q

# Create your views here.
def todo_list(request):
    return render(request, 'todo/todo_list.html', {})

def Login(request):
    if request.user.is_authenticated:
        return redirect('/')
    params = {'message': '', 'form': None}
    # POST通信だった場合
    if request.method == 'POST':
        # POSTされたフォームを取得する
        form = LoginForm(request.POST)
        # バリデーションを行う
        if form.is_valid():
            pass
        else:
            params['form'] = form
            return render(request, 'todo/login.html', params)
        # idとpasswordを取得して認証を行う
        ID = request.POST.get('username')
        Pass = request.POST.get('password')
        # 認証チェック
        user = authenticate(username=ID, password=Pass)
        # 認証が通った場合
        if user:
            login(request,user)
            return HttpResponseRedirect(reverse('home'))
        else:
            # フォームを表示する
            params['form'] = form
            params['message'] = 'IDかパスワードに誤りがあります'
            # ログイン画面に移行
            return render(request, 'todo/login.html',params)
    # GET通信だった場合
    else:
        params = {'message': '', 'form': None}
        # フォームを表示する
        params['form'] = LoginForm()
        # ログイン画面に移行
        return render(request, 'todo/login.html',params)

# ログイン時のみ、ホーム画面を表示する
@login_required
def home(request):
    search = request.GET.get('search')
    if search is None:
        todos = Todo.objects.filter(user=request.user)
        params = {"todos":todos,'CRUD':'一覧'}
        return render(request, 'todo/todo_list.html', params)
    todos = Todo.objects.filter(Q(item_name__icontains=search)|Q(user__username__icontains=search),user=request.user)
    params = {"todos":todos,"search":search}
    return render(request, 'todo/todo_list.html', params)

# ログイン時のみ、新規作成画面を表示する
@login_required
def new(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.registration_date = timezone.now()
            todo.save()
            return redirect('/')
    else:
        form = TodoForm()
        form.fields['is_finished'] = forms.BooleanField(label='完了',initial=False, required=False)
    return render(request, 'todo/edit.html', {'CRUD':'登録','form': form})

# ログイン時のみ、編集画面を表示する
@login_required
def edit(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.save()
            return redirect('edit', pk=todo.pk)
    else:
        form = TodoForm(instance=todo)
        is_finished = True
        if todo.finished_date is None:
            is_finished = False
        form.fields['is_finished'] = forms.BooleanField(label='完了',initial=is_finished, required=False)
    params = {"form":form,'CRUD':'編集'}
    print(request.user)
    return render(request, 'todo/edit.html', params)

# ログイン時のみ、削除処理を行う
@login_required
def delete(request):
    id = request.POST.get('id')
    todo = Todo.objects.get(pk=id)
    todo.is_deleted = 1
    todo.save()
    return redirect('/')

# ログイン時のみ、完了処理を行う
@login_required
def complete(request):
    id = request.POST.get('id')
    print(id)
    todo = Todo.objects.get(pk=id)
    todo.finished_date = timezone.now()
    todo.save()
    return redirect('/')

#ログアウト
@login_required
def Logout(request):
    logout(request)
    # ログイン画面遷移
    return HttpResponseRedirect(reverse('Login'))
