from rest_framework import serializers
from apps.peekpauser.models import User


class LoginSerializer(serializers.ModelSerializer): 
    email = serializers.EmailField(max_length=255, min_length=6, write_only=True)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'token']

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=20, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = User.objects.create_user(email, password)
        user.first_name = validated_data.get('first_name')
        user.last_name = validated_data.get('last_name')
        user.save()
        return user

from apps.job.models import Resume

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = '__all__'

from apps.peekpauser.models import User, Avatar

class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = '__all__'

class AdminUserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['uid', 'email', 'first_name', 'last_name', 'gender', 'data_join', 'last_login',
                  'is_active']
        
from apps.company.models import Company

class AdminCompanyUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['uid', 'email', 'first_name', 'last_name', 'data_join']


class AdminCompanyListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    email = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def get_user(self, obj):
        user = User.objects.filter(details__contains={'company_id': obj.id, "is_manager": True})
        if user.count():
            return AdminCompanyUserSerializer(user.all().first()).data
        return None

    class Meta:
        model = Company
        fields = ['id', 'name', 'website', 'user', 'email', 'first_name', 'last_name', 'password']

from apps.job.models import Interview, Job

class JobListSerializer(serializers.ModelSerializer):
    resumes = serializers.SerializerMethodField(read_only=True)
    pass_number = serializers.SerializerMethodField()
    company_name = serializers.CharField(source='company.name', read_only=True)
    company_tags = serializers.CharField(source='company.tags', read_only=True)
    company_avatar = serializers.CharField(source='company.avatar', read_only=True)
    company_id = serializers.CharField(source='company.id', read_only=True)

    def get_resumes(self, obj):
        return Interview.objects.filter(job__id=obj.id).count()

    def get_pass_number(self, obj):
        return Interview.objects.filter(job__id=obj.id, status=4).count()
    
    def to_representation(self, instance):
        ret = super(JobListSerializer, self).to_representation(instance)
        if not (self.context.get('request') and self.context.get('request').user and self.context.get(
                'request').user.is_staff):
            ret.pop("status")
            ret.pop("pass_number")
            ret.pop("hire_number")
            ret.pop("resumes")
        return ret

    class Meta:
        model = Job
        fields = ['id', 'title', 'status', 'city', 'location', 'salary_min', 'salary_max', 'salary_count', 'education',
                  'experience', 'benefit', 'publish_time', 'pass_number', 'hire_number', 'resumes',
                  'company_name', 'description', 'company_tags', 'company_avatar', 'company_id']
        read_only_fields = ['id', 'publish_time', 'pass_number']

from django.contrib.auth.models import AnonymousUser

class JobSerializer(serializers.ModelSerializer):
    pass_number = serializers.SerializerMethodField()
    company_name = serializers.CharField(source='company.name', read_only=True)
    company_tags = serializers.CharField(source='company.tags', read_only=True)
    company_size = serializers.CharField(source='company.size', read_only=True)
    company_website = serializers.CharField(source='company.website', read_only=True)
    company_id = serializers.CharField(source='company.id', read_only=True)
    has_resume = serializers.SerializerMethodField()   # 是否有简历
    applied = serializers.SerializerMethodField()  # 是否申请
    resumes = serializers.SerializerMethodField()

    def get_applied(self, obj):
        if self.context.get('request') \
                and self.context.get('request').user \
                and not isinstance(self.context.get('request').user, AnonymousUser) \
                and not self.context.get('request').user.is_staff:
            user_uid = self.context.get('request').user.uid
            apply = Interview.objects.filter(candidate__uid=user_uid, job=obj).count()
            return bool(apply)
        return False

    def get_has_resume(self, obj):
        if self.context.get('request') \
                and self.context.get('request').user \
                and not isinstance(self.context.get('request').user, AnonymousUser) \
                and not self.context.get('request').user.is_staff \
                and self.context.get('request').user.resume.all().count():
            return True
        return False

    def get_resumes(self, obj):
        return obj.resumes.count()

    def get_pass_number(self, obj):
        return Interview.objects.filter(job__id=obj.id, status=4).count()

    class Meta:
        model = Job
        fields = ['id', 'title', 'status', 'city', 'location', 'salary_min', 'salary_max', 'salary_count', 'education',
                  'pass_number', 'hire_number', 'experience', 'benefit', 'description', 'publish_time', 'resumes',
                  'company_name', 'company_tags', 'company_size', 'company_website', 'company_id', 'has_resume', 'applied']
        read_only_fields = ['id', 'pass_number', 'publish_time', 'resumes', 'has_resume', 'applied']

from apps.job.models import Invitation
class InterviewInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['id', 'response', 'publish_time', 'due_time', 'message', 'update_time']

class InterviewJobSerializer(serializers.ModelSerializer):
    pass_number = serializers.SerializerMethodField()

    def get_pass_number(self, obj):
        return Interview.objects.filter(job__id=obj.id, status=4).count()

    class Meta:
        model = Job
        fields = ['id', 'pass_number', 'hire_number', 'title']

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uid', 'email', 'name', 'gender', 'details']

class InterviewResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['name', 'url']

