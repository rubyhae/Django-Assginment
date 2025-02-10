from django import forms
from django_summernote.widgets import SummernoteWidget

from todo.models import Todo, Comment


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["title","description","start_date","end_date"]
        labels = {
            'title': '제목',
            'description': '설명',
            'start_date': '시작 날짜',
            'end_date': '마감 날짜',
        }
        widgets = {
            'description':SummernoteWidget(),
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'start_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'end_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
        }

class TodoUpdateForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["title","description","start_date","end_date","is_completed",'completed_image']
        labels = {
            'title': '제목',
            'description': '설명',
            'start_date': '시작 날짜',
            'end_date': '마감 날짜',
            'is_completed':'완료 유무',
        }
        widgets = {
            'description':SummernoteWidget(),
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'start_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'end_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'is_completed':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'completed_image':forms.FileInput(attrs={'class':'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']
        labels = {
            'message':'댓글 내용',
        }
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 4,'cols': 4, 'class':'form-control', 'placeholder':'댓글을 적어주세요.'
            }),
        }