import React, { useState } from 'react';
import {
  useHistory,
  useLocation,
} from "react-router-dom";
import { EuiIcon, EuiSideNav, slugify } from '@elastic/eui';

const SideNavigation: React.FC = () => {
  const { pathname } = useLocation();
  const history = useHistory();

  const [isSideNavOpenOnMobile, setIsSideNavOpenOnMobile] = useState(false);
  const [selectedItemName, setSelectedItemName] = useState(pathname);

  const toggleOpenOnMobile = () => {
    setIsSideNavOpenOnMobile(!isSideNavOpenOnMobile);
  };

  const selectItem = (name: any, data: any) => {
    if (data['url'] !== undefined) {
      history.push(data['url']);
    }
    setSelectedItemName(data['url']);
  };

  const createItem = (name: any, data: any = {url: ''}) => {
    return {
      id: slugify(name),
      name,
      isSelected: selectedItemName === data['url'],
      onClick: () => selectItem(slugify(name), data),
      ...data,
    };
  };

  const sideNav = [
    createItem('Account', {
      onClick: undefined,
      icon: <EuiIcon type="user" />,
      items: [
        createItem('Profile', {url: "/settings/profile"}),
      ],
    }),
    createItem('Integrations', {
      onClick: undefined,
      icon: <EuiIcon type="home" />,
      items: [
        createItem('Data Sources', {url: "/settings/sources"}),
        createItem('Integrations', {url: "/settings/integrations"}),
      ],
    }),
  ];

  return (
    <EuiSideNav
      aria-label="Settings side navigation"
      mobileTitle="Navigate Settings"
      toggleOpenOnMobile={toggleOpenOnMobile}
      isOpenOnMobile={isSideNavOpenOnMobile}
      items={sideNav}
      style={{ width: 192 }}
    />
  );
};

export default SideNavigation;
