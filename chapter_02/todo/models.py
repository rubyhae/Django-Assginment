from django.contrib.auth import get_user_model
#from django.contrib.auth.models import User
from django.db import models

# Create your models here.

User = get_user_model()

class Todo(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE) # 로그인유저 확인
    title = models.CharField(max_length=50) # 제목
    info = models.TextField() # 할일 설명
    start_date = models.DateField() # 시작 날짜
    end_date = models.DateField() # 끝나는 날짜
    is_done = models.BooleanField(default=False) # 완료 여부
    created_at = models.DateTimeField(auto_now_add=True) # 생성 날짜
    updated_at = models.DateTimeField(auto_now=True) # 수정 날짜


    def __str__(self):
        return self.title