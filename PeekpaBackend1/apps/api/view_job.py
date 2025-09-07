import uuid
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from apps.api.serializers import ResumeSerializer

from apps.job.models import Resume


class ResumeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        unused_resumes = Resume.objects.filter(user=self.request.user, interviews=None)
        # 删除旧的并且没有和 Interview 关联的 Resume 对象及其关联的文件
        for resume in unused_resumes:
            default_storage.delete(resume.url[6:])
            resume.delete()
        old_resumes = Resume.objects.filter(user=self.request.user)
        # 将和 Interviews 绑定的 Resume 的 is_active 设置成 False
        for resume in old_resumes:
            if resume.is_active:
                resume.is_active = False
                resume.save()
        # 获取上传文件名称
        file = request.FILES.get('resume')
        file_name = file.name
        # 拼凑存储文件名，并存储在 `/media/resume/` 目录下
        file_path = f'resume/{".".join(file_name.split(".")[:-1])}_{str(uuid.uuid4())[:8]}.{file_name.split(".")[-1]}'
        saved_path = default_storage.save(file_path, ContentFile(file.read()))
        resume = Resume.objects.create(name=file_name, user=self.request.user, url='media/{}'.format(saved_path))
        return Response(data=ResumeSerializer(resume).data, status=status.HTTP_201_CREATED)
    
from apps.peekpauser.models import Avatar
from apps.api.serializers import ResumeSerializer, AvatarSerializer

class AvatarView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        old_avatars = Avatar.objects.filter(user=self.request.user)
        # 删除旧的 Avatar 对象及其关联的文件
        for avatar in old_avatars:
            default_storage.delete(avatar.url[6:])
        old_avatars.delete()
        # 获取上传文件名称
        file = request.FILES.get('avatar')
        file_name = file.name
        # 拼凑存储文件名，并存储在 `/media/avatar/` 目录下
        file_path = f'avatar/{".".join(file_name.split(".")[:-1])}_{str(uuid.uuid4())[:8]}.{file_name.split(".")[-1]}'
        saved_path = default_storage.save(file_path, ContentFile(file.read()))
        avatar = Avatar.objects.create(name=file_name, user=self.request.user, url='media/{}'.format(saved_path))
        return Response(data=AvatarSerializer(avatar).data, status=status.HTTP_201_CREATED)
    
from urllib.parse import unquote
from apps.job.models import Job
from django_filters import rest_framework as filters
from django.db.models import Q

class JobListFilter(filters.FilterSet):
    q = filters.CharFilter(method='my_custom_filter', label="Search")
    order = filters.CharFilter(method='order_search', label="Order")
    experience = filters.CharFilter(method='experience_search', label="Experience")
    education = filters.CharFilter(method='education_search', label="Education")

    class Meta:
        model = Job
        fields = ['q', 'order', 'education', 'experience']

    # 自定义搜索
    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(
            Q(title__contains=value) | Q(city__contains=value) | Q(location__contains=value) | Q(company__name__contains=value)
        )

    # 职位学历要求
    def education_search(self, queryset, name, value):
        decoded_data = unquote(value)
        if value:
            return queryset.filter(education=decoded_data)
        return queryset

    # 职位经验要求
    def experience_search(self, queryset, name, value):
        decoded_data = unquote(value)
        if value:
            return queryset.filter(experience=decoded_data)
        return queryset

    # 职位发布时间排序
    def order_search(self, queryset, name, value):
        if value == 'newest':
            return queryset.order_by('-publish_time')
        return queryset
    
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from apps.api.serializers import JobListSerializer

class JobListView(generics.ListAPIView):
    queryset = Job.objects.filter(status=Job.STATUS_PUBLISH).order_by('title')
    serializer_class = JobListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = JobListFilter

from apps.api.serializers import JobSerializer
from apps.api.permissions import IsGetForAll
from apps.api.authentications import PassGetAuthentication

class JobDetailView(generics.RetrieveAPIView):
    queryset = Job.objects.filter(status=Job.STATUS_PUBLISH)
    serializer_class = JobSerializer
    authentication_classes = [PassGetAuthentication]
    permission_classes = [IsGetForAll]
    lookup_field = 'id'

from apps.job.models import Invitation
from apps.api.serializers import InterviewInvitationSerializer
from rest_framework.generics import get_object_or_404

class InvitationDetailView(generics.UpdateAPIView):
    queryset = Invitation.objects.all()
    serializer_class = InterviewInvitationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), candidate=self.request.user, id=self.kwargs['iid'])
        return obj

    def put(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

from django.contrib.auth.models import AnonymousUser
from apps.job.models import PublishJob, Interview

class ApplyJobView(APIView):
    authentication_classes = [PassGetAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        data = dict()
        if isinstance(request.user, AnonymousUser):
            data['message'] = '请登录之后再投递简历。'
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
        else:
            user = request.user
            job = get_object_or_404(Job.objects.all(), id=id)
            poster = PublishJob.objects.get(job__id=id).user
            if job.status != Job.STATUS_PUBLISH:
                return Response(status=status.HTTP_404_NOT_FOUND)
            if user.is_staff:
                data['message'] = '您不可以通过此账号投递简历。'
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            resumes = user.resume.filter(is_active=True)
            if resumes.count() == 0:
                data['message'] = '您还未上传简历，请上传简历之后再投递。'
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            else:
                resume = resumes.all().first()
                Interview.objects.create(job=job, interviewer=poster, candidate=user, resume=resume)
                return Response(data=data, status=status.HTTP_200_OK)