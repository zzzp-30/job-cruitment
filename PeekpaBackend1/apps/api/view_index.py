from django.db.models import Count
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.serializers import JobListSerializer, CompanyListSerializer
from apps.company.models import Company
from apps.job.models import Job


class IndexView(APIView):

    def get(self, request):
        content = {}
        category = [
            {
                "title": "技术",
                "param": "q",
                "filters": [
                    {
                        "name": "Java",
                        "param": "java"
                    },
                    {
                        "name": "PHP",
                        "param": "php"
                    },
                    {
                        "name": "C++",
                        "param": "c++"
                    },
                    {
                        "name": "区块链",
                        "param": "区块链"
                    },
                    {
                        "name": "Android",
                        "param": "android"
                    },
                    {
                        "name": "iOS",
                        "param": "ios"
                    }
                ]
            },
            {
                "title": "产品",
                "param": "q",
                "filters": [
                    {
                        "name": "产品总监",
                        "param": "产品总监"
                    },
                    {
                        "name": "产品经理",
                        "param": "产品经理"
                    },
                    {
                        "name": "数据产品经理",
                        "param": "数据产品经理"
                    },
                    {
                        "name": "游戏策划",
                        "param": "游戏策划"
                    }
                ]
            },
            {
                "title": "设计",
                "param": "q",
                "filters": [
                    {
                        "name": "UI设计师",
                        "param": "UI设计师"
                    },
                    {
                        "name": "交互设计",
                        "param": "交互设计"
                    },
                    {
                        "name": "网页设计师",
                        "param": "网页设计师"
                    },
                    {
                        "name": "平面设计师",
                        "param": "平面设计师"
                    }
                ]
            },
            {
                "title": "运营",
                "param": "q",
                "filters": [
                    {
                        "name": "新媒体运营",
                        "param": "新媒体运营"
                    },
                    {
                        "name": "编辑",
                        "param": "编辑"
                    },
                    {
                        "name": "数据运营",
                        "param": "数据运营"
                    },
                    {
                        "name": "运营总监",
                        "param": "运营总监"
                    },
                    {
                        "name": "COO",
                        "param": "COO"
                    }
                ]
            },
            {
                "title": "市场",
                "param": "q",
                "filters": [
                    {
                        "name": "市场营销",
                        "param": "市场营销"
                    },
                    {
                        "name": "市场推广",
                        "param": "市场推广"
                    },
                    {
                        "name": "市场策划",
                        "param": "市场策划"
                    },
                    {
                        "name": "政府关系",
                        "param": "政府关系"
                    }
                ]
            },
            {
                "title": "销售",
                "param": "q",
                "filters": [
                    {
                        "name": "销售专员",
                        "param": "销售专员"
                    },
                    {
                        "name": "销售经理",
                        "param": "销售经理"
                    },
                    {
                        "name": "销售总监",
                        "param": "销售总监"
                    },
                    {
                        "name": "大客户代表",
                        "param": "大客户代表"
                    }
                ]
            },
            {
                "title": "职能",
                "param": "q",
                "filters": [
                    {
                        "name": "HR",
                        "param": "HR"
                    },
                    {
                        "name": "行政",
                        "param": "行政"
                    },
                    {
                        "name": "财务",
                        "param": "财务"
                    },
                    {
                        "name": "审计",
                        "param": "审计"
                    }
                ]
            },
            {
                "title": "游戏",
                "param": "q",
                "filters": [
                    {
                        "name": "小游戏开发",
                        "param": "小游戏开发"
                    },
                    {
                        "name": "U3D",
                        "param": "U3D"
                    },
                    {
                        "name": "游戏策划",
                        "param": "游戏策划"
                    },
                    {
                        "name": "游戏运营",
                        "param": "游戏运营"
                    }
                ]
            },
        ]
        banner = [
            {
                "img_url": "/banner1.png",
                "link_url": "/#/jobs/?q=123"
            },
            {
                "img_url": "/banner2.png",
                "link_url": "/#/companies/?q=乐视"
            },
            {
                "img_url": "/banner3.jpeg",
                "link_url": "/#/jobs/?q=vue"
            },
            {
                "img_url": "/banner4.png",
                "link_url": "/#/companies/?q=乐视"
            },
        ]
        recommend_jobs = [
            {
                "name": "为你匹配",
                "data_list": JobListSerializer(Job.objects.filter(status=Job.STATUS_PUBLISH).order_by('?')[:12],
                                               many=True).data
            },
            {
                "name": "24Hour热门",
                "data_list": JobListSerializer(Job.objects.filter(status=Job.STATUS_PUBLISH).order_by('?')[:12],
                                               many=True).data
            },
            {
                "name": "最新职位",
                "data_list": JobListSerializer(
                    Job.objects.filter(status=Job.STATUS_PUBLISH).order_by('-publish_time')[:12], many=True).data
            },
        ]
        recommend_companies = [
            {
                "name": "互联网热门公司排行",
                "data_list": CompanyListSerializer(
                    Company.objects.annotate(interview_count=Count('jobs__interviews')).order_by('-interview_count')[
                    :12], many=True).data
            },
            {
                "name": "全球500强公司",
                "data_list": CompanyListSerializer(Company.objects.all().order_by('?')[:12], many=True).data
            },
            {
                "name": "新进独角兽",
                "data_list": CompanyListSerializer(Company.objects.all().order_by('?')[:12], many=True).data
            }
        ]
        content['category'] = category
        content['banner'] = banner
        content['recommend_jobs'] = recommend_jobs
        content['recommend_companies'] = recommend_companies
        return Response(content, status=status.HTTP_200_OK)