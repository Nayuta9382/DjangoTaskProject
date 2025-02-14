from django.views import generic,View
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404,redirect
from .models import Task
from .forms import TaskForm,SearchForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
class Top(LoginRequiredMixin,generic.ListView):
    model = Task
    template_name = 'task/top.html'

    # 検索機能の実装
    def get_queryset(self):
        queryset = super().get_queryset()
        form = SearchForm(self.request.GET)

        # 完了/未完了のソート
        complet = self.request.GET.get('complet', False) 
        queryset = queryset.filter(complet_flg=complet)
        
         # 検索機能
        if form.is_valid():
            # パラメータを取得
            title = form.cleaned_data.get('title')
            # titleで部分一致するデータのみ取得
            if title:
                queryset = queryset.filter(title__icontains=title)
        
        # 優先度による絞り込み
        degree = self.request.GET.get('degree')
        if degree in ['high', 'medium', 'low']:  
            queryset = queryset.filter(degree=degree)


        # 日付でのソート（デフォルトは降順）
        order = self.request.GET.get('order', 'asc') 
        if order == 'desc':
            queryset = queryset.order_by('-deadline')  # 降順
        else:
            queryset = queryset.order_by('deadline')  # 昇順
           
        return queryset
    
    

    # 検索するクエリを保持させる
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['searchForm'] = SearchForm(self.request.GET)  # 検索条件を保持するため
        context['order'] = self.request.GET.get('order', 'asc')  # 現在の並び順（昇順・降順）
        context['degree'] = self.request.GET.get('degree')  # 優先度のフィルタを保持
        complet = self.request.GET.get('complet', 'False')
        context['complet'] = complet == 'True'  
        return context

# 新規タスク作成ページ
class CreateTask(LoginRequiredMixin,generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task/add.html'
    success_url = reverse_lazy('task:index')

    def form_valid(self, form):
        # ログインしているユーザーをフォームに設定
        form.instance.user = self.request.user
        return super().form_valid(form)


# 詳細
class DetailTask(LoginRequiredMixin,generic.DeleteView):
    model = Task
    fields = ('id','title','user','detail','deadline','complet_flg')
    template_name = "task/detail.html"

    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()  # 更新対象の投稿オブジェクトを取得
        if task.user != request.user:  # 投稿者と現在のユーザーが一致しない場合
            raise PermissionDenied("このタスクを閲覧する権限がありません。")
        return super().dispatch(request, *args, **kwargs)

# 更新
class UpdateTask(LoginRequiredMixin,generic.UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "task/update.html"

    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()  # 更新対象の投稿オブジェクトを取得
        if task.user != request.user:  # 投稿者と現在のユーザーが一致しない場合
            raise PermissionDenied("このタスクを閲覧する権限がありません。")
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('task:detail', kwargs={'pk': self.object.pk})

    
# 削除
 # 更新後にtopページへリダイレクト
class DeleteTask(LoginRequiredMixin,View):
    def get(self,request,pk):
        task = get_object_or_404(Task, pk=pk) # インスタンスの生成
        # 投稿者以外は403エラーを返す
        if task.user != request.user:
            return PermissionDenied("このタスクを削除する権限がありません。")
        task.complet_flg = not task.complet_flg          
        task.save()
        return HttpResponseRedirect(reverse_lazy('task:index'))

# カスタムエラー
def custom_403_view(request, exception):
    return render(request, '403.html', {'error_message': 'このページへのアクセスは許可されていません。'},status=403)


def custom_404_view(request, exception):
    return render(request, '404.html', {'error_message': 'ページが見つかりません。'})

def custom_500_view(request):
    return render(request, '500.html', {'error_message': '予期せぬエラーが発生しました'})