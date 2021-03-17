from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from jobs.models import Advert
from jobs.serializers import AdvertSerializer


class AdvertListView(APIView):
    def get(self, request):
        adverts = Advert.objects.only_moderated()
        s = AdvertSerializer(adverts, many=True)
        return Response(data=s.data, status=status.HTTP_200_OK)
