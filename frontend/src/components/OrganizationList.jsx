import React from 'react';
import OrganizationItem from './OrganizationItem';

const OrganizationList = ({ organizations = [] }) => {
  if (!Array.isArray(organizations)) {
    console.error('Expected organizations to be an array but got:', organizations);
    return <div>No organizations found.</div>;
  }

  return (
    <div>
      {organizations.map((org) => (
        <OrganizationItem key={org.id} organization={org} />
      ))}
    </div>
  );
};


export default OrganizationList;