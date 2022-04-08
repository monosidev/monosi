import React, { ReactNode } from 'react';

import Navigation from 'components/Navigation';

import 'bootstrap/dist/css/bootstrap.min.css';
import './bootstrap_page.css';

interface PageProps {
  children?: ReactNode;
  selectedTab: string
}

const Page: React.FC<PageProps> = ({ children, selectedTab }) => {
  return (
    <div className="bg-light faux-body">
      <div className="container-fluid">
        <div className="row">
          <Navigation selectedTab={selectedTab} />
          {children}
        </div>
      </div>
    </div>
  );
};

export default Page;
