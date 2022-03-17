import React from 'react';

import IntegrationForm from 'components/forms/IntegrationForm';
import Flyout from 'components/Flyout';
import SettingsPage from 'components/SettingsPage';

import IntegrationsTable from './components/IntegrationsTable';

const IntegrationsSettings: React.FC = () => {
    let flyout = <Flyout name="Integration" form={<IntegrationForm />} />

    return (
        <SettingsPage
            title="Integrations"
            rightSideItems={[flyout]}
            >
            <IntegrationsTable />
        </SettingsPage>
    )
}

export default IntegrationsSettings;
