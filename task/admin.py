from django.contrib import admin
from django.contrib.auth.models import User  # User モデルをインポート

# Register your models here.
# from アプリケーション名.models import マイグレーションのクラス名
from task.models import Task
admin.site.register(Task)