class InterviewSerializer(serializers.ModelSerializer):
    job = InterviewJobSerializer()
    candidate = CandidateSerializer()
    interviewer = serializers.CharField(source='interviewer.name')
    resume = InterviewResumeSerializer()
    invitation = serializers.SerializerMethodField()

    def get_invitation(self, obj):
        invitations = obj.invitations.all()
        if invitations.count():
            invitation = invitations.filter(status=obj.status)
            if invitation.count():
                return InterviewInvitationSerializer(invitation.all().first()).data
        return None

    class Meta:
        model = Interview
        fields = ['id', 'job', 'interviewer', 'candidate', 'resume', 'status', 'feedback', 'invitation', 'publish_time']
        read_only_fields = ['resume', 'candidate', 'interviewer', 'invitation', 'publish_time']

class InvitationJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title']

from rest_framework.generics import get_object_or_404

class InvitationSerializer(serializers.ModelSerializer):
    candidate = CandidateSerializer(read_only=True)
    job = serializers.SerializerMethodField()
    user_uid = serializers.CharField(write_only=True)
    status = serializers.IntegerField(write_only=True)

    def get_job(self, obj):
        job = Job.objects.get(interviews__invitations__id=obj.id)
        return InvitationJobSerializer(job).data
    # 新添加的方法
    def create(self, validated_data):
        request = self.context.get('request')
        url_kwargs = self.context.get('view').kwargs
        job_id = url_kwargs.get('id')
        interview_id = url_kwargs.get('iid')
        user_uid = validated_data.pop('user_uid')

        get_object_or_404(Job, id=job_id)
        interview = get_object_or_404(Interview, id=interview_id)
        user = User.objects.get(uid=user_uid)
        interviewer = request.user
        invitation = Invitation.objects.create(
            interview=interview,
            candidate=user,
            interviewer=interviewer,
            **validated_data
        )
        return invitation

    class Meta:
        model = Invitation
        fields = ['message', 'response', 'candidate', 'publish_time', 'due_time', 'job', 'user_uid', 'update_time',
                  'status']
        read_only_fields = ['response', 'publish_time', 'due_time', 'candidate', 'job', 'update_time']

class CompanyListSerializer(serializers.ModelSerializer):
    jobs = serializers.SerializerMethodField()
    interviews = serializers.SerializerMethodField()

    def get_interviews(self, obj):
        job_ids = obj.jobs.values_list('id', flat=True)
        return Interview.objects.filter(status__in=[0, 1, 2, 3], job__id__in=job_ids).count()

    def get_jobs(self, obj):
        return obj.jobs.count()

    class Meta:
        model = Company
        fields = ['id', 'name', 'slogan', 'avatar', 'tags', 'size', 'jobs', 'interviews']

class CompanySerializer(serializers.ModelSerializer):
    jobs = serializers.SerializerMethodField()

    def get_jobs(self, obj):
        jobs = Job.objects.filter(company__id=obj.id, status=Job.STATUS_PUBLISH).all()
        return JobListSerializer(jobs, many=True).data

    class Meta:
        model = Company
        fields = ['id', 'name', 'slogan', 'avatar', 'tags', 'size', 'jobs', 'website', 'description']

class JobApplicationSerializer(serializers.ModelSerializer):
    timestamp = serializers.SerializerMethodField()
    invitation = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    company_name = serializers.CharField(source='company.name')

    def get_invitation(self, obj):
        interview = Interview.objects.get(candidate=self.context.get('request').user, job=obj)
        invitations = Invitation.objects.filter(interview=interview,
                                                candidate=self.context.get('request').user,
                                                status=interview.status)
        if invitations.count():
            return InterviewInvitationSerializer(invitations.all().first()).data
        return None

    def get_status(self, obj):
        interview = Interview.objects.get(candidate=self.context.get('request').user, job=obj)
        if interview:
            return interview.status
        return None

    def get_timestamp(self, obj):
        interview = Interview.objects.get(candidate=self.context.get('request').user, job=obj)
        if interview:
            return interview.publish_time
        return None

    class Meta:
        model = Job
        fields = ['id', 'title', 'status', 'salary_min', 'salary_max', 'salary_count', 'timestamp', 'invitation',
                  'status', 'company_name']
        
class UserResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['name', 'url']
        
class UserSerializer(serializers.ModelSerializer):
    applications = serializers.SerializerMethodField()
    resume = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True, allow_blank=True)

    def get_resume(self, obj):
        resume = Resume.objects.filter(user__uid=obj.uid, is_active=True)
        if resume.count():
            return UserResumeSerializer(resume[0]).data
        return None

    def get_applications(self, obj):
        applications = Interview.objects.filter(candidate__uid=obj.uid)
        jobs = []
        for apply in applications:
            jobs.append(apply.job)
        return JobApplicationSerializer(jobs, context=self.context, many=True).data

    class Meta:
        model = User
        fields = ['uid', 'email', 'first_name', 'last_name', 'gender', 'details', 'resume', 'applications', 'password']
        read_only_fields = ['uid', 'email', 'applications']

class CompanyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'gender']
        
        
class CompanyProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True, allow_blank=True)

    def get_user(self, obj):
        return CompanyUserSerializer(self.context.get('request').user).data

    class Meta:
        model = Company
        fields = ['name', 'slogan', 'avatar', 'tags', 'size', 'website', 'description', 'user', 'password']