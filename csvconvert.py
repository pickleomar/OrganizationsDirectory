import json
import uuid
import requests
import csv

# --- NACE Code Loading and Parsing ---
#Returns a dictionary of {nacecode:description,}
def load_nace_codes(filepath):
    """Loads NACE codes from a text file and creates a lookup dictionary."""
    nace_codes = {}
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split(" - ", 1)  # Split only once at the first " - "
                if len(parts) == 2:
                    code, description = parts[0].strip(), parts[1].strip()
                    nace_codes[code] = description
    return nace_codes

def find_best_nace_code(description, nace_codes):
    """Finds the best matching NACE code based on description keywords."""
    description = description.lower()
    best_code = None
    for code, desc in nace_codes.items():
        desc_lower = desc.lower()
        if any(keyword in description for keyword in desc_lower.split()):  #Check if any keyword from description
            if best_code is None or len(desc_lower) < len(nace_codes[best_code].lower()): #select the shortest description to be more accurate
                best_code = code
    return best_code

# Ownership structure mapping
OWNERSHIP_STRUCTURE_LOOKUP = {
    "company": ["Token-based Ownership"],
    "cooperative": ["Community-Owned"],
    "resource": ["Community-Owned"],
    "organization": ["Community-Owned"],
    "platform co-op": ["Community-Owned"],
    "co-op-run platform": ["Community-Owned"],
}

# Static lookup for NACE codes based on the Category field. Changed since this is no longer useful.
NACE_LOOKUP = {
    "supporter": None, #No defaults available to every category
    "platform co-op": None, #No defaults available to every category
    "co-op-run platform": None, #No defaults available to every category
}

# Mapping for legal structures based on the "Type" field
LEGAL_STRUCTURE_LOOKUP = {
    "company": "corporation",
    "cooperative": "cooperative",
    "resource": "other",  # Adjust as needed
    "organization": "other",
    "platform co-op": "cooperative",
}

# Mapping for OrganizationType based on the Category field
ORGANIZATION_TYPE_STRUCTURE_LOOKUP = {
    "supporter": "community_trust",
    "platform co-op": "platform_coop",
    "shared platform": "employee_owned",
    "co-op-run platform": "platform_coop",
    # If the category isn't listed here, we will default to "other"
}

# Governance model mapping
GOVERNANCE_MODEL_LOOKUP = {
    "company": "board",
    "cooperative": "direct",
    "resource": "other",
    "organization": "board",
    "platform co-op": "direct",
    "co-op-run platform": "direct",
}

# Keywords to identify DAO or Crypto/Web3 organizations
DAO_KEYWORDS = {"dao", "decentralized", "autonomous", "governance"}
CRYPTO_KEYWORDS = {"blockchain", "crypto", "web3", "token", "nft"}

def parse_comma_separated(value):
    """Convert a comma-separated string into a list. Return an empty list if the value is empty."""
    if isinstance(value, str) and value.strip():
        return [item.strip() for item in value.split(',')]
    return []

def determine_geo_scope(location_str):
    """Determine the geographic scope based on the location string."""
    if "virtual" in location_str.lower():
        return "virtual"
    if "," in location_str:
        parts = [p.strip() for p in location_str.split(",")]
        if len(parts) >= 2:
            return "local" if len(parts) == 2 else "regional"
    if location_str.strip() == "":
        return "virtual"
    return "global"

def get_city_country_from_coords(lat, lon):
    """Use OpenStreetMap's Nominatim API to get city and country from coordinates."""
    try:
        response = requests.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={"format": "json", "lat": lat, "lon": lon},
            headers={"User-Agent": "YourApp/1.0"}
        )
        data = response.json()
        address = data.get("address", {})
        city = address.get("city") or address.get("town") or address.get("village") or ""
        country = address.get("country", "")
        return city, country
    except Exception as e:
        print(f"Geolocation API failed for coordinates ({lat}, {lon}): {e}")
        return "", ""

def determine_organization_type(tags):
    """Determine the organization type based on tags."""
    tags_lower = {tag.lower() for tag in tags}
    if any(keyword in tags_lower for keyword in DAO_KEYWORDS):
        return "dao"
    if any(keyword in tags_lower for keyword in CRYPTO_KEYWORDS):
        return "crypto_web3"
    return "other"

def convert_json(input_file, output_file, nace_file):
    """Converts the input JSON file, mapping to the specified format."""

    nace_codes = load_nace_codes(nace_file) #Load NACE codes from provided file
    
    with open(input_file, 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    results = []
    for row in data:
        # Extract and clean fields from CSV-derived JSON
        name = row.get("Name", "").strip()
        description = row.get("Description", "").strip()
        
        csv_category = row.get("Category", "").strip().lower()
        industry = find_best_nace_code(description, nace_codes)

        # Map organization type using the category.
        org_type = ORGANIZATION_TYPE_STRUCTURE_LOOKUP.get(csv_category, "other")
        
        # Get the "Type" field for legal structure mapping.
        type_field = row.get("Type", "").strip().lower()
        legal_structure = LEGAL_STRUCTURE_LOOKUP.get(type_field, "other")
        
        # Determine ownership structure
        ownership_structure = OWNERSHIP_STRUCTURE_LOOKUP.get(type_field, ["Community-Owned"])
        
        # Determine geographic scope
        location_str = row.get("Location", "").strip()
        geo_scope = determine_geo_scope(location_str)
        
        # Determine governance model
        governance_model = GOVERNANCE_MODEL_LOOKUP.get(type_field, "other")
        
        # Get fields for tags: combine "What are you looking for?" and "Activities"
        what_looking_for = row.get("What are you looking for?", "").strip()
        activities = row.get("Activities", "").strip()
        tags = []
        if what_looking_for:
            tags.append(what_looking_for)
        tags.extend(parse_comma_separated(activities))
        
        # Determine organization type based on tags
        org_type = determine_organization_type(tags)
        
        logo = row.get("Logo", "").strip()
        website = row.get("Website", "").strip()
        
        # Process Latitude and Longitude: convert to string if numeric.
        latitude = row.get("Latitude", "")
        longitude = row.get("Longitude", "")
        if isinstance(latitude, (float, int)):
            lat_val = str(latitude)
        else:
            lat_val = str(latitude).strip()
        if isinstance(longitude, (float, int)):
            lon_val = str(longitude)
        else:
            lon_val = str(longitude).strip()
        
        github = row.get("Open  Repo", "").strip()
        email = row.get("Email", "").strip()
        
        # Process location: if location string contains a comma, assume format "City, Country"
        if "," in location_str:
            parts = [p.strip() for p in location_str.split(",")]
            if len(parts) >= 2:
                city = parts[0]
                country = parts[-1]
            else:
                city, country = "", ""
        elif lat_val and lon_val:
            city, country = get_city_country_from_coords(lat_val, lon_val)
        else:
            city, country = "", ""
        
        # Build the organization record matching your Django model structure.
        organization = {
            "id": str(uuid.uuid4()),
            "name": name,
            "description": description,
            "type": org_type,  # OrganizationType mapped from tags
            "industry": industry,  # NACE code from description
            "ownership_structure": ownership_structure,  # Determined from type_field
            "legal_structure": legal_structure,
            "year_founded": None,  # Not provided in CSV.
            "location": {
                "city": city,
                "country": country,
                "address": "",  # Not provided.
                "state_region": "",
                "zip_postal_code": ""
            },
            "geo_scope": geo_scope,
            "size": "unknown",  # Not provided.
            "members": None,    # Not provided.
            "funding": {
                "sources": [],  # Not provided.
                "revenue": ""
            },
            "token": {
                "name": "",  # Not provided.
                "token_symbol": "",
                "blockchain_platform": "",
                "governance_mechanism": "",
                "link_to_token_contract": ""
            },
            "governance_model": governance_model,
            "links_social_media": {
                "website": website,
                "twitter": "",  # Not provided.
                "linkedin": "",  # Not provided.
                "discord": "",   # Not provided.
                "github": github,
                "other": logo   # Logo stored as an extra link.
            },
            "contact_information": {
                "contact_person": "",  # Not provided.
                "email": email,
                "phone": ""  # Not provided.
            },
            "certifications_affiliations": [],
            "tags": tags
        }
        results.append(organization)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(results, outfile, indent=4)
    
    print(f"Converted JSON saved to {output_file}")

""" if __name__ == '__main__':
    nace_codes_file = "NACEcodes.txt"
    convert_json("converted_data.json", "django_seed_data.json", nace_codes_file) """