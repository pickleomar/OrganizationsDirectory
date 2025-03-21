from django.db import models
from django.core.validators import MaxLengthValidator
import uuid

class OrganizationType(models.TextChoices):
    COOPERATIVE = 'cooperative', 'Cooperative'
    EMPLOYEE_OWNED = 'employee_owned', 'Employee-Owned'
    DAO = 'dao', 'DAO'
    CRYPTO_WEB3 = 'crypto_web3', 'Crypto/Web3'
    ESOP = 'esop', 'ESOP'
    PLATFORM_COOP = 'platform_coop', 'Platform Cooperative'
    COMMUNITY_TRUST = 'community_trust', 'Community Trust'
    HYBRID = 'hybrid', 'Hybrid'
    OTHER = 'other', 'Other'

class GeographicalScope(models.TextChoices):
    LOCAL = 'local', 'Local'
    REGIONAL = 'regional', 'Regional'
    NATIONAL = 'national', 'National'
    GLOBAL = 'global', 'Global'
    VIRTUAL = 'virtual', 'Virtual'

class OrganizationSize(models.TextChoices):
    MICRO = 'micro', 'Micro'
    SMALL = 'small', 'Small'
    MEDIUM = 'medium', 'Medium'
    LARGE = 'large', 'Large'

class LegalStructure(models.TextChoices):
    LLC = 'llc', 'LLC'
    CORPORATION = 'corporation', 'Corporation'
    COOPERATIVE = 'cooperative', 'Cooperative'
    DAO = 'dao', 'DAO'
    FOUNDATION = 'foundation', 'Foundation'
    TRUST = 'trust', 'Trust'
    NONPROFIT = 'nonprofit', 'Nonprofit'
    HYBRID = 'hybrid', 'Hybrid'
    OTHER = 'other', 'Other'

class GovernanceModel(models.TextChoices):
    DIRECT = 'direct', 'Direct Democracy'
    REPRESENTATIVE = 'representative', 'Representative Democracy'
    TOKEN = 'token', 'Token-Based'
    HYBRID = 'hybrid', 'Hybrid'
    BOARD = 'board', 'Board'
    SOCIOCRATIC = 'sociocratic', 'Sociocratic'
    OTHER = 'other', 'Other'

class Industry(models.Model):
    nace_code = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.nace_code

class OwnershipStructure(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Location(models.Model):
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state_region = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    zip_postal_code = models.CharField(max_length=20, blank=True)

class FundingInformation(models.Model):
    sources = models.JSONField(default=list)
    revenue = models.CharField(max_length=50, blank=True)

class TokenInformation(models.Model):
    name = models.CharField(max_length=100, blank=True)
    symbol = models.CharField(max_length=20, blank=True)
    blockchain = models.CharField(max_length=50, blank=True)
    governance = models.CharField(max_length=100, blank=True)
    contract = models.URLField(blank=True)

class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(validators=[MaxLengthValidator(2000)], blank=True)
    type = models.CharField(max_length=50, choices=OrganizationType.choices)
    industry = models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True, blank=True)
    ownership_structures = models.ManyToManyField(OwnershipStructure)
    legal_structure = models.CharField(max_length=50, choices=LegalStructure.choices)
    year_founded = models.IntegerField(null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    geo_scope = models.CharField(max_length=50, choices=GeographicalScope.choices)
    size = models.CharField(max_length=50, choices=OrganizationSize.choices)
    members = models.IntegerField(null=True, blank=True)
    funding = models.ForeignKey(FundingInformation, on_delete=models.SET_NULL, null=True, blank=True)
    token = models.ForeignKey(TokenInformation, on_delete=models.SET_NULL, null=True, blank=True)
    governance = models.CharField(max_length=50, choices=GovernanceModel.choices, blank=True)
    social = models.ForeignKey('SocialLinks', on_delete=models.SET_NULL, null=True, blank=True)
    contact = models.ForeignKey('ContactInformation', on_delete=models.SET_NULL, null=True, blank=True)
    certifications = models.JSONField(default=list)
    tags = models.JSONField(default=list)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class SocialLinks(models.Model):
    website = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    discord = models.URLField(blank=True)
    github = models.URLField(blank=True)
    other = models.URLField(blank=True)

class ContactInformation(models.Model):
    person = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)