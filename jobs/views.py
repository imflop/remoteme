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


class AdvertDetailView(APIView):
    def get(self, request, uuid):
        if uuid:
            advert = Advert.objects.filter(uuid=uuid).first()
            s = AdvertSerializer(advert, many=False)
            return Response(data=s.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
