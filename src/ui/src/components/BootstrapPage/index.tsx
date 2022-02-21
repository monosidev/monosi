import React, { ReactNode } from 'react';

import BootstrapNavigation from 'components/BootstrapNavigation';

import 'bootstrap/dist/css/bootstrap.min.css';
import './bootstrap_page.css';

interface PageProps {
  children?: ReactNode;
  selectedTab: string
}

const BootstrapPage: React.FC<PageProps> = ({ children, selectedTab }) => {
  return (
          <div className="bg-light faux-body">

            <div className="container-fluid">
              <div className="row">
                <BootstrapNavigation selectedTab={selectedTab} />
                {children}
              </div>
            </div>
          </div>
  );
};

export default BootstrapPage;
