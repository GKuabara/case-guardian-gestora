from rest_framework import serializers
from .models import Contract, Parcel

class ParcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcel
        fields = '__all__'
        read_only_fields = ['contract_id', 'parcel_number']  # Auto-incremented, read-only

class ContractSerializer(serializers.ModelSerializer):
    parcels = ParcelSerializer(many=True, required=False)

    class Meta:
        model = Contract
        fields = '__all__'
        read_only_fields = ['contract_id']  # Auto-incremented, read-only

    def create(self, validated_data):
        parcels_data = validated_data.pop('parcels', [])
        contract = Contract.objects.create(**validated_data)
        for i, parcel_data in enumerate(parcels_data):
            Parcel.objects.create(contract_id=contract, parcel_number=i+1, **parcel_data)
        return contract
