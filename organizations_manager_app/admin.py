from django.contrib import admin
from .models import (
    Industry, OwnershipStructure, Location, FundingInformation, 
    TokenInformation, Organization, SocialLinks, ContactInformation
)

@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ('nace_code', 'description')
    search_fields = ('nace_code', 'description')

@admin.register(OwnershipStructure)
class OwnershipStructureAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('address', 'city', 'state_region', 'country', 'zip_postal_code')
    search_fields = ('city', 'country')

@admin.register(FundingInformation)
class FundingInformationAdmin(admin.ModelAdmin):
    list_display = ('revenue', 'sources')

@admin.register(TokenInformation)
class TokenInformationAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'blockchain', 'governance', 'contract')
    search_fields = ('name', 'symbol')

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'legal_structure', 'size', 'geo_scope', 'members', 'year_founded')
    search_fields = ('name', 'type', 'legal_structure')
    list_filter = ('type', 'legal_structure', 'size', 'geo_scope')
    filter_horizontal = ('ownership_structures',)

@admin.register(SocialLinks)
class SocialLinksAdmin(admin.ModelAdmin):
    list_display = ('website', 'twitter', 'linkedin', 'discord', 'github', 'other')

@admin.register(ContactInformation)
class ContactInformationAdmin(admin.ModelAdmin):
    list_display = ('person', 'email', 'phone')