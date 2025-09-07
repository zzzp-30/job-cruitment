from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .views import BothHttpAndHttpsSchemaGenerator
# PeekpaBackend1/urls.py


schema_view = get_schema_view(
    openapi.Info(
        title="PeekpaJob API",
        default_version='v1',
        description="这里是 PeekpaJob.com 的 API 文档。如果你有什么疑问，请联系管理员：gaoliangcode@gmail.com",
        contact=openapi.Contact(email="gaoliangcode@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    generator_class=BothHttpAndHttpsSchemaGenerator
)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/api.json/', schema_view.without_ui(cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/', include('apps.api.urls')), # 新添加的 APU urls.py 文件 
]