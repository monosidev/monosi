import React, { useState } from 'react';

import {
  EuiFormRow,
  EuiFieldText,
} from '@elastic/eui';

const SchemaConfiguration: React.FC<{setConfiguration: any}> = ({setConfiguration}) => {
  const [table, setTable] = useState('');
  // const [thresholds, setThresholds] = useState('');
        
  function updateFormState(setState: any) {
       setState();
       setConfiguration({"table": table})
  }

  return (
    <>
      <EuiFormRow label="Table">
        <EuiFieldText
          value={table}
          onChange={(e: any) => updateFormState(() => setTable(e.target.value))}
        />
      </EuiFormRow>
    </>
  );
};

export default SchemaConfiguration;


