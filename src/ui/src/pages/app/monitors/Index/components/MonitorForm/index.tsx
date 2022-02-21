import React, { useState, useEffect } from 'react';

import {
  EuiButton,
  EuiFlexGroup,
  EuiFormRow,
  EuiFieldText,
  EuiFlexItem,
  EuiSelect,
  EuiCheckableCard,
  EuiSpacer,
  EuiHorizontalRule,
  EuiPageHeader,
  EuiFieldNumber,
  EuiComboBox,
} from '@elastic/eui';

import MonitorService from 'services/monitors';
import datasourceService from 'services/datasources';

import TableConfiguration from './TableConfiguration';
import CustomConfiguration from './CustomConfiguration';
import SchemaConfiguration from './SchemaConfiguration';

const MonitorForm: React.FC = () => {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [type, setType] = useState('table');
  const [datasourceName, setDatasourceName] = useState('');
  const [intervalAmount, setIntervalAmount] = useState('');
  const [intervalType, setIntervalType] = useState('minutes');
  const [configuration, setConfiguration] = useState('');

  const [datasources, setDatasources] = useState([]);
  const [selectedDatasource, setSelectedDatasource] = useState([]);

  useEffect(() => {
    async function loadDatasources() {
      let res = await datasourceService.getAll();
      if (res !== null && res.datasources) {
        setDatasources(res.datasources);
      }
    }
    loadDatasources();
  }, []);

  const selectDatasource = async (selectedOptions: any) => {
    if (selectedOptions.length === 0) return;

    setSelectedDatasource(selectedOptions);

    const datasource = selectedOptions[0].label;
    setDatasourceName(datasource);
  };

  const validateInput = () => {
    // TODO: change to server based validation once implemented
    if (name && parseInt(intervalAmount) >= 1) {
      return true;
    }
    return false;
  };

  const createMonitor = () => {
    const isValid = validateInput();
    if (!isValid) return;

    const service = MonitorService;
    const body: any = {
      name: name,
      type: type,
      datasource: datasourceName,
      configuration: configuration,
      schedule_minutes: intervalAmount,
      schedule_type: intervalType,
      // schedule: {
      //   interval_amount: intervalAmount,
      //   interval_type: intervalType,
      // },
    };
    if (description) {
      body['description'] = description;
    }

    const resp = service.create(body);

    // TODO: check for error on creation

    window.location.reload();
  };

  return (
    <>
      <EuiFlexGroup>
        <EuiFlexItem>
          <EuiFormRow label="Name">
            <EuiFieldText
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </EuiFormRow>
        </EuiFlexItem>
        <EuiFlexItem>
          <EuiFormRow label="Check every">
            <EuiFlexGroup>
              <EuiFlexItem>
                <EuiFieldNumber
                  required
                  min={1}
                  value={intervalAmount}
                  onChange={(e) => setIntervalAmount(e.target.value)}
                />
              </EuiFlexItem>
              <EuiFlexItem grow={false}>
                <EuiSelect
                  value={intervalType}
                  disabled
                  options={[{ text: 'minutes' }]}
                />
              </EuiFlexItem>
            </EuiFlexGroup>
          </EuiFormRow>
        </EuiFlexItem>
      </EuiFlexGroup>
      <EuiFlexGroup>
        <EuiFlexItem>
          <EuiFormRow label="Description">
            <EuiFieldText
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </EuiFormRow>
        </EuiFlexItem>
      </EuiFlexGroup>

      <EuiHorizontalRule />
      <EuiPageHeader
        pageTitle="Configure Monitor"
        description="Choose a monitor type and configure it's details"
      />
      <EuiHorizontalRule />
      <EuiCheckableCard
        id="table"
        label="Table Health"
        name="Table Health"
        value="table"
        checked={type === 'table'}
        onChange={() => setType('table')}
      />
      <EuiSpacer size="s" />
      <EuiCheckableCard
        id="custom"
        label="Custom SQL"
        name="Custom SQL"
        value="custom"
        checked={type === 'custom'}
        onChange={() => setType('custom')}
      />
      <EuiSpacer size="s" />
      <EuiCheckableCard
        id="schema"
        label="Schema Changes"
        name="Custom SQL"
        value="schema"
        disabled
        checked={type === 'schema'}
        onChange={() => setType('schema')}
      />
      <EuiHorizontalRule />

      <EuiFormRow label="Data Source">
        <EuiComboBox
          onChange={selectDatasource}
          singleSelection={{ asPlainText: true }}
          selectedOptions={selectedDatasource}
          options={datasources.map((el: any) => {
            return { label: el.name, value: el.id };
          })}
        />
      </EuiFormRow>
      {type === 'table' && (
        <TableConfiguration setConfiguration={setConfiguration} />
      )}
      {type === 'custom' && (
        <CustomConfiguration setConfiguration={setConfiguration} />
      )}
      {type === 'schema' && (
        <SchemaConfiguration setConfiguration={setConfiguration} />
      )}
      <EuiButton fill onClick={createMonitor}>
        Save
      </EuiButton>
    </>
  );
};

export default MonitorForm;
