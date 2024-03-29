from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from redirects.models import LiveRedirect
from redirects.serializers import LiveRedirectSerializer

from django.http import Http404

class RedirectList(APIView):
    """
    GET all LiveRedirects or POST a new one
    """
    permission_classes = (IsAdminUser,)


    def get(self,request,format=None):
        redirects = LiveRedirect.objects.all()
        serializer = LiveRedirectSerializer(redirects)
        return Response(serializer.data)

class RedirectDetails(APIView):
    """
    GET a specific LiveRedirect
    """

    def get(self,request,slug=None,format=None):

        try:
            request = LiveRedirect.objects.get(slug=slug)
        except LiveRedirect.DoesNotExist:
            raise Http404

        serializer = LiveRedirectSerializer(request)
        return Response(serializer.data)

    def post(self,request,slug=None,format=None):

        if slug:
            return Response({'error':'Cannot POST new redirect if url has slug!'},status=status.HTTP_400_BAD_REQUEST)

        serializer = LiveRedirectSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)