# 【Django】共有TODOリスト

デモサイトは<a href="https://1110tk.pythonanywhere.com/" target="_blank">こちら</a>です。

```
上記のユーザー名とパスワードは、
ユーザー名：aiueo
パスワード：miraiktc
です。
```

1. Pythonのインストール
<a href="https://tutorial.djangogirls.org/ja/python_installation/" target="_blank">こちら</a>のページを参照して行ってください。

2. Gitのインストール
<a href="https://tutorial.djangogirls.org/ja/installation/#git" target="_blank">こちら</a>のページを参照して行ってください。

3. GitHubのURLからローカルにプロジェクトをコピーするために、以下のコマンドをコマンドプロンプトから実行してください。以下、コマンドの実行(:)はWindowsであればコマンドプロンプト、Macであればシェルから実行するコマンドを意味します。  
: git clone https://github.com/miraino-katachi/django_todo.git

4. 作成されたdjango-todoディレクトリ内に移動してください。  
: cd django_todo

5. 仮想環境を作ります。  
（ここではvenvという名前で環境を作ります）  
: python -m venv venv

6. 作成した仮想環境を有効にします。  
: .\venv\Scripts\activate

7. Djangoを動作させるのに、必要なモジュールをインストールします。  
: pip install -r requirements.txt

8. データベースにTodoモデルを作成します。  
python manage.py makemigrations todo

9. データベースのマイグレーションを行います。  
:python manage.py migrate

10. 管理ユーザーを設定します。  
:python manage.py createsuperuser  
ユーザー名、メールアドレス、パスワードを設定してください。

11. サーバーを開始します。  
python manage.py runserver

12. 早速、以下のＵＲＬからコンテンツにアクセスしてみましょう。  
http://127.0.0.1:8000/
