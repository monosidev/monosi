import React, { useState, useEffect } from 'react';
import {
  EuiFlexGroup,
  EuiFlexItem,
  EuiFormRow,
  EuiHeaderLogo,
  EuiButton,
  EuiFieldText,
  EuiFieldPassword,
  EuiFilePicker,
  EuiSpacer,
  EuiFlexGrid,
  EuiCard,
  EuiIcon,
  EuiHorizontalRule,
  EuiPageHeader,
} from '@elastic/eui';

import { BigQueryLogo } from 'images';
import datasourceService from 'services/datasources';

enum DataSourceTypes {
  SNOWFLAKE = 'snowflake',
  POSTGRESQL = 'postgresql',
  REDSHIFT = 'redshift',
  BIGQUERY = 'bigquery'
}

const DatasourceForm = () => {
  const [datasourceType, setDatasourceType] = useState<DataSourceTypes>(
    DataSourceTypes.SNOWFLAKE
  );
  const [datasourceName, setDatasourceName] = useState<string>('');

  const [account, setAccount] = useState<string>('');
  const [user, setUser] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [warehouse, setWarehouse] = useState<string>('');
  const [database, setDatabase] = useState<string>('');
  const [schema, setSchema] = useState<string>('');
  const [host, setHost] = useState<string>('');
  const [port, setPort] = useState<string>('');
  const [project, setProject] = useState<string>('');
  const [dataset, setDataset] = useState<string>('');
  const [file, setFile] = useState<File | null>(null);

  const submitForm = async () => {

    let config = {}

    if (datasourceType === DataSourceTypes.SNOWFLAKE) {
      config = {
        driver: datasourceType,
        account: account,
        user: user,
        password: password,
        warehouse: warehouse,
        database: database,
        schema: schema,
      };
    } else if (
      datasourceType === DataSourceTypes.POSTGRESQL ||
      datasourceType === DataSourceTypes.REDSHIFT
    ) {
      config = {
        user: user,
        password: password,
        host: host,
        port: parseInt(port),
        database: database,
        schema: schema
      };
    } else if (datasourceType === DataSourceTypes.BIGQUERY) {
      // TODO: Implement better validation
      if(!datasourceName || !project || !dataset || !file) return;

      const credentials_base64 = await toBase64(file);

      config = {
        project,
        dataset,
        credentials_base64,
      };
    }

    const body = {
      name: datasourceName,
      type: datasourceType,
      config
    };

    await datasourceService.create(body);

    window.location.reload();
    
  };

  const onChange = (value: any) => {
    setDatasourceType(value);
  };

  const onFileChange = (files: FileList | null) => {
    if(files && files.length > 0) {
      const filesArray = Array.from(files);
      const firstFile = filesArray[0];
      setFile(firstFile);
    }
  };

  const toBase64 = (file: File):Promise<string> => new Promise<string>((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      let encoded = reader.result?.toString() || '';
      encoded = encoded.replace(/^data:(.*,)?/, '');
      if ((encoded.length % 4) > 0) {
        encoded += '='.repeat(4 - (encoded.length % 4));
      }
      resolve(encoded);
    };
    reader.onerror = error => reject(error);
  });

  return (
    <div>
      <EuiFlexGrid columns={3}>
        <EuiFlexItem>
          <EuiCard
            icon={<EuiIcon type={DataSourceTypes.SNOWFLAKE} size="xl" />}
            selectable={{
              onClick: () => onChange(DataSourceTypes.SNOWFLAKE),
              isSelected: datasourceType === DataSourceTypes.SNOWFLAKE,
              isDisabled: false,
            }}
            title="Snowflake"
            description="Connect to Snowflake Data Warehouse"
          />
        </EuiFlexItem>
        <EuiFlexItem>
          <EuiCard
            selectable={{
              onClick: () => onChange(DataSourceTypes.POSTGRESQL),
              isSelected: datasourceType === DataSourceTypes.POSTGRESQL,
              isDisabled: false,
            }}
            icon={<EuiIcon type="logoPostgres" size="xl" />}
            title="PostgreSQL"
            description="Connect to PostgreSQL Database"
          />
        </EuiFlexItem>
        <EuiFlexItem>
          <EuiCard
            selectable={{
              onClick: () => onChange(DataSourceTypes.REDSHIFT),
              isSelected: datasourceType === DataSourceTypes.REDSHIFT,
              isDisabled: false,
            }}
            icon={<EuiIcon type="logoAWS" size="xl" />}
            title="Redshift"
            description="Connect to AWS Redshift Data Warehouse"
          />
        </EuiFlexItem>
        <EuiFlexItem>
          <EuiCard
            selectable={{
              onClick: () => onChange(DataSourceTypes.BIGQUERY),
              isSelected: datasourceType === DataSourceTypes.BIGQUERY,
              isDisabled: false,
            }}
            icon={<EuiIcon type={BigQueryLogo} size="xl" />}
            title="BigQuery"
            description="Connect to Google BigQuery Data Warehouse"
          />
        </EuiFlexItem>
      </EuiFlexGrid>

      <EuiHorizontalRule />

      {datasourceType === DataSourceTypes.POSTGRESQL && (
        <div>
          <EuiPageHeader
            iconType="logoPostgres"
            pageTitle="PostgreSQL"
            description="Connect to PostgreSQL Database"
          />
          <EuiHorizontalRule />
          <EuiFormRow label="Name for Data Source">
            <EuiFieldText
              placeholder="Company Data Warehouse"
              onChange={(e) => setDatasourceName(e.target.value)}
              value={datasourceName}
            />
          </EuiFormRow>
          <EuiFormRow label="User">
            <EuiFieldText
              placeholder="MONOSI_USER"
              onChange={(e) => setUser(e.target.value)}
              value={user}
            />
          </EuiFormRow>
          <EuiFormRow label="Password">
            <EuiFieldPassword
              placeholder="password123"
              onChange={(e) => setPassword(e.target.value)}
              value={password}
            />
          </EuiFormRow>
          <EuiFormRow label="Host">
            <EuiFieldText
              placeholder="host"
              onChange={(e) => setHost(e.target.value)}
              value={host}
            />
          </EuiFormRow>
          <EuiFormRow label="Port">
            <EuiFieldText
              placeholder="5432"
              onChange={(e) => setPort(e.target.value)}
              value={port}
            />
          </EuiFormRow>
          <EuiFormRow label="Database (case-sensitive)">
            <EuiFieldText
              placeholder="postgres"
              onChange={(e) => setDatabase(e.target.value)}
              value={database}
            />
          </EuiFormRow>
          <EuiFormRow label="Schema (case-sensitive)">
            <EuiFieldText
              placeholder="public"
              onChange={(e) => setSchema(e.target.value)}
              value={schema}
            />
          </EuiFormRow>
        </div>
      )}
      {datasourceType === DataSourceTypes.REDSHIFT && (
        <div>
          <EuiPageHeader
            iconType="logoAWS"
            pageTitle="Redshift"
            description="Connect to Redshift Data Warehouse"
          />
          <EuiHorizontalRule />
          <EuiFormRow label="Name for Data Source">
            <EuiFieldText
              placeholder="Company Data Warehouse"
              onChange={(e) => setDatasourceName(e.target.value)}
              value={datasourceName}
            />
          </EuiFormRow>
          <EuiFormRow label="User">
            <EuiFieldText
              placeholder="MONOSI_USER"
              onChange={(e) => setUser(e.target.value)}
              value={user}
            />
          </EuiFormRow>
          <EuiFormRow label="Password">
            <EuiFieldPassword
              placeholder="password123"
              onChange={(e) => setPassword(e.target.value)}
              value={password}
            />
          </EuiFormRow>
          <EuiFormRow label="Host">
            <EuiFieldText
              placeholder="host"
              onChange={(e) => setHost(e.target.value)}
              value={host}
            />
          </EuiFormRow>
          <EuiFormRow label="Port">
            <EuiFieldText
              placeholder="5439"
              onChange={(e) => setPort(e.target.value)}
              value={port}
            />
          </EuiFormRow>
          <EuiFormRow label="Database (case-sensitive)">
            <EuiFieldText
              placeholder="dev"
              onChange={(e) => setDatabase(e.target.value)}
              value={database}
            />
          </EuiFormRow>
          <EuiFormRow label="Schema (case-sensitive)">
            <EuiFieldText
              placeholder="public"
              onChange={(e) => setSchema(e.target.value)}
              value={schema}
            />
          </EuiFormRow>
        </div>
      )}
      {datasourceType === DataSourceTypes.SNOWFLAKE && (
        <div>
          <EuiPageHeader
            iconType="snowflake"
            pageTitle="Snowflake"
            description="Connect to Snowflake Data Warehouse"
          />
          <EuiHorizontalRule />
          <EuiFormRow label="Name for Data Source">
            <EuiFieldText
              placeholder="Company Data Warehouse"
              onChange={(e) => setDatasourceName(e.target.value)}
              value={datasourceName}
            />
          </EuiFormRow>
          <EuiFormRow label="Account">
            <EuiFieldText
              placeholder="abc123"
              onChange={(e) => setAccount(e.target.value)}
              value={account}
            />
          </EuiFormRow>
          <EuiFormRow label="Warehouse">
            <EuiFieldText
              placeholder="COMPUTE_WH"
              onChange={(e) => setWarehouse(e.target.value)}
              value={warehouse}
            />
          </EuiFormRow>
          <EuiFormRow label="User">
            <EuiFieldText
              placeholder="MONOSI_USER"
              onChange={(e) => setUser(e.target.value)}
              value={user}
            />
          </EuiFormRow>
          <EuiFormRow label="Password">
            <EuiFieldPassword
              placeholder="password123"
              onChange={(e) => setPassword(e.target.value)}
              value={password}
            />
          </EuiFormRow>
          <EuiFormRow label="Database (case-sensitive)">
            <EuiFieldText
              placeholder="SNOWFLAKE_SAMPLE_DATA"
              onChange={(e) => setDatabase(e.target.value)}
              value={database}
            />
          </EuiFormRow>
          <EuiFormRow label="Schema (case-sensitive)">
            <EuiFieldText
              placeholder="tpch_sf1000"
              onChange={(e) => setSchema(e.target.value)}
              value={schema}
            />
          </EuiFormRow>
        </div>
      )}
      {datasourceType === DataSourceTypes.BIGQUERY && (
        <div>
          <EuiPageHeader
            iconType={BigQueryLogo}
            pageTitle="BigQuery"
            description="Connect to Google BigQuery Data Warehouse"
          />
          <EuiHorizontalRule />
          <EuiFormRow label="Name for Data Source">
            <EuiFieldText
              placeholder="Company Data Warehouse"
              onChange={(e) => setDatasourceName(e.target.value)}
              value={datasourceName}
            />
          </EuiFormRow>
          <EuiFormRow label="Project">
            <EuiFieldText
              placeholder="abc123"
              onChange={(e) => setProject(e.target.value)}
              value={project}
            />
          </EuiFormRow>
          <EuiFormRow label="Dataset">
            <EuiFieldText
              placeholder="mydataset"
              onChange={(e) => setDataset(e.target.value)}
              value={dataset}
            />
          </EuiFormRow>
          <EuiFormRow label="Service Account JSON File">
            <EuiFilePicker
              initialPromptText="Select Service Account JSON file"
              onChange={onFileChange}
              display='default'
              aria-label="Service Account JSON File"
              accept='.json'
            />
          </EuiFormRow>
        </div>
      )}

      <EuiSpacer />

      <div>
        <EuiFormRow>
          <EuiButton
            fill
            onClick={submitForm}
            disabled={process.env.REACT_APP_IS_DEMO === 'true'}
          >
            Save
          </EuiButton>
        </EuiFormRow>
      </div>
    </div>
  );
};

export default DatasourceForm;
