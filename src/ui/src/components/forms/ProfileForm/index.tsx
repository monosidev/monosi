import React, { useState, useEffect } from 'react';
import UserService from 'services/users';
import {
  EuiFlexGroup,
  EuiFlexItem,
  EuiFormRow,
  EuiFieldText,
} from '@elastic/eui';


const ProfileForm: React.FC = () => {
  const [email, setEmail] = useState<string>('');

  useEffect(() => {
    async function loadEmail() {
      let res = await UserService.getAll();
      if (res !== null && res.user && res.user.email) {
        setEmail(res.user.email);
      }
    }

    loadEmail();
  }, []);

  return (
    <div>
      <EuiFlexGroup>
        <EuiFlexItem>
          <EuiFormRow label="Email">
            <EuiFieldText
              placeholder="example@email.com"
              value={email}
              disabled={true}
            />
          </EuiFormRow>
        </EuiFlexItem>
      </EuiFlexGroup>
    </div>
  );
};

export default ProfileForm;

