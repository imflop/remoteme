from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from jobs.selectors import get_advert, get_adverts, get_scope, get_stack
from jobs.serializers import (AdvertCreateSerializer, AdvertDetailSerializer,
                              AdvertSerializer, ScopeSerializer,
                              StackSerializer, AdvertFilterSerializer)
from jobs.services import create_advert
from utils.mixins import ApiErrorsMixin
from utils.pagination import LimitOffsetPagination, get_paginated_response


class ScopeListView(APIView):
    """
    Scopes
    """

    def get(self, request) -> Response:
        scopes = get_scope()
        serializer = ScopeSerializer(scopes, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class StackListView(APIView):
    """
    Stack
    """

    def get(self, request) -> Response:
        stack = get_stack()
        serializer = StackSerializer(stack, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class AdvertPagination(LimitOffsetPagination):
    default_limit = 10


class AdvertListView(APIView):
    """
    Adverts
    """

    def get(self, request):
        filter_serializer = AdvertFilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        adverts = get_adverts(filters=filter_serializer.validated_data)

        return get_paginated_response(
            pagination_class=AdvertPagination,
            serializer_class=AdvertSerializer,
            queryset=adverts,
            request=request,
            view=self,
        )


class AdvertDetailView(APIView):
    """
    Single advert by requested params
    """

    def get(self, request, uuid) -> Response:
        if uuid:
            advert = get_advert(fetched_by=uuid)
            serializer = AdvertDetailSerializer(advert, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AdvertCreateView(ApiErrorsMixin, APIView):
    """
    Create advert from form
    """

    def post(self, request) -> Response:
        serializer = AdvertCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        create_advert(serializer.validated_data)

        return Response(status.HTTP_201_CREATED)
