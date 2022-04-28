from datetime import datetime, timedelta
from django.db import models

from django.conf import settings
# Create your models here.

if getattr(settings, "USE_TZ", False):
    from django.utils.timezone import localtime as now
else:
    from django.utils.timezone import now


class SoftDeleteManager(models.Manager):
    # 옵션은 기본 매니저로 이 매니저를 정의한 모델이 있을 때 이 모델을 가리키는 모든 관계 참조에서 모델 매니저를 사용할 수 있도록 한다.
    use_for_related_fields = True

    def get_queryset(self):
        return super().get_queryset().filter(delete_date__isnull=True)


class SoftDeleteModel(models.Model):
    reg_date = models.DateTimeField('등록날짜', auto_now_add=True)
    update_date = models.DateTimeField('수정날짜', auto_now=True, null=True)
    delete_date = models.DateTimeField(
        '삭제날짜', blank=True, null=True, default=None)

    class Meta:
        abstract = True  # 상속 할수 있게

    objects = SoftDeleteManager()  # 커스텀 매니저

    def delete(self, using=None, keep_parents=False):
        self.delete_date = now()
        self.save(update_fields=['delete_date'])

    def restore(self):  # 삭제된 레코드를 복구한다.
        self.delete_date = None
        self.save(update_fields=['delete_date'])


class UploadFileModel(models.Model):
    title = models.TextField(default='')
    file = models.FileField(null=True)

    @property
    def get_url(self):
        return self.file.url
