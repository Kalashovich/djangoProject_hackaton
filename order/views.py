from rest_framework import views
from order import serializers
from rest_framework.response import Response
from rest_framework import permissions


class OrderApiView(views.APIView):

    def post(self, request):
        permission_classes = [permissions.IsAuthenticated]
        serializer = serializers.OrderSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data)

