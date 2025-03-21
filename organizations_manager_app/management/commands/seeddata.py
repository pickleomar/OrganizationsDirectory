import json
import uuid
from django.core.management.base import BaseCommand
from django.utils import timezone
from organizations_manager_app.models import (
    Organization, 
    Industry, 
    OwnershipStructure, 
    Location, 
    FundingInformation, 
    TokenInformation, 
    SocialLinks, 
    ContactInformation
)


class Command(BaseCommand):
    help = 'Seed the database with initial organization data'
    def load_nace_codes(self):
        nace_data = {}
        try:
            with open('NACEcodes.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if ' - ' in line:
                        code, description = line.split(' - ', 1)
                        nace_data[code.strip()] = description.strip()
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('NACEcodes.txt file not found!'))
        return nace_data
    def handle(self, *args, **kwargs):
        
        nace_mapping = self.load_nace_codes()
        # Load seed data
        with open('django_seed_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        for entry in data:  # Loop through the list of organizations
            self.stdout.write(f"Processing: {entry.get('name', 'Unknown Organization')}")

            # Get or create Industry
            industry_value = entry.get('industry') or ''
            industry_description = nace_mapping.get(industry_value, f"Unknown industry ({industry_value})")
        
            industry, _ = Industry.objects.get_or_create(
                nace_code=industry_value,
                defaults={'description': industry_description}
            )


            # Get or create Ownership Structures
            ownership_structures = []
            for structure in entry.get('ownership_structure', []):  # Ensure it's a list
                obj, _ = OwnershipStructure.objects.get_or_create(name=structure)
                ownership_structures.append(obj)

            # Create Location
            location = Location.objects.create(
                city=entry.get('location', {}).get('city', ''),
                country=entry.get('location', {}).get('country', '')
            )

            # Create Funding Information
            funding = FundingInformation.objects.create(
                sources=entry.get('funding', {}).get('sources', []),
                revenue=entry.get('funding', {}).get('revenue', '')
            )

            # Create Token Information
            token = TokenInformation.objects.create(
                name=entry.get('token', {}).get('name', ''),
                symbol=entry.get('token', {}).get('token_symbol', ''),
                blockchain=entry.get('token', {}).get('blockchain_platform', ''),
                governance=entry.get('token', {}).get('governance_mechanism', ''),
                contract=entry.get('token', {}).get('link_to_token_contract', '')
            )

            # Create Social Links
            social = SocialLinks.objects.create(
                website=entry.get('links_social_media', {}).get('website', ''),
                discord=entry.get('links_social_media', {}).get('discord', ''),
                github=entry.get('links_social_media', {}).get('github', '')
            )

            # Create Contact Information
            contact = ContactInformation.objects.create(
                person=entry.get('contact_information', {}).get('contact_person', ''),
                email=entry.get('contact_information', {}).get('email', '')
            )

            # Create Organization
            organization = Organization.objects.create(
                id=uuid.UUID(entry.get('id', str(uuid.uuid4()))),  # Ensure a valid UUID
                name=entry.get('name', 'Unnamed Organization'),
                description=entry.get('description', ''),
                type=entry.get('type', 'other'),
                industry=industry,
                legal_structure=entry.get('legal_structure', 'other'),
                year_founded=entry.get('year_founded', None),
                location=location,
                geo_scope=entry.get('geo_scope', 'global'),
                size=entry.get('size', 'unknown'),
                members=entry.get('members', None),
                funding=funding,
                token=token,
                governance=entry.get('governance_model', 'other'),
                social=social,
                contact=contact,
                certifications=entry.get('certifications_affiliations', []),
                tags=entry.get('tags', []),
                created=timezone.now(),
                updated=timezone.now()
            )

            # Add many-to-many relationships
            organization.ownership_structures.add(*ownership_structures)

            self.stdout.write(self.style.SUCCESS(f'Successfully added: {organization.name}'))

        self.stdout.write(self.style.SUCCESS('Database seeding completed!'))
