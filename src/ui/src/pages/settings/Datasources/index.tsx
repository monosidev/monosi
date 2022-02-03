import React from 'react';

import DatasourceForm from 'components/forms/DatasourceForm';
import Flyout from 'components/Flyout';
import SettingsPage from 'components/SettingsPage';

import DatasourcesTable from './components/DatasourcesTable';


const SourcesSettings: React.FC = () => {
  let flyout = <Flyout name="Data Source" form={<DatasourceForm />} />

  return (
    <SettingsPage
      title="Data Sources"
      rightSideItems={[flyout]}
    >
      <DatasourcesTable />
    </SettingsPage>
  );
};

export default SourcesSettings;
