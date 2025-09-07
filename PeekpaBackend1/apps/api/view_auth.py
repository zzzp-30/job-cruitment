from rest_framework.response import Response
from django.contrib import auth
from django.contrib.auth.models import update_last_login
from rest_framework import generics, status
from apps.peekpauser.models import User
from apps.api.serializers import LoginSerializer
from apps.api.serializers import LoginSerializer, RegisterUserSerializer
from django_filters.rest_framework import DjangoFilterBackend


class RegisterUserView(generics.GenericAPIView):
    serializer_class = RegisterUserSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response(LoginSerializer(user).data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LoginBaseView(generics.GenericAPIView):

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = self.queryset.filter(email=email)
        # 用户不存在
        if not user.count():
            return Response(status=status.HTTP_404_NOT_FOUND)
        # 系统登录用户
        auth_user = auth.authenticate(email=email, password=password, is_active=True)
        if auth_user:
            # 更新用户最后登录时间
            update_last_login(None, auth_user)
            return Response(self.get_serializer(auth_user).data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class LoginView(LoginBaseView):
    serializer_class = LoginSerializer
    queryset = User.objects.filter(is_staff=False)

class LoginAdminView(LoginBaseView):
    serializer_class = LoginSerializer
    queryset = User.objects.filter(is_staff=True)

    
from django_filters import rest_framework as filters
from django.db.models import Q

class UserListFilter(filters.FilterSet):
    q = filters.CharFilter(method='my_custom_filter', label="Search")

    class Meta:
        model = User
        fields = ['q']

    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(
            Q(first_name__contains=value) | Q(last_name__contains=value) | Q(email__contains=value)
        )
from apps.api.permissions import IsCompanyAdminUser

from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.api.serializers import AdminUserListSerializer

class UserAdminView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = AdminUserListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserListFilter
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCompanyAdminUser]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        company_id = self.request.user.details.get('company_id', -1)
        queryset = queryset.filter(details__contains={'company_id': company_id}).exclude(uid=self.request.user.uid)
        return queryset

    def perform_create(self, serializer):
        password = self.request.data.get('password')
        user = serializer.save()
        company_id = self.request.user.details.get('company_id')
        details = {
            'company_id': company_id,
            'is_manager': False
        }
        user.details = details
        user.is_staff = True
        user.set_password(password)
        user.save()
from rest_framework.generics import get_object_or_404

class UserAdminDetailView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = AdminUserListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCompanyAdminUser]
    lookup_field = 'uid'

    def get_object(self):
        queryset = super().get_queryset()
        company_id = self.request.user.details.get('company_id', -1)
        queryset = queryset.filter(
            Q(details__contains={'company_id': company_id}))
        uid = self.kwargs['uid']
        obj = get_object_or_404(queryset, uid=uid)
        return obj

    def put(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


from apps.company.models import Company
from apps.api.permissions import IsSuperUser
from apps.api.serializers import AdminCompanyListSerializer

class CompanyListFilter(filters.FilterSet):
    q = filters.CharFilter(method='my_custom_filter', label="Search")

    class Meta:
        model = Company
        fields = ['q']

    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(name__contains=value)
class CompanyAdminView(generics.ListCreateAPIView):
    queryset = Company.objects.all().order_by('-id')
    serializer_class = AdminCompanyListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CompanyListFilter
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperUser]
    
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validata_data = serializer.validated_data

        # 创建公司
        name = validata_data.get('name')
        website = validata_data.get('website')
        company = Company.objects.create(name=name, website=website)

        # 创建公司经理
        password = validata_data.get('password')
        first_name = validata_data.get('first_name')
        last_name = validata_data.get('last_name')
        email = validata_data.get('email')
        details = {"company_id": company.id, "is_manager": True}
        user = User.objects.create(email=email, first_name=first_name, last_name=last_name, details=details, is_staff=True)
        user.set_password(password)
        user.save()
        return Response(status=status.HTTP_201_CREATED)
    
from apps.api.serializers import UserSerializer
from rest_framework import permissions
from rest_framework.exceptions import NotFound

class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.filter(is_staff=False)
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = get_object_or_404(self.queryset, uid=self.request.user.uid)
        return user


    def put(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


    def patch(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if serializer.validated_data.get('password'):
            instance.set_password(serializer.validated_data.get('password'))
            instance.save()
        return Response(serializer.data)
    
import uuid
from apps.api.serializers import CompanyProfileSerializer
from apps.peekpauser.models import Avatar
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

class CompanyProfileView(generics.RetrieveUpdateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        company_id = self.request.user.details.get('company_id', -1)
        company = get_object_or_404(self.queryset, id=company_id)
        return company

    def put(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def patch(self, request, *args, **kwargs):
        company = self.get_object()
        # 修改密码
        if 'password' in request.data and request.data.get('password'):
            request.user.set_password(request.data.get('password'))
            request.user.save()
        if request.user.details.get('is_manager', False):
            # 更新公司头像
            if 'avatar_file' in request.data:
                file = request.data.get('avatar_file')
                old_avatars = Avatar.objects.filter(user=self.request.user)
                if old_avatars.count():
                    if old_avatars.count():
                        # 删除旧的 Avatar 对象及其关联的文件
                        for old_avatar in old_avatars:
                            default_storage.delete(old_avatar.url[6:])
                        old_avatars.delete()
                file_name = file.name
                file_path = f'avatar/{".".join(file_name.split(".")[:-1])}_{str(uuid.uuid4())[:8]}.{file_name.split(".")[-1]}'
                saved_path = default_storage.save(file_path, ContentFile(file.read()))
                avatar = Avatar.objects.create(name=file_name, user=self.request.user, url='media/{}'.format(saved_path))
                company.avatar = avatar.url
            company.slogan = request.data.get('slogan', company.slogan)
            company.size = request.data.get('size', company.size)
            company.description = request.data.get('description', company.description)
            company.tags = request.data.get('tags', company.tags)
            company.save()
        serializer = self.get_serializer(company)
        return Response(data=serializer.data)