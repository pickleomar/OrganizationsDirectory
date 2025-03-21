import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export const searchOrganizations = async (query) => {
  console.log('Searching organizations with query:', query);
  try {
    const response = await axios.get(`${API_URL}/organizations/`, {
      params: { search: query }
    });
    console.log('Search response:', response.data);
    return response.data; 
  } catch (error) {
    console.error('Error searching organizations:', error);
    throw error;
  }
};

export const filterOrganizations = async (filters) => {
  console.log('Filtering organizations with filters:', filters);
  try {
    const params = new URLSearchParams();
    Object.entries(filters).forEach(([key, value]) => {
      if (Array.isArray(value)) {
        value.forEach(v => params.append(key, v));
      } else if (value) {
        params.append(key, value);
      }
    });
    const response = await axios.get(`${API_URL}/organizations/filter/`, { params });
    console.log('Filter response:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error filtering organizations:', error);
    throw error;
  }
};

export const getOwnershipStructures = async () => {
  console.log('Fetching ownership structures');
  try {
    const response = await axios.get(`${API_URL}/ownership-structures/`);
    console.log('Ownership structures response:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error fetching ownership structures:', error);
    throw error;
  }
};