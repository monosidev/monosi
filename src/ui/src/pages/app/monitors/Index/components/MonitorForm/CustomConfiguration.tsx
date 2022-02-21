import React, { useEffect, useState } from 'react';

import {
  EuiFormRow,
  EuiFieldText,
  EuiFlexGroup,
  EuiFlexItem,
  EuiComboBox,
  EuiButton,
  EuiTextArea,
  EuiSpacer,
} from '@elastic/eui';

const ThresholdForm: React.FC<any> = ({threshold, setThreshold}) => {
  const [selectedOptions, setSelectedOptions] = useState([]);
  const [value, setValue] = useState('');

  useEffect(() => {
    const retrieveOperator = (selectedOptions:any) => {
      if (selectedOptions.length > 0) {
        return selectedOptions[0].value;
      } else {
        return null
      };
    }
    setThreshold({
        id: threshold.id,
        operator: retrieveOperator(selectedOptions),
        value: value,
    }, threshold.id);
  }, [value, selectedOptions, threshold])

  return (
    <EuiFlexGroup>
      <EuiFlexItem>
      <EuiFormRow label="Operator">
      <EuiComboBox
          placeholder="Select a single option"
          singleSelection={{ asPlainText: true }}
          options={
            ['eq', 'ne', 'gt', 'ge', 'lt', 'le'].map((el: any) => {
              return {
                label: el,
                value: el,
              }
            })
          }
          selectedOptions={selectedOptions}
          onChange={(e: any) => setSelectedOptions(e)}
        />
      </EuiFormRow>
      </EuiFlexItem>
      <EuiFlexItem>
      <EuiFormRow label="Value (Numeric)">
        <EuiFieldText
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
  const [thresholds, setThresholds] = useState<any[]>([]);
  
  function updateFormState(setState: any) {
    setState();
    setConfiguration({ sql: sql, thresholds: thresholds.map((el:any) => {return {operator: el.operator, value: parseFloat(el.value)}}) });
  }

  const handleAddThreshold = () => {
        const num_thresholds = thresholds.length;
        const newThreshold: any = {
                id: num_thresholds,
                operator: null,
                value: null,
        }
        const newThresholds: any = thresholds;
        newThresholds.push(newThreshold);
        updateFormState(() => setThresholds([...newThresholds]));
  };

  const setThreshold = (threshold: any, id: any) => {
       const newThresholds = thresholds;
       newThresholds.map((el: any) => {
        if (el.id === id) {
          return threshold;
        } else {
          return el;
        }
       });
       updateFormState(() => setThresholds([...newThresholds]));
  }

  let thresholdsBlock = thresholds.sort((a: any, b: any) => a.id - b.id).map((el: any) => {
    return <EuiFormRow><ThresholdForm threshold={el} setThreshold={setThreshold} /></EuiFormRow>
  });

  return (
    <div>
      <br />
      <EuiFormRow label="SQL">
        <EuiTextArea
          value={sql}
          onChange={(e: any) => updateFormState(() => setSql(e.target.value))}
        />
      </EuiFormRow>
      {thresholdsBlock}
      <EuiSpacer />
      <EuiButton onClick={handleAddThreshold}>
        Add Threshold
      </EuiButton>
      <EuiSpacer />

    </div>
  );
};

export default CustomConfiguration;
