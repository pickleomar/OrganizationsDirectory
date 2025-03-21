import React, { useState, useEffect } from 'react';
import SearchBar from './components/SearchBar';
import Filters from './components/Filters';
import OrganizationList from './components/OrganizationList';
import { searchOrganizations, filterOrganizations } from './api';
import './App.css';

const App = () => {
  const [organizations, setOrganizations] = useState([]);

  useEffect(() => {
    console.log('Organizations state updated:', organizations);
  }, [organizations]);

  const handleSearch = async (query) => {
    const data = await searchOrganizations(query);
    if (Array.isArray(data)) {
      setOrganizations(data);
    } else if (data.results) {
      setOrganizations(data.results);
    } else {
      console.warn("Unexpected API response structure:", data);
      setOrganizations([]);
    }
  };

  const handleFilter = async (filters) => {
    console.log('Filtering with:', filters);
    try {
      const data = await filterOrganizations(filters);
      console.log('Filter response:', data);

      if (data && data.results) {
        setOrganizations(data.results);
      } else {
        console.error('Unexpected API response structure:', data);
        setOrganizations([]);
      }
    } catch (error) {
      console.error('Error filtering organizations:', error);
    }
  };

  useEffect(() => {

    handleSearch('');
  }, []);

  return (
    <div className="App">
      <h1>Organization Directory</h1>
      <SearchBar onSearch={handleSearch} />
      <Filters onFilter={handleFilter} />
      <OrganizationList organizations={organizations} />
    </div>
  );
};

export default App;