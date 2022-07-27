###
# imports
###
# ショートカット
from django.shortcuts import render,redirect,get_object_or_404
# クラスビュー
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
# フォーム関連
from django import forms
from .forms import LoginForm,TodoForm
# ログイン・ログアウト処理に利用
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# リダイレクト、レスポンス、戻る処理
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
# モデル関連
from .models import Todo
from django.db.models import Q
from django.utils import timezone

# ログイン画面
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
            return HttpResponseRedirect(reverse('list'))
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

# クラスビュー

# 一覧画面
class TodoList(LoginRequiredMixin, ListView):
    # Todoテーブルより呼び出す
    model = Todo
    # レコード情報をテンプレートに渡すオブジェクト
    context_object_name = "todos"
    #テンプレートファイル連携
    template_name = "todo_list.html"
    # Todoの一覧をユーザー、検索文字でフィルタして取得する
    def get_queryset(self):
        search_param = self.request.GET.get('search') # 検索文字の取得
        if search_param is None: # 検索文字がない場合
            query_result = self.model.objects.filter(user=self.request.user) # ログインユーザーでフィルタ
        else: # 検索文字がある場合
            query_result = self.model.objects.filter( \
                Q(item_name__icontains=search_param) | Q(user__username__icontains=search_param), \
                user=self.request.user)
        return query_result # 結果を返す

# 新規作成画面
class TodoCreateView(LoginRequiredMixin, CreateView):
    # Todo
    model = Todo
    # フォームの設定
    form_class = TodoForm
    # ページの設定
    template_name = "todo/edit.html"
    # 新規登録成功時のURL
    success_url = "/"
    # 登録画面として表示する
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crud'] = '登録' # 画面に渡すパラメータにセット
        return context
    # 保存前にフォームのデータを変更する
    def form_valid(self, form):
        todo_form = form.save(commit=False)
        todo_form.registration_date = timezone.now() # 登録日を本日にセット
        todo_form.save() # 保存する
        return redirect('/')

# 更新画面
class TodoUpdateView(LoginRequiredMixin, UpdateView):
    # Todo
    model = Todo
    # フォームの設定
    form_class = TodoForm
    # ページの設定
    template_name = "todo/edit.html"
    # 新規登録成功時のURL
    success_url = "/"
    # 編集画面として表示する
    def get_queryset(self):
        queryset = super().get_queryset()
        print(queryset)
        return queryset.filter(user_id=self.request.user)


# 関数ビュー

# 一覧画面
# @login_required
# def home(request):
#     search = request.GET.get('search')
#     if search is None:
#         todos = Todo.objects.filter(user=request.user)
#         params = {"todos":todos,'CRUD':'一覧'}
#         return render(request, 'todo/todo_list.html', params)
#     todos = Todo.objects.filter(Q(item_name__icontains=search)|Q(user__username__icontains=search),user=request.user)
#     params = {"todos":todos,"search":search}
#     return render(request, 'todo/todo_list.html', params)

# 新規登録画面
# @login_required
# def new(request):
#     if request.method == "POST":
#         form = TodoForm(request.POST)
#         if form.is_valid():
#             todo = form.save(commit=False)
#             todo.registration_date = timezone.now()
#             todo.save()
#             return redirect('/')
#     else:
#         form = TodoForm()
#         form.fields['is_finished'] = forms.BooleanField(label='完了',initial=False, required=False)
#     return render(request, 'todo/edit.html', {'CRUD':'登録','form': form})

# ログイン時のみ、編集画面を表示する
# @login_required
# def edit(request, pk):
#     todo = get_object_or_404(Todo, pk=pk)
#     if request.method == "POST":
#         form = TodoForm(request.POST, instance=todo)
#         if form.is_valid():
#             todo = form.save(commit=False)
#             todo.save()
#             return redirect('edit', pk=todo.pk)
#     else:
#         form = TodoForm(instance=todo)
#         is_finished = True
#         if todo.finished_date is None:
#             is_finished = False
#         form.fields['is_finished'] = forms.BooleanField(label='完了',initial=is_finished, required=False)
#     params = {"form":form,'CRUD':'編集'}
#     print(request.user)
#     return render(request, 'todo/edit.html', params)

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
