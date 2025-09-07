from django.urls import path
from apps.api.view_auth import LoginView
from apps.api.view_auth import LoginView, LoginAdminView, RegisterUserView, UserAdminView
from apps.api.view_job import ResumeView
from apps.api.view_job import ResumeView, AvatarView
from apps.api.view_auth import UserAdminDetailView
from apps.api.view_auth import CompanyAdminView
from apps.api.view_manage import ManageJobListView
from apps.api.view_manage import ManageJobNameListView
from apps.api.view_manage import ManageJobDetailView
from apps.api.view_manage import ManageInterviewListView
from apps.api.view_manage import ManageInterviewDetailView
from apps.api.view_manage import ManageInvitationView
from apps.api.view_manage import ManageInvitationDetailView
from apps.api.view_manage import DashboardView
from apps.api.view_job import JobListView
from apps.api.view_job import JobDetailView
from apps.api.view_job import InvitationDetailView
from apps.api.view_job import ApplyJobView
from apps.api.view_company import CompanyListView
from apps.api.view_company import CompanyDetailView
from apps.api.view_index import IndexView
from apps.api.view_auth import ProfileView
from apps.api.view_auth import CompanyProfileView

urlpatterns = [
    path("auth/signin/", LoginView.as_view(), name='signin_view'),
    path("auth/signup/", RegisterUserView.as_view(), name="signup"),  # 新添加的求职者注册接口
    path("auth/login/", LoginAdminView.as_view(), name="login_admin"),  
    path("manage/user/", UserAdminView.as_view(), name="user_admin"), 
    path("resume/upload/", ResumeView.as_view(), name='resume_upload'), # 简历上传接口
    path("avatar/upload/", AvatarView.as_view(), name='avatar_upload'),
    path("manage/user/<str:uid>/", UserAdminDetailView.as_view(), name="user_admin_detail"), 
    path("manage/company/", CompanyAdminView.as_view(), name="company_admin"), 
    path("manage/job/", ManageJobListView.as_view(), name='manage_job_list_view'), 
    path("manage/job/list/", ManageJobNameListView.as_view(), name='manage_job_namelist_view'),
    path("manage/job/<str:id>/", ManageJobDetailView.as_view(), name='manage_job_detail_view'), path("manage/job/<str:id>/", ManageJobDetailView.as_view(), name='manage_job_detail_view'), 
    path("manage/job/<str:id>/interviews/", ManageInterviewListView.as_view(), name='manage_job_interview_list_view'),
    path("manage/job/<str:id>/interviews/<str:iid>/", ManageInterviewDetailView.as_view(), name='manage_job_interview_detail_view'), 
    path("manage/job/<str:id>/interviews/<str:iid>/invitation/", ManageInvitationView.as_view(), name='manage_job_interview_invitation_view'),
    path("manage/job/<str:id>/interviews/<str:iid>/invitation/<str:ivid>/", ManageInvitationDetailView.as_view(), name='manage_job_interview_invitation_detail_view'),
    path("manage/dashboard/", DashboardView.as_view(), name='dashboard'),
    path("job/", JobListView.as_view(), name='job_list'), # 前端职位列表接口
    path("job/<str:id>/", JobDetailView.as_view(), name='job_detail'), # 前端职位详情接口
    path("invitation/<str:iid>/", InvitationDetailView.as_view(), name='invitation_detail'),
    path("job/<str:id>/apply/", ApplyJobView.as_view(), name='job_apply'),
    path("company/", CompanyListView.as_view(), name='company_list'), # 公司列表接口
    path("company/<str:id>/", CompanyDetailView.as_view(), name='company_detail'),# 公司详情接口
    path("index/", IndexView.as_view(), name='index'), # 首页接口
    path("profile/", ProfileView.as_view(), name="profile_user"), # 个人信息修改接口
    path("manage/setting/", CompanyProfileView.as_view(), name="company_profile_user"),
]

app_name = "api"


