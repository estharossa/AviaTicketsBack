from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import CabinetUserSerializer, BankCardSerializer
from rest_framework import viewsets, status, generics
from .models import BankCard
from auth_.models import MainUser
from airflow.models import FlightOrder
from airflow.serializers import OrderInfoSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cabinet_orders(request):
    serializer = CabinetUserSerializer(request.user)
    return Response(serializer.data)


class CabinetOrdersView(generics.ListAPIView):
    queryset = MainUser.objects.all()
    serializer_class = CabinetUserSerializer

    def list(self, request, *args, **kwargs):
        serializer = CabinetUserSerializer(request.user)
        return Response(serializer.data)


class CabinetOrderDetailsView(generics.RetrieveAPIView):
    queryset = FlightOrder.objects.all()
    serializer_class = OrderInfoSerializer


class BankCardViewSet(viewsets.ModelViewSet):
    queryset = BankCard.objects.all()
    serializer_class = BankCardSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return Response("Not Authorized", status=status.HTTP_401_UNAUTHORIZED)
        cards = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(cards, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        context = {
            'user': request.user
        }
        serializer = self.get_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        card = serializer.save()
        return Response(self.get_serializer(card).data)
