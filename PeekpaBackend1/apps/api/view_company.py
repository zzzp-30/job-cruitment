from django_filters import rest_framework as filters
from apps.company.models import Company
from django.db.models import Q, Count
from urllib.parse import unquote


class CompanyListFilter(filters.FilterSet):
    q = filters.CharFilter(method='my_custom_filter', label="Search")
    order = filters.CharFilter(method='order_search', label="Order")
    tag = filters.CharFilter(method='tag_search', label="Tag")
    size = filters.CharFilter(method='size_search', label="Size")

    class Meta:
        model = Company
        fields = ['q']

    # 自定义搜索
    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(
            Q(name__contains=value)
        )

    # 公司标签
    def tag_search(self, queryset, name, value):
        decoded_data = unquote(value)
        if value:
            return queryset.filter(tags__contains=decoded_data)
        return queryset

    # 公司规模
    def size_search(self, queryset, name, value):
        decoded_data = unquote(value)
        if value:
            return queryset.filter(size=decoded_data)
        return queryset

    # 按照职位发布数量排序
    def order_search(self, queryset, name, value):
        if value == 'job':
            return queryset.annotate(job_count=Count('jobs')).order_by('-job_count')
        return queryset
    
from rest_framework import generics
from apps.api.serializers import CompanyListSerializer
from django_filters.rest_framework import DjangoFilterBackend

class CompanyListView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CompanyListFilter

from apps.api.serializers import CompanySerializer

class CompanyDetailView(generics.RetrieveAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = 'id'