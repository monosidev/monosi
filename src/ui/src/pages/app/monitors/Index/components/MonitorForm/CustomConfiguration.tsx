import React, { useState } from 'react';

import {
  EuiFormRow,
  EuiFieldText,
  EuiFlexGroup,
  EuiFlexItem,
  EuiComboBox,
} from '@elastic/eui';

const ThresholdForm: React.FC = () => {
  const [selectedOptions, setSelectedOptions] = useState([]);
  const [value, setValue] = useState('');

  return (
    <EuiFlexGroup>
      <EuiFlexItem>
      <EuiFormRow label="Operator">
      <EuiComboBox
          placeholder="Select a single option"
          singleSelection={{ asPlainText: true }}
          options={[
            {
              label: 'eq',
              value: 'eq'
            },
          ]}
          selectedOptions={selectedOptions}
          onChange={(e:any) => setSelectedOptions(e.target.value)}
        />
      </EuiFormRow>
      </EuiFlexItem>
      <EuiFlexItem>
      <EuiFormRow label="Value">
        <EuiFieldText
          disabled
          value={value}
          onChange={(e: any) => setValue(e.target.value)}
        />
      </EuiFormRow>
      </EuiFlexItem>
    </EuiFlexGroup>
  );
}

const CustomConfiguration: React.FC<{setConfiguration: any}> = ({setConfiguration}) => {
  const [sql, setSql] = useState('');
  const [thresholds, setThresholds] = useState([]);
  
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
