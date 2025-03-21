from rest_framework import serializers
from .models import Organization , OwnershipStructure

class OrganizationSerializer(serializers.ModelSerializer):
    # These fields will return human-readable values
    industry_display = serializers.SerializerMethodField()
    geo_scope_display = serializers.SerializerMethodField()
    governance_display = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = '__all__'  # You can list fields explicitly if needed

    def get_industry_display(self, obj):
        # If you want to show the nace_code or description
        return obj.industry.nace_code if obj.industry else ''

    def get_geo_scope_display(self, obj):
        return obj.get_geo_scope_display() if obj.geo_scope else ''

    def get_governance_display(self, obj):
        return obj.get_governance_display() if obj.governance else ''



class OwnershipStructureSerializer(serializers.ModelSerializer):
    """
    Serializer for OwnershipStructure model.
    """
    class Meta:
        model = OwnershipStructure
        fields = ['id', 'name']




        