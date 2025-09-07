from django.db import models
from apps.peekpauser.models import User

class Resume(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resume')
    url = models.URLField()
    is_active = models.BooleanField(default=True)

from apps.company.models import Company

class Job(models.Model):
    STATUS_PUBLISH = 0
    STATUS_CLOSE = 1
    STATUS_FINISH = 2
    STATUS_ITEMS = (
        (STATUS_PUBLISH, '已发布'),
        (STATUS_CLOSE, '已下线'),
        (STATUS_FINISH, '已结束'),
    )

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    status = models.PositiveIntegerField(default=STATUS_PUBLISH, choices=STATUS_ITEMS)
    city = models.CharField(max_length=10, null=True)
    location = models.CharField(max_length=50, null=True)
    salary_min = models.PositiveIntegerField(default=0)
    salary_max = models.PositiveIntegerField(default=0)
    salary_count = models.PositiveIntegerField(default=0)
    hire_number = models.PositiveIntegerField(default=1)
    experience = models.CharField(max_length=50)
    benefit = models.CharField(max_length=300)
    education = models.CharField(max_length=30)
    description = models.CharField(max_length=3000)
    publish_time = models.DateTimeField(auto_now_add=True)
    resumes = models.ManyToManyField(Resume)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, related_name='jobs')

class PublishJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    
class Interview(models.Model):
    id = models.AutoField(primary_key=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='interviews')
    interviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interviews')  # 面试者，即招聘者
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_interviews')  # 求职者
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='interviews')
    status = models.PositiveIntegerField(default=0)
    publish_time = models.DateTimeField(auto_now_add=True)
    feedback = models.JSONField(default=dict)

from datetime import timedelta
from django.db.models import F
from django.utils import timezone

class Invitation(models.Model):
    RESPONSE_UNRESPONSE = 0
    RESPONSE_YES = 1
    RESPONSE_NO = 2
    RESPONSE_CLOUSE = 3
    RESPONSE_ITEMS = (
        (RESPONSE_UNRESPONSE, '未回复'),
        (RESPONSE_YES, '同意'),
        (RESPONSE_NO, '拒绝'),
        (RESPONSE_CLOUSE, '取消'),
    )
    id = models.AutoField(primary_key=True)
    status = models.PositiveIntegerField(default=0)
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name='invitations')  # 面试邀请
    message = models.CharField(max_length=200)
    interviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interview_invitation')  # 招聘者
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_invitation')  # 求职者
    response = models.PositiveIntegerField(default=RESPONSE_UNRESPONSE, choices=RESPONSE_ITEMS)
    publish_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    due_time = models.DateTimeField() 

    def save(self, *args, **kwargs):
        self.update_time = timezone.now()  # 在保存模型时更新 update_time 字段
        super().save(*args, **kwargs)

    