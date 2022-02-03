import React, { useState } from 'react';

import {
  EuiFormRow,
  EuiFieldText,
} from '@elastic/eui';

const CustomConfiguration: React.FC<{setConfiguration: any}> = ({setConfiguration}) => {
  const [sql, setSql] = useState('');
  const [thresholds, setThresholds] = useState('');
        
  function updateFormState(setState: any) {
       setState();
       setConfiguration({"sql": sql, "thresholds": []})
  }

  return (
    <>
      <EuiFormRow label="SQL">
        <EuiFieldText
          value={sql}
          onChange={(e: any) => updateFormState(() => setSql(e.target.value))}
        />
      </EuiFormRow>
      <EuiFormRow label="Thresholds">
        <EuiFieldText
          disabled
          value={thresholds}
          onChange={(e: any) => updateFormState(() => setThresholds(e.target.value))}
        />
      </EuiFormRow>
    </>
  );
};

export default CustomConfiguration;

