import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import {
  EuiAvatar,
  EuiPopover,
  EuiFlexItem,
  EuiFlexGroup,
  EuiSpacer,
  EuiLink,
  EuiHeaderSectionItemButton,
  EuiText,
} from '@elastic/eui';

const HeaderAvatar: React.FC = () => {
  const userPopoverId = 'userPopover';
  const history = useHistory();

  const [email, _] = useState('example@email.com');
  const [isOpen, setIsOpen] = useState(false);

  const onMenuButtonClick = () => {
    setIsOpen(!isOpen);
  };

  const closeMenu = () => {
    setIsOpen(false);
  };

  const button = (
    <EuiHeaderSectionItemButton
      aria-controls={userPopoverId}
      aria-expanded={isOpen}
      aria-haspopup="true"
      aria-label="Account menu"
      onClick={onMenuButtonClick}
    >
      <EuiAvatar name={email} size="s" />
    </EuiHeaderSectionItemButton>
  );

  return (
    <EuiPopover
      id={userPopoverId}
      repositionOnScroll
      button={button}
      isOpen={isOpen}
      anchorPosition="downRight"
      closePopover={closeMenu}
      panelPaddingSize="none"
    >
      <div style={{ width: 320 }}>
        <EuiFlexGroup
          gutterSize="m"
          className="euiHeaderProfile"
          responsive={false}
        >
          <EuiFlexItem grow={false}>
            <EuiAvatar name={email} size="xl" />
          </EuiFlexItem>

          <EuiFlexItem>
            <EuiText>
              <p>{email}</p>
            </EuiText>

            <EuiSpacer size="m" />

            <EuiFlexGroup>
              <EuiFlexItem>
                <EuiFlexGroup justifyContent="spaceBetween">
                  <EuiFlexItem grow={false}>
                    <EuiLink
                      onClick={() => history.push('/settings/profile')}
                    >
                      Edit Settings
                    </EuiLink>
                  </EuiFlexItem>
                </EuiFlexGroup>
              </EuiFlexItem>
            </EuiFlexGroup>
          </EuiFlexItem>
        </EuiFlexGroup>
      </div>
    </EuiPopover>
  );
};

export default HeaderAvatar;
