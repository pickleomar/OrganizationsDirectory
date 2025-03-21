import React, { useState, useEffect } from 'react';
import { getOwnershipStructures } from '../api';

const OrganizationType = {
  COOPERATIVE: 'cooperative',
  EMPLOYEE_OWNED: 'employee_owned',
  DAO: 'dao',
  CRYPTO_WEB3: 'crypto_web3',
  ESOP: 'esop',
  PLATFORM_COOP: 'platform_coop',
  COMMUNITY_TRUST: 'community_trust',
  HYBRID: 'hybrid',
  OTHER: 'other',
};

const OwnershipStructure = {
  EMPLOYEE_OWNED: 'employee_owned',
  WORKER_COOP: 'worker_coop',
  CONSUMER_COOP: 'consumer_coop',
  MULTI_STAKEHOLDER_COOP: 'multi_stakeholder_coop',
  MEMBER_OWNED: 'member_owned',
  INVESTOR_OWNED: 'investor_owned',
  COMMUNITY_OWNED: 'community_owned',
  TOKEN_BASED: 'token_based',
  ESOP: 'esop',
  HYBRID: 'hybrid',
  OTHER: 'other',
};

const GeographicalScope = {
  LOCAL: 'local',
  REGIONAL: 'regional',
  NATIONAL: 'national',
  GLOBAL: 'global',
  VIRTUAL: 'virtual',
};

const GovernanceModel = {
  DIRECT: 'direct',
  REPRESENTATIVE: 'representative',
  TOKEN: 'token',
  HYBRID: 'hybrid',
  BOARD: 'board',
  SOCIOCRATIC: 'sociocratic',
  OTHER: 'other',
};

const Filters = ({ onFilter }) => {
  const [ownershipOptions, setOwnershipOptions] = useState([]);
  const [filters, setFilters] = useState({
    name: '',
    type: '',
    ownership: [],
    industry: '',
    geoScope: '',
    governance: '',
  });

  const [naceCodes, setNaceCodes] = useState([]);

  
  useEffect(() => {
    fetch('/NACEcodes.txt') 
      .then((response) => response.text())
      .then((data) => {
        const codes = data.split('\n').map((line) => line.trim());
        setNaceCodes(codes);
      })
      .catch((error) => console.error('Error loading NACE codes:', error));
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFilters({ ...filters, [name]: value });
  };

  const handleOwnershipChange = (e) => {
    const selectedOptions = Array.from(e.target.selectedOptions, (option) => option.value);
    setFilters({ ...filters, ownership: selectedOptions });
  };

  const handleApplyFilters = () => {
    onFilter(filters);
  };

  const handleClearFilters = () => {
    setFilters({
      name: '',
      type: '',
      ownership: [],
      industry: '',
      geoScope: '',
      governance: '',
    });
    onFilter({}); // Clear filters in the parent component
  };

  return (
    <div>
      {/* Organization Type */}
      <select name="type" value={filters.type} onChange={handleChange}>
        <option value="">Organization Type</option>
        {Object.entries(OrganizationType).map(([key, value]) => (
          <option key={key} value={value}>
            {key.replace(/_/g, ' ')}
          </option>
        ))}
      </select>

      {/* Ownership Structure (Multi-Select) */}
      <select
        name="ownership"
        multiple
        value={filters.ownership}
        onChange={handleOwnershipChange}
      >
        <option value="">Ownership Structure</option>
        {Object.entries(OwnershipStructure).map(([key, value]) => (
          <option key={key} value={value}>
            {key.replace(/_/g, ' ')}
          </option>
        ))}
      </select>

      {/* Industry (NACE Codes) */}
      <select name="industry" value={filters.industry} onChange={handleChange}>
        <option value="">Industry</option>
        {naceCodes.map((code) => {
          const [shortCode] = code.split(' - ');
          return (
            <option key={code} value={shortCode}>
              {code}
            </option>
          );
        })}
      </select>

      {/* Geographic Scope */}
      <select name="geoScope" value={filters.geoScope} onChange={handleChange}>
        <option value="">Geographic Scope</option>
        {Object.entries(GeographicalScope).map(([key, value]) => (
          <option key={key} value={value}>
            {key.replace(/_/g, ' ')}
          </option>
        ))}
      </select>

      {/* Governance Model */}
      <select name="governance" value={filters.governance} onChange={handleChange}>
        <option value="">Governance Model</option>
        {Object.entries(GovernanceModel).map(([key, value]) => (
          <option key={key} value={value}>
            {key.replace(/_/g, ' ')}
          </option>
        ))}
      </select>

      {/* Buttons */}
      <button onClick={handleApplyFilters}>Apply Filters</button>
      <button onClick={handleClearFilters}>Clear Filters</button>
    </div>
  );
};

export default Filters;