from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User  # Userモデルのインポート
from django.core.exceptions import ValidationError
import re



# ログインにエラーメッセージをカスタム
class LoginForm(AuthenticationForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages = {
            'invalid_login': _('ユーザー名またはパスワードが一致しません'),
            'inactive': _('ユーザー名またはパスワードが一致しません'),
        }
         
        # フィールドにclassとplaceholderを追加
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',  # クラス名を指定
            'placeholder': 'ユーザー名を入力してください'  # プレースホルダーを指定
        })
        
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',  # クラス名を指定
            'placeholder': 'パスワードを入力してください'  # プレースホルダーを指定
        })

# サインアップのカスタムフォーム
class SignupForm(UserCreationForm):

    # 使用するモデルとフィールドを定義
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # ラベルの明示的な上書き
        self.fields["username"].label = "ユーザー名"
        self.fields["password1"].label = "パスワード"
        self.fields["password2"].label = "パスワード確認"

        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

        # ヘルプテキストの明示的な上書き
        self.fields["username"].help_text = ""
        self.fields["password1"].help_text = "パスワードはアルファベットと数字を必ず含め、8文字以上で入力してください"
        self.fields["password2"].help_text = ""
    
   