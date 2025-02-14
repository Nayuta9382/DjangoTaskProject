
from django.urls import path, include 
from . import views

app_name ='task'


urlpatterns = [
    path('',views.Top.as_view(), name='index'), # トップ(一覧)ページ
    path('add',views.CreateTask.as_view(), name='add'), # 新規追加
    path('detail/<int:pk>',views.DetailTask.as_view(), name='detail'), # 詳細表示
    path('update/<int:pk>',views.UpdateTask.as_view(), name='update'), # 更新
    path('delete/<int:pk>',views.DeleteTask.as_view(), name='delete'), # 削除
]
