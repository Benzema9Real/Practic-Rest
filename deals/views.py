from rest_framework import generics, status, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import DealsSerializer, DealsAllSerializer, FavoriteDealsSerializer, DealsSectorSerializer, \
    DealsCountrySerializer, DealsPaymentConditionSerializer
from .models import Deals, FavoriteDeals, DealsSector, Country, PaymentCondition
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import UntypedToken
from .serializers import ContactSupplierSerializer
from django.core.mail import send_mail


class DealsSectorListView(generics.ListAPIView):
    queryset = DealsSector.objects.all()
    serializer_class = DealsSectorSerializer
    permission_classes = [AllowAny]


class DealsPaymentConditionListView(generics.ListAPIView):
    queryset = PaymentCondition.objects.all()  # Измените queryset на PaymentCondition
    serializer_class = DealsPaymentConditionSerializer
    permission_classes = [AllowAny]


class DealsCountryListView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = DealsCountrySerializer
    authentication_classes = []
    permission_classes = [AllowAny]


class DealsCreateView(generics.CreateAPIView):
    queryset = Deals.objects.all()
    serializer_class = DealsSerializer
    permission_classes = [IsAuthenticated]


    def create(self, request, *args, **kwargs):
        # Проверка токена
        token = request.headers.get('Authorization', '').split(' ')[-1]
        if not token:
            return Response({"detail": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Проверка токена
            UntypedToken(token)
            user = JWTAuthentication().get_user(JWTAuthentication().get_validated_token(token))
        except Exception as e:
            return Response({"detail": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)

        # Создание сделки
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Сохраняем сделку с привязкой к текущему пользователю
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DealsDetailUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Deals.objects.all()
    serializer_class = DealsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Deals.objects.filter(user=self.request.user)


class DealsDetailView(generics.RetrieveAPIView):
    queryset = Deals.objects.all()
    serializer_class = DealsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Deals.objects.filter(user=self.request.user)


class DealsDetailAllView(generics.RetrieveAPIView):
    serializer_class = DealsAllSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Deals.objects.filter(activate=True)  # Возвращает только активные сделки

    def get_object(self):
        queryset = self.get_queryset()
        filter_kwargs = {'pk': self.kwargs['pk']}
        obj = generics.get_object_or_404(queryset, **filter_kwargs)
        return obj

    def get_queryset(self):
        return Deals.objects.filter(activate=True)


class AddFavoriteDealsView(APIView):
    permission_classes = []
    authentication_classes = [JWTAuthentication]

    def post(self, request, pk):
        # Проверка токена
        token = request.headers.get('Authorization', '').split(' ')[-1]
        if not token:
            return Response({"detail": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Проверка токена
            UntypedToken(token)
            user = JWTAuthentication().get_user(JWTAuthentication().get_validated_token(token))
        except Exception as e:
            return Response({"detail": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)

        # Проверяем, существует ли сделка
        try:
            deal = Deals.objects.get(pk=pk)
        except Deals.DoesNotExist:
            return Response({"error": "Сделка не найдена."}, status=status.HTTP_404_NOT_FOUND)

        # Проверяем, уже ли сделка в избранном
        if FavoriteDeals.objects.filter(user=user, deal=deal).exists():
            return Response({"error": "Сделка уже в избранном."}, status=status.HTTP_400_BAD_REQUEST)

        # Добавляем в избранное
        FavoriteDeals.objects.create(user=user, deal=deal)
        return Response({"success": "Сделка добавлена в избранное."}, status=status.HTTP_201_CREATED)


class RemoveFavoriteDealsView(APIView):
    permission_classes = []
    authentication_classes = [JWTAuthentication]

    def delete(self, request, pk):
        # Проверка токена
        token = request.headers.get('Authorization', '').split(' ')[-1]
        if not token:
            return Response({"detail": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Проверка токена
            UntypedToken(token)
            user = JWTAuthentication().get_user(JWTAuthentication().get_validated_token(token))
        except Exception as e:
            return Response({"detail": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)

        # Поиск и удаление сделки из избранного
        try:
            favorite_deal = FavoriteDeals.objects.get(user=user, deal_id=pk)
            favorite_deal.delete()
            return Response({"success": "Сделка удалена из избранного."}, status=status.HTTP_204_NO_CONTENT)
        except FavoriteDeals.DoesNotExist:
            return Response({"error": "Сделка не найдена в избранном."}, status=status.HTTP_404_NOT_FOUND)


class FavoriteDealsListView(generics.ListAPIView):
    serializer_class = DealsAllSerializer
    permission_classes = []
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        # Проверка токена
        token = self.request.headers.get('Authorization', '').split(' ')[-1]
        if not token:
            return Deals.objects.none()

        try:
            # Проверка токена
            UntypedToken(token)
            user = JWTAuthentication().get_user(JWTAuthentication().get_validated_token(token))
        except Exception as e:
            return Deals.objects.none()

        # Возвращаем сделки, добавленные в избранное текущим пользователем
        return Deals.objects.filter(favorited_by_deals__user=user, activate=True)


class UserDealsListView(generics.ListAPIView):
    serializer_class = DealsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Deals.objects.filter(user=self.request.user, activate=True)


class DealsListView(generics.ListAPIView):
    queryset = Deals.objects.filter(activate=True)
    serializer_class = DealsAllSerializer
    permission_classes = [AllowAny]


class ContactSupplierView(APIView):
    serializer_class = ContactSupplierSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            deal = Deals.objects.get(pk=pk, activate=True)  # Фильтрация активных сделок
        except Deals.DoesNotExist:
            return Response({"error": "Сделка не найдена или не активна."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            email = serializer.validated_data['email']
            message = serializer.validated_data['message']

            subject = f"Новый запрос по вашей сделке: {deal.company_name}"
            full_message = f"Вы получили новый запрос от {name} ({email}):\n\n{message}"

            # Отправка почты владельцу сделки (например, по email, который можно добавить в модель Deals)
            send_mail(subject, full_message, email,
                      ['owner_email@example.com'])  # Замените на реальный email владельца сделки

            return Response({"success": "Сообщение успешно отправлено."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
