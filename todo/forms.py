from django import forms
from django.contrib.auth.models import User
from .models import Todo
from django.utils import timezone
import pprint

class LoginForm(forms.Form):
    username = forms.CharField(label='ユーザー名', max_length=50)
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        print("testan")
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control mb-3"

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        labels = {
            'username': 'ID',
            'password': 'Password'
        }
        error_messages = {
            'username': {
                'required': '必須です!',
            },
            'password': {
                'required': '必須です!',
            }
        }
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        print("testan")
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"

class TodoForm(forms.ModelForm):
    is_finished = forms.BooleanField(required=False,label="完了")
    class Meta:
        model = Todo
        fields = ('item_name','user','expire_date','is_finished','finished_date')
        labels = {
            'item_name': '項目名',
            'user': '担当者',
            'expire_date': '期限日',
        }
        error_messages = {
            "item_name": {
                "required": "項目名が入力されていません",
            },
            "user": {
                "required": "担当者名が入力されていません",
            },
            "expire_date": {
                "required": "期限日が入力されていません",
            },
        }
        widgets = {
            'expire_date': forms.DateInput(attrs={"type":"date"})
        }
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['finished_date'].widget = forms.HiddenInput()
        for field in self.fields:
            if field != "is_finished":
                self.fields[field].widget.attrs["class"] = "form-control"
    def clean_item_name(self):
        item_name = self.cleaned_data.get('item_name')
        if len(item_name) >= 100:
            self.add_error('item_name', '項目名は100文字以内で入力してください')
        return item_name
    def clean_expire_date(self):
        expire_date = self.cleaned_data.get('expire_date')
        try:
            expire_date.strftime('%Y/%m/%d %H:%M:%S')
        except:
            if expire_date is None:
                self.add_error('expire_date', '期限日が入力されていません')
            else:
                self.add_error('expire_date', '日付の形式で入力してください')
        return expire_date

    def clean(self):
        cleaned_data = super().clean()
        is_finished = cleaned_data.get('is_finished')
        if is_finished:
            cleaned_data['finished_date'] = timezone.now()
        else:
            cleaned_data['finished_date'] = None
        return cleaned_data
