import React from 'react';

import SettingsPage from 'components/SettingsPage';
import ProfileForm from 'components/forms/ProfileForm';

const ProfileSettings: React.FC = () => {
  return (
    <SettingsPage title="Profile" rightSideItems={[]}>
        <ProfileForm />
    </SettingsPage>
  );
};

export default ProfileSettings;
