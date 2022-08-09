# 【Django】共有TODOリスト

デモサイトは<a href="https://1110tk.pythonanywhere.com/" target="_blank">こちら</a>です。

```
上記のユーザー名とパスワードは、
ユーザー名：aiueo
パスワード：miraiktc
です。
```

## ローカルでTODOアプリを動かしてみましょう。  

上のURLからTODOアプリを見ることはできますが、以下の手順に従えば、ご自身のパソコン内からアプリを動かすこともできます。コードを変更して、挙動がどう変わるのかもご確認頂けます。  

1. 環境設定は下記のソフトウェアを参考に、各自の環境に合わせて行って下さい。  
(動作を確認したバージョンを掲載しております)

| ソフトウェア | Version |
----|----
| Python | 3.8.8 |
| Git | 2.33.0 |
| SQLite | 3.35.4 |

2. プロジェクトをコピーするためのフォルダをひとつ作成してください。コマンドプロンプト（あるいはシェル）のカレントディレクトリをそのフォルダ内にするように設定します。
```
: cd フォルダまでのアドレス
```

3. GitHubのURLからローカルにプロジェクトをコピーするために、以下のコマンドをコマンドプロンプトから実行してください。以下、コマンドの実行(:)はWindowsであればコマンドプロンプト、Macであればシェルから実行するコマンドを意味します。  
```
: git clone https://github.com/miraino-katachi/django_todo.git
```

4. 作成されたdjango-todoディレクトリ内に移動してください。  
```
: cd django_todo
```

5. 仮想環境を作ります。  
（ここではvenvという名前で環境を作ります）  
```
: python -m venv venv
```

6. 作成した仮想環境を有効にします。  

仮想環境の必要性と、各OS毎の仮想環境を有効にする方法については<a href="https://camp.trainocate.co.jp/magazine/venv-python/" target="_blank">こちら</a>のサイトをご参照ください。


7. Djangoを動作させるのに、必要なモジュールをインストールします。  
```
: pip install -r requirements.txt
```

8. データベースにTodoモデルを作成します。  
```
: python manage.py makemigrations todo
```

9. データベースのマイグレーションを行います。  
```
: python manage.py migrate
```

10. データベースにアクセスできるユーザーを設定します。
```
: python manage.py createsuperuser  
```
ユーザー名、メールアドレス、パスワードを設定してください。  
ここで作成したユーザーでログインすることができます。  

11. サーバーを開始します。  
```
: python manage.py runserver
```

12. 早速、以下のＵＲＬからコンテンツにアクセスしてみましょう。  
  **http://127.0.0.1:8000/**
