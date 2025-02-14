from django import forms
from .models import Task
from django.utils import timezone  # timezoneをインポート

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'detail', 'deadline', 'degree')  # フィールドを指定
        labels = {
            'title': 'タイトル',
            'detail': '詳細',
            'deadline': '期限',
            'degree': '優先度'
        }
        help_texts = {
            'title': '',
            'detail': '',
            'deadline': 'タスクの期限は本日以降で設定してください'
        }
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),  # 日付入力フィールドを設定
            'title': forms.TextInput(attrs={'type': 'text'})  # 日付入力フィールドを設定
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
        
        # 一括で適用するフィールドの設定
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'タスクのタイトルを入力してください',  'style': 'font-weight: 400;' })
        self.fields['detail'].widget.attrs.update({'class': 'form-control', 'placeholder': 'タスクの詳細を入力してください', 'rows': 4})
        self.fields['deadline'].widget.attrs.update({'class': 'form-control w-50'})
        self.fields['degree'].widget.attrs.update({'class': 'class=" form-control form-select form-select-sm mb-3 w-25'})
    
    # 本日以降の日付を設定するためのバリデーション
    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')
        if deadline and deadline < timezone.now().date():
            raise forms.ValidationError('本日以降の日付を設定してください')
        return deadline

class SearchForm(forms.ModelForm): # topページで使用
    class Meta:
        model = Task
        fields = ['title']

    title = forms.CharField(
        required=False,
        label='タイトル',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'タイトル',
                'class': 'form-control ',  # class を追加
                'aria-label': 'Search',  # aria-label を追加
                'style': 'height:36px',  # スタイルを追加
                'type': 'search', 
            }
        )
)