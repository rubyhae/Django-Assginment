from django.contrib.auth import get_user_model
from django.db import models
from PIL import Image
from io import BytesIO
from pathlib import Path

User = get_user_model()


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, verbose_name="제목")
    description = models.TextField(verbose_name="설명")
    is_completed = models.BooleanField(default=False, verbose_name="완료 여부")
    start_date = models.DateTimeField(verbose_name="시작 날짜")
    end_date = models.DateTimeField(verbose_name="마감 날짜")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 날짜")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정 날짜")
    # 완료시 이미지과 완료, 기본 썸네일/완료되면 바뀌는 썸네일 = models의 ImageField를 사용하여 각각 이미지를 저장할 경로를 정해주고, 썸네일은 기본으로 완료 이미지에 대신 들어갈 이미지의 경로를 정해준다.
    completed_image = models.ImageField(upload_to='todo/completed_images', null=True, blank=True, verbose_name='완료_이미지')
    thumbnail = models.ImageField(upload_to='todo/thumbnails', default='todo/no_image/NO-IMAGE.gif', null=True,
                                  blank=True, verbose_name='썸네일_이미지')

    class Meta:
        verbose_name = "할 일"
        verbose_name_plural = "할 일 목록"

    def __str__(self):
        return self.title

    # Django 모델에서 save 메서드를 재정의해준 것이고, save()는 데이터베이스에 저장될때 실행된다,.
    def save(self, *args, **kwargs):
        # 만약 업로드된 이미지가 None이거나 False라면
        if not self.completed_image:
            # 부모 super()클래스의 save 메서드를 호출하여 원래의 저장기능을 수행한다.
            return super().save(*args, **kwargs)

        # PIL.Image.open()을 사용해 업로드된 이미지를 열어 image 객체로 변환
        image = Image.open(self.completed_image)
        image.thumbnail((100, 100))  # 썸네일 이미지 크기 지정

        # 업로드된 이미지의 이름을 파일 이름과 확장자를 쉽게 다룰 수 있도록 Path의 객체로 변환하여 image_path로 지정해준다.
        image_path = Path(self.completed_image.name)

        thumbnail_name = image_path.stem  # 업로드된 이미지 명(stem)을 thumbnail_name로 지정
        thumbnail_extension = image_path.suffix  # 업로드된 이미지 확장자(suffix)를 thumbnail_extension로 지정
        thumbnail_filename = f'{thumbnail_name}_thumbnail{thumbnail_extension}'  # 업로드된_이미지_명_thumbnail업로드된_이미지_확장자

        # 원본 이미지의 확장자를 확인해서 적절한 파일 포맷(JPEG, PNG, GIF)을 설정한다.
        if thumbnail_extension in ['.jpg', '.jpeg']:
            file_type = 'JPEG'
        elif thumbnail_extension == '.png':
            file_type = 'PNG'
        elif thumbnail_extension == '.gif':
            file_type = 'GIF'
        else:
            return super().save(*args, **kwargs)
        # 그 무엇도 아니라면 그냥 저장후 종료.

        temp_thumb = BytesIO()  # 메모리에서 임시 파일을 생성하여(BytesIO()/ 메모리에 저장하는 객체) temp_thumb으로 지정해준다.
        image.save(temp_thumb,
                   format=file_type)  # PIL.image.save()메서드를 사용하여 if문을 통해 정해준 file_type로 타입을 지정해준다. (지정해주지 않으면 저장이 불가능하기에 꼭 해줘야한다. )
        temp_thumb.seek(
            0)  # 매모리에 저장한 썸네일 파일은 처음으로 저장한것이니, 첫번째 포인로 이동을 시켜주는 것이다. (이것또한 지정해주지 않으면 특정 포인터를 알아챌 수 없기 때문에 불러오기가 불가능해진다. )

        self.thumbnail.save(thumbnail_filename, temp_thumb, save=False)
        # self.thumbnail은 Django 모델의 ImageField 필드이며,
        # (f'{thumbnail_name}_thumbnail{thumbnail_extension}', file_type, 지금 바로 데이터베이스에 저장해주지 않고 나중에 super().save() 호출시에만 저장이 된다라는 뜻이다. )
        # DB에 불필요한 저장을 없애기 위함.
        temp_thumb.close()  # 객체 닫아주며 메모리 정리.

        return super().save(*args, **kwargs)  # save()를 실행하여 데이터베이스에 변경 사항을 저장해준다.


class Comment(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='comments', verbose_name="할 일")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="유저")
    message = models.TextField(max_length=200, verbose_name="댓글")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 날짜")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정 날짜")

    class Meta:
        verbose_name = "댓글"
        verbose_name_plural = "댓글 목록"

    def __str__(self):
        return f'{self.user}: {self.message}'