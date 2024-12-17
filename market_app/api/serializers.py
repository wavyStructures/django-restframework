from rest_framework import serializers
from market_app.models import Market, Seller

class MarketSerializer(serializers.Serializer):
  id = serializers.IntegerField(read_only=True)
  name = serializers.CharField(max_length=255)
  location = serializers.CharField(max_length=255)
  description = serializers.CharField()
  net_worth = serializers.DecimalField(max_digits=100, decimal_places=2)
  
    def create(self, validated_data):
        return Market.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.location = validated_data.get('location', instance.location)
        instance.description = validated_data.get('description', instance.description)
        instance.net_worth = validated_data.get('net_worth', instance.net_worth)
        instance.save()
        return instance     
    
    def validate_location(self, value):
        if 'X' in value:
            raise serializers.ValidationError("Location cannot contain X")
        return value
 
class SellerDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField()
    markets = MarketSerializer(many=True, read_only=True)
    
class SellerCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField()
    markets = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    def validate_markets(self, value):
        markets = Market.objects.filter(id__in=value)
        if (markets) != len(value):
            raise serializers.ValidationError("one or more markets not found")
        return value
  
    
    def create(self, validated_data):
        market_ids = validated_data.pop('markets')
         seller = Seller.objects.create(**validated_data)
         
    #     for market_data in markets_data:
    #         Market.objects.create(seller=seller, **market_data)
    #     return seller
    
    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.contact_info = validated_data.get('contact_info', instance.contact_info)
    #     instance.save()
    #     markets = validated_data.get('markets')
    #     for market in markets:
    #         market_id = market.get('id', None)
    #         if market_id:
    #             market_instance = Market.objects.get(id=market_id)
    #             market_instance.name = market.get('name', market_instance.name)
    #             market_instance.location = market.get('location', market_instance.location)
    #             market_instance.description = market.get('description', market_instance.description)
    #             market_instance.net_worth = market.get('net_worth', market_instance.net_worth)
    #             market_instance.save()
    #         else:
    #             Market.objects.create(seller=instance, **market)
    #     return instance
    
    # def validate_name(self, value):
    #     if 'X' in value:
    #         raise serializers.ValidationError("Name cannot contain X")
    #     return value
    
    # def validate_contact_info(self, value):
    #     if 'X' in value:
    #         raise serializers.ValidationError("Contact info cannot contain X")
    #     return value
    
    # def validate_markets(self, value):
    #     if len(value) < 1:
    #         raise serializers.ValidationError("Seller must have at least one market")
    #     return value