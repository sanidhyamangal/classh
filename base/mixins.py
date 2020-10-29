"""
Author: Sanidhya Mangal, Ravinder Singh
github:sanidhyamangal
email: sanidhya.mangal@engineerbabu
"""

from rest_framework import status
from rest_framework.response import Response


class GetQuerySetMixin:
    def get_queryset(self):
        return self.model_class.objects.all()


# mixin class for List APIView
class BaseAPIViewListMixin:
    """
    Mixin Class for Performing List Ops
    """
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(
            data={
                "status": True,
                "message":
                f"{self.instance_name}s list reterieved sucessfully",
                "data": serializer.data
            })


class BaseAPIViewCreateMixin:
    """
    Mixin class for create op
    """
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={
                "status": True,
                "message": f"{self.instance_name} created sucessfully",
                "data": serializer.data
            },
                            status=status.HTTP_201_CREATED)

        return Response(data={
            "status": False,
            "message": serializer.data,
            "data": {}
        },
                        status=status.HTTP_400_BAD_REQUEST)


class ReterieveAPIViewMixin:
    """
    Mixin class for performing reterieve op
    """
    def get(self, request, pk=None, format=None):
        obj = self.get_object()
        serializer = self.serializer_class(obj)
        return Response(
            data={
                "status": True,
                "message": f"{self.instance_name} reterived successfully",
                "data": serializer.data
            })


class UpdateAPIViewMixin:
    """
    Mixin class for performing update op
    """
    def put(self, request, pk=None, format=None):
        obj = self.get_object()
        serializer = self.serializer_class(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={
                    "status": True,
                    "message": f"{self.instance_name} updated successfully",
                    "data": serializer.data
                })
        return Response(data={
            "status": False,
            "message": f"{self.instance_name} update failed",
            "data": serializer.errors
        },
                        status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None, format=None):
        obj = self.get_object()
        serializer = self.serializer_class(obj,
                                           data=request.data,
                                           partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={
                    "status": True,
                    "message": f"{self.instance_name} updated successfully",
                    "data": serializer.data
                })
        return Response(data={
            "status": False,
            "message": f"{self.instance_name} update failed",
            "data": serializer.errors
        },
                        status=status.HTTP_400_BAD_REQUEST)


class DestroyAPIViewMixin:
    """
    Mixin class for performing Delete op
    """
    def delete(self, request, pk=None, format=None):
        obj = self.get_object()
        obj.delete()
        return Response(data={
            "status": True,
            "message": f"{self.instance_name} deleted successfully",
            "data": {}
        },
                        status=status.HTTP_200_OK)


class ReadWriteSerializerMixin:
    """
    Overrides get_serializer_class to choose the read serializer
    for GET requests and the write serializer for POST requests.

    Set read_serializer_class and write_serializer_class attributes on a
    viewset.
    """

    read_serializer_class = None
    write_serializer_class = None

    def get_serializer_class(self):
        """
        Method to get serializer
        """
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return self.get_write_serializer_class()
        return self.get_read_serializer_class()

    def get_read_serializer_class(self):
        assert self.read_serializer_class is not None, (
            "'%s' should either include `read_serializer_class` attribute"
            "or override `get_read_serializer_class()` method." %
            self.__class__.__name__)

        return self.read_serializer_class

    def get_write_serializer_class(self):
        assert self.write_serializer_class is not None, (
            "'%s' should either include `write_serializer_class` attribute"
            "or override `get_write_serializer_class()` method." %
            self.__class__.__name__)

        return self.write_serializer_class
