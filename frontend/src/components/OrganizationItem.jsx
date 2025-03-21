import React from 'react';

const OrganizationItem = ({ organization }) => {
  return (
    <div>
      <h2>{organization.name}</h2>
      <p>{organization.description}</p>
      <p>Type: {organization.type}</p>
      <p>Industry: {organization.industry_display || organization.industry}</p>
      <p>Geographic Scope: {organization.geo_scope_display}</p>
      <p>Governance Model: {organization.governance_display || organization.governance}</p>
    </div>
  );
};

export default OrganizationItem;