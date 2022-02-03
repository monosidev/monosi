import React, { ReactNode } from 'react';
import {
	EuiPage,
	EuiPageHeader,
	EuiPageSideBar,
	EuiPageBody,
	EuiPageContent,
	EuiPageContentBody,
} from '@elastic/eui';

import Navigation from 'components/Navigation';
import SideNavigation from './SideNavigation';

interface PageProps {
  title?: string;
  rightSideItems?: ReactNode[];
  children?: ReactNode;
}

const SettingsPage: React.FC<PageProps> = ({title, rightSideItems, children}) => {
	return (
		<>
		    <Navigation />
		    <EuiPage paddingSize="none" style={{minHeight: 'calc(100vh - 48px)'}}>
		      <EuiPageSideBar paddingSize="l" sticky>
		      	<SideNavigation />
		      </EuiPageSideBar>

		      <EuiPageBody panelled fullHeight>
		        <EuiPageHeader
		          pageTitle={title}
		          rightSideItems={rightSideItems}
		        />
		        <EuiPageContent
		          hasBorder={false}
		          hasShadow={false}
		          paddingSize="none"
		          color="transparent"
		          borderRadius="none"
		        >
		          <EuiPageContentBody>
		          	{children}
		          </EuiPageContentBody>
		        </EuiPageContent>
		      </EuiPageBody>
		    </EuiPage>
		</>
	);
}

export default SettingsPage;
