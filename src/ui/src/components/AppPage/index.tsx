import React, { ReactNode } from 'react';
import {
  EuiAvatar,
  EuiLoadingContent,
  EuiPage, 
  EuiPageHeader,
  EuiPageBody,
} from '@elastic/eui';

import Navigation from 'components/Navigation';

interface PageHeaderProps {
  title?: string;
  rightSideItems?: ReactNode[];
}

const PageHeader: React.FC<PageHeaderProps> = ({title, rightSideItems}) => {
  if (title === undefined) {
    return <EuiLoadingContent lines={2} />;
  } else {
    return <EuiPageHeader pageTitle={title} rightSideItems={rightSideItems} />;
  }
};


interface PageProps extends PageHeaderProps {
  children?: ReactNode;
}

const AppPage: React.FC<PageProps> = ({ title, rightSideItems, children }) => {
  return (
    <>
      <Navigation />
      <EuiPage>
        <EuiPageBody>
          {PageHeader({title, rightSideItems})}
          {children}
        </EuiPageBody>
      </EuiPage>
    </>
  );
};

export default AppPage;
