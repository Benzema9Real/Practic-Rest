from .models import Deals, FavoriteDeals, Country, PaymentCondition
from rest_framework import serializers
from .models import DealsSector, Contact


class DealsSectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealsSector
        fields = '__all__'


class DealsCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class DealsPaymentConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentCondition
        fields = '__all__'


class DealsSerializer(serializers.ModelSerializer):
    economic_sectors = DealsSectorSerializer(many=True)
    location = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())
    payment_condition = serializers.PrimaryKeyRelatedField(queryset=PaymentCondition.objects.all())
    contact_email = serializers.EmailField()

    class Meta:
        model = Deals
        fields = [
            'id', 'company_name', 'delivers_self', 'economic_sectors', 'com_offer', 'product_photo',
            'video_presentation', 'website_url', 'what_do_you_offer', 'price', 'created_at', 'updated_at',
            'location', 'payment_condition', 'contact_email'
        ]
        read_only_fields = ['user']

    def create(self, validated_data):
        economic_sectors_data = validated_data.pop('economic_sectors')
        location_data = validated_data.pop('location', None)

        # Создаем основную запись для Deals
        deal = Deals.objects.create(**validated_data)

        # Устанавливаем location, если передан
        if location_data:
            deal.location = location_data
            deal.save()

        # Связываем секторы по ID
        for sector_data in economic_sectors_data:
            sector, created = DealsSector.objects.get_or_create(**sector_data)
            deal.economic_sectors.add(sector)

        return deal

class DealsAllSerializer(serializers.ModelSerializer):
    economic_sectors = DealsSectorSerializer(many=True, read_only=True)
    location = serializers.SlugRelatedField(slug_field='name_ru', read_only=True)
    payment_condition = serializers.SlugRelatedField(slug_field='name_ru', read_only=True)
    contact_email = serializers.EmailField()

    class Meta:
        model = Deals
        fields = [
            'id', 'company_name', 'delivers_self', 'economic_sectors',
            'com_offer', 'product_photo', 'video_presentation', 'website_url',
            'what_do_you_offer', 'price',
            'created_at', 'updated_at', 'location', 'payment_condition', 'contact_email'
        ]
        ref_name = 'DealsAllSerializerService'


class ContactSupplierSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    message = serializers.CharField(max_length=1000)

    class Meta:
        model = Contact
        fields = '__all__'
        ref_name = 'ContactSerializerDeals'


class FavoriteDealsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteDeals
        fields = ['deal']  # Правильное название

    def create(self, validated_data):
        favorite_deal, created = FavoriteDeals.objects.get_or_create(
            user=self.context['request'].user,
            deal=validated_data['deal']  # Правильное название
        )
        return favorite_deal
