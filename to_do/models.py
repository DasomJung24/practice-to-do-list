from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from core.models import Employee


class ToDoList(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    name = models.CharField(_('이름'), max_length=20)

    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_datetime',)

    def __str__(self):
        return f'{self.employee.name} > {self.name}'

    def sorted_to_do(self):
        to_do = self.to_do.select_related(
            'content',
            'is_important',
            'to_do_date_time'
        ).all()
        # to_do_close = to_do.filter(to_do_date_time__lte=timezone.now())
        return to_do


class ToDo(models.Model):
    to_do_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE, related_name='to_do')

    content = models.CharField(_('내용'), max_length=50)
    is_important = models.BooleanField(_('중요도설정'), default=False, choices=((True, '중요'), (False, '중요하지 않음')))
    is_checked = models.BooleanField(_('할일완료'), default=False, choices=((True, '완료'), (False, '완료되지 않음')))
    to_do_date_time = models.DateTimeField()

    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-is_important', '-to_do_date_time', '-created_datetime')

    def __str__(self):
        return f'{self.to_do_list.name} : {self.content}'
