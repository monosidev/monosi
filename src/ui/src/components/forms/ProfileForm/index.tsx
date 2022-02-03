import React, { useState, useEffect } from 'react';

import {
  EuiFlexGroup,
  EuiFlexItem,
  EuiFormRow,
  EuiFieldText,
} from '@elastic/eui';


const ProfileForm: React.FC = () => {
  const [email, _] = useState('');

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

