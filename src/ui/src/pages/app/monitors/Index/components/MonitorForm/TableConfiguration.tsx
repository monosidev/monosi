import React, { useState } from 'react';

import {
  EuiFormRow,
  EuiFieldText,
} from '@elastic/eui';

const TableConfiguration: React.FC<{setConfiguration: any}> = ({setConfiguration}) => {
  const [table, setTable] = useState('');
  const [timestampField, setTimestampField] = useState('');

  React.useEffect(() => {
         setConfiguration({
           "table": table,
           "timestamp_field": timestampField,
         });
  }, [table, timestampField])
        
  return (
    <>
      <EuiFormRow label="Table">
        <EuiFieldText
          value={table}
          onChange={(e: any) => setTable(e.target.value)}
        />
      </EuiFormRow>
      <EuiFormRow label="Timestamp Field">
        <EuiFieldText
          value={timestampField}
          onChange={(e: any) => setTimestampField(e.target.value)}
        />
      </EuiFormRow>
    </>
  );
};

export default TableConfiguration;

