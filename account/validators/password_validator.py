import re

from django.core.exceptions import ValidationError



# パスワードのカスタムバリデータの作成
class PasswordValidator:
     def validate(self, password, user=None):

        # パスワードに文字と数字が含まれているかどうか
        pattern = r'(?=.*\d)(?=.*[a-zA-Z])'
         # パスワードが空でないかを確認
        if not re.match(pattern, password):
            raise ValidationError('パスワードには数字とアルファベットを含めてください')