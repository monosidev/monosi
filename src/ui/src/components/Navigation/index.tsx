import React from 'react';
import {
  EuiHeader,
  EuiAvatar,
} from '@elastic/eui';

import HeaderAvatar from './HeaderAvatar';
import HeaderLinks from './HeaderLinks';

const Navigation: React.FC = () => {
  const headerAvatar = <HeaderAvatar />;
  const headerLinks = <HeaderLinks />

  const tempLogo = () => {
    return (
      <div style={{padding: '0px 20px'}}>
        <EuiAvatar
          size="m"
          type="space"
          name="monosi"
          color="#026ab4"
          initials="Si"
          initialsLength={2}
        />
      </div>
    );
  };

  const sections = [
    {
      items: [
        tempLogo(),
        headerLinks,
      ],
    },
    {
      items: [
          headerAvatar,
      ],
    },
  ];

  return (
    <EuiHeader
      theme="dark"
      sections={sections}
    />
  );
};

export default Navigation;
