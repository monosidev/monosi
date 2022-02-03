import React, { useState } from 'react';
import { useHistory, useLocation } from 'react-router-dom';
import {
  EuiHeaderLink,
  EuiHeaderLinks,
} from '@elastic/eui';

function rootPathName(pathname: string): string {
  if (pathname.startsWith('/')) {
    const pathParts = pathname.split('/');

    if (pathParts.length > 1) {
      return pathParts[1];
    }
  }
  return '';
}

const HeaderLinks: React.FC = () => {
  const history = useHistory();
  const location = useLocation();

  const [activeLink, _] = useState(rootPathName(location.pathname));

  const isActive = (link: string) => { return link === activeLink };
  const handleClick = (e: any) => { history.push("/" + e.target.innerText.toLowerCase()) };

  return (
    <EuiHeaderLinks>
      <EuiHeaderLink 
        isActive={isActive('monitors')}
        onClick={handleClick}>
        Monitors
      </EuiHeaderLink>
      <EuiHeaderLink 
        iconType="help"
        target="_blank"
        href={'https://docs.monosi.dev'}>
        Docs
      </EuiHeaderLink>
    </EuiHeaderLinks>
  );
}

export default HeaderLinks;
