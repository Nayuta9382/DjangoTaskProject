from django.db import models
from django.contrib.auth.models import User
from django.db import models
from datetime import timedelta, date

# Create your models here.
class Task(models.Model):

    # 今日の日付から1週間後の日付を計算
    def get_default_deadline():
        return date.today() + timedelta(weeks=1)
    
    # フィールド
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    title = models.TextField( max_length=100)
    detail = models.TextField(blank=True,max_length=255) # 空を許可(nullではない)
    deadline = models.DateField(default=get_default_deadline) # 期限
    degree = models.CharField(max_length=10,choices = (
        ('high', '高'),
        ('medium', '中'),
        ('low', '低'),
        ),default='high') # 優先度
    complet_flg = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)   
    updated_at = models.DateTimeField(auto_now=True)

    # 優先度のクラスを取得するメソッド
    def get_degree_class(self):
        # CSSクラスを定義
        degree_classes = {
            'high': 'bg-red',   
            'medium': 'bg-yellow',  
            'low': 'bg-green',    
        }
        # degreeの値に対応するクラスを返す、デフォルトは空文字
        return degree_classes.get(self.degree, '')
    
    #期限のstatusを返すメソッド
    def get_status(self):
        today = date.today()
        one_week_ago = today - timedelta(weeks=1)
        one_week_later = today + timedelta(weeks=1)

        # 1週間未満
        if self.deadline > today and self.deadline <= one_week_later:
            return 1
        # 期限切れ
        elif self.deadline < today:
            return 2
        # 期限未到達
        else:
            return 0
        
    def __str__(self):
        return (f"{self.title}")