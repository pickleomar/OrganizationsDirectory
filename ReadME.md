# Organization Directory Application

## Overview

This project is a full-stack web application that lets users search and filter a directory of organizations. The application provides a simple interface to:

- **Search** companies by name.
- **Filter** companies by:
  - Organization type
  - Ownership structure
  - Industry (NACE codes)
  - Geographic scope
  - Governance model

---

## Features

- **Search Functionality**  
  Use the search bar to query organizations by name. The backend leverages Django REST Framework's search filters to return matching results.

- **Filter Functionality**  
  Users can filter organizations by:
  - Organization Type (e.g., DAO, cooperative, etc.)
  - Ownership Structure (multi-select options)
  - Industry (NACE codes – only the code is sent in the request)
  - Geographic Scope (local, regional, national, global, or virtual)
  - Governance Model (direct, board, etc.)

- **Paginated API Responses**  
  The backend typically returns paginated responses with metadata (e.g., count and results), although the search endpoint can be configured to return a plain list.

- **Human-Readable Data**  
  Custom serializer fields provide human-readable representations for fields like industry and geographic scope.

---

## Technologies

- **Frontend:** React, JavaScript, Axios  
- **Backend:** Django, Django REST Framework, Python  
- **Database:** PostgreSQL (default) or any other Django-supported database  
- **Other:** DRF filters, logging

---

## Project Deliverables

- **Documentation & Data Scraping:**  
  - **Data Source:**  
    A CSV file from a public Internet of Ownership Directory is available [here](https://docs.google.com/spreadsheets/d/1RQTMhPJVVdmE7Yeop1iwYhvj46kgvVJQnn11EPGwzeY/edit?gid=674927682).
  - **Data Conversion:**  
    The CSV data was converted into JSON format using a custom script (`csvconvert.py`), which restructured the data in accordance with the provided schema.
  - **NACE Code Mapping:**  
    Each organization was linked to its corresponding NACE code using a text file (`NACEcodes.txt`).
  - **Geolocation Data:**  
    An external API was used to determine the city and country for each organization based on longitude and latitude.
  - **Database Design:**  
    The database schema was designed with sub-entities linked via foreign keys to enable faster and more reliable search and filtering.
  - **Data Seeding:**  
    A script (`seeddata.py`) automates the process of populating the database with initial, realistic data.

---
## Challenges Faced

- **Data Consistency:**  
  Ensuring that scraped data from public directories matched the required schema and was cleaned properly.
  
- **API Integration:**  
  Adapting to external APIs for geolocation and handling their rate limits and response formats.
  
- **Low-Code Backend Adaptation:**  
  Configuring a low-code backend (e.g., Airtable) to support custom filtering and search functionality.
  
- **Environment Configuration:**  
  Managing sensitive environment variables securely and ensuring easy setup for end users.
  
- **Pagination Handling:**  
  Ensuring the frontend properly handles paginated API responses while maintaining a smooth user experience.

---

## Installation and Setup

### Prerequisites

- **Frontend:** Node.js and npm  
- **Backend:** Python 3.x, pip, and (optionally) virtualenv

### Backend Setup

1. **Clone the Repository:**

   ```bash
   git clone <https://github.com/pickleomar/OrganizationsDirectory.git>
   cd <organizations_manager> ```
2. **Configure Environment Variables:**
- A sample environment configuration file (.env.example) is provided in the repository.
``` cp .env.example .env
```
-Edit the .env file to enter your database credentials and any other settings. For example:
``` DEBUG=True

DATABASE_NAME=organizationsdb
DATABASE_USER=user
DATABASE_PASSWORD=password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```
3. **Install the requirements:**
    ```
    pip install -r requirements.txt 
    ``` 
4. **Apply migrations:**
```
    python manage.py migrate
    python manage.py makemigration
 ```

5. **Seed data to the DB:**
```
python manage.py seeddata

```
### Frontend Setup

```
cd frontend 

npm install

npm start
```
