import React, { useState } from 'react';

import { EuiFormRow, EuiFieldText, EuiTextArea } from '@elastic/eui';

const CustomConfiguration: React.FC<{ setConfiguration: any }> = ({
  setConfiguration,
}) => {
  const [sql, setSql] = useState('');
  const [thresholds, setThresholds] = useState('');

  function updateFormState(setState: any) {
    setState();
    setConfiguration({ sql: sql, thresholds: [] });
  }

  return (
    <>
      <EuiFormRow label="SQL">
        <EuiTextArea
          value={sql}
          onChange={(e: any) => updateFormState(() => setSql(e.target.value))}
        />
      </EuiFormRow>
      <EuiFormRow label="Thresholds">
        <EuiFieldText
          // TODO: this shouldn't be disabled and should expect a certain format of input
          disabled
          value={thresholds}
          onChange={(e: any) =>
            updateFormState(() => setThresholds(e.target.value))
          }
        />
      </EuiFormRow>
    </>
  );
};

export default CustomConfiguration;
