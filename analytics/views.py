from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from analytics.models import Analytics
from analytics.serializers import AnalyticsSerializer
from utilities.http_code_handler import response_formatter


class AnalyticsAPI(APIView):
    """
    Analytics API
    """
    queryset = Analytics.objects.all()
    serializer_class = AnalyticsSerializer

    def get_queryset(self):
        """
        Filter query set base on user and code
        :return:
        """
        try:
            short_code = self.request.query_params.get("url").split("/")[-2]
        except Exception as e:
            short_code = ""

        return self.queryset.filter(
            shortener__user=self.request.user,
            shortener__short_code=short_code
        )

    def get(self, request):
        """
        Get analytics info
        :param request:
        :return:
        """
        return Response(
            data=response_formatter(
                status.HTTP_200_OK,
                self.serializer_class(self.get_queryset(), many=True, context={"request": self.request}).data
            ),
            status=status.HTTP_200_OK
        )
