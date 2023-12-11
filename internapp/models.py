from django.db import models
from django.utils.translation import gettext_lazy as _

# 作業モデル
class Work(models.Model):
    work = models.CharField(max_length=30, verbose_name='作業名')

    class Meta:
        verbose_name_plural = '作業'

    def __str__(self):
        return self.work

# マニュアルモデル
class Manual(models.Model):
    name = models.CharField(max_length=30, verbose_name='マニュアル名')

    class Meta:
        verbose_name_plural = 'マニュアル'

    def __str__(self):
        return self.name

# 手順モデル
class Process(models.Model):
    title = models.CharField(max_length=30, verbose_name='手順名')
    work_set = models.ManyToManyField(Work, verbose_name='作業', related_name='works_for_processes')
    previous = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='next_processes', verbose_name='前の手順')
    move = models.ManyToManyField('self', blank=True, symmetrical=False,  related_name='previous_processes', verbose_name='次の手順')

    class Meta:
        verbose_name_plural = '手順'

    def __str__(self):
        return self.title

# ドキュメント（マニュアルの中身）モデル
class Document(models.Model):
    process_set = models.ManyToManyField(Process, verbose_name='手順', related_name='documents')
    manual = models.ForeignKey(Manual, verbose_name='マニュアル', on_delete=models.PROTECT, related_name='documents', null=True,)
    text = models.TextField(max_length=800, verbose_name='内容')
    relation = models.ManyToManyField(Manual, verbose_name='関連マニュアル', related_name='related_documents', blank=True)

    class Meta:
        verbose_name_plural = 'ドキュメント'

    def __str__(self):
        if self.manual and self.manual.name:
            return self.manual.name
        else:
            return super().__str__()
