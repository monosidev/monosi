import React, { useState } from 'react';
import { EuiButton, EuiCard, EuiFieldText, EuiFlexGrid, EuiFlexItem, EuiFormRow, EuiHorizontalRule, EuiIcon, EuiLink, EuiPageHeader, EuiSpacer, EuiText } from '@elastic/eui';

import { PagerDutyLogo, WebhookLogo } from 'images';
import IntegrationService from 'services/integrations';

enum IntegrationTypes {
  SLACK = 'slack',
  WEBHOOK = 'webhook',
}

const IntegrationForm: React.FC = () => {
  const [integrationType, setIntegrationType] = useState<IntegrationTypes>(
    IntegrationTypes.SLACK
  );
  const [connectorName, setConnectorName] = useState('');
  const [webhookUrl, setWebhookUrl] = useState('');

  const handleClick = async () => {
    const body = {
      name: connectorName,
      type: integrationType,
      config: {
        url: webhookUrl,
      },
    };
    const resp = await IntegrationService.create(body);

    window.location.reload(); // TODO: Fix - dirty
  };

  return (
    <div>
      <EuiFlexGrid columns={3}>
        <EuiFlexItem>
          <EuiCard
            icon={<EuiIcon type="logoSlack" size="xl" />}
            selectable={{
              onClick: () => setIntegrationType(IntegrationTypes.SLACK),
              isSelected: integrationType === IntegrationTypes.SLACK,
              isDisabled: false,
            }}
            title="Slack"
            description="Send a message to a Slack channel or user"
          />
        </EuiFlexItem>
        <EuiFlexItem>
          <EuiCard
            selectable={{
              onClick: () => setIntegrationType(IntegrationTypes.WEBHOOK),
              isSelected: integrationType === IntegrationTypes.WEBHOOK,
              isDisabled: false,
            }}
            icon={<EuiIcon type={WebhookLogo} size="xl" />}
            title="Webhook"
            description="Send a request to a web service."
          />
        </EuiFlexItem>
        <EuiFlexItem>
          <EuiCard
            selectable={{
              onClick: undefined,
              isSelected: false,
              isDisabled: true,
            }}
            icon={<EuiIcon type={PagerDutyLogo} size="xl" />}
            title="PagerDuty"
            description="Send an event in PagerDuty."
          />
        </EuiFlexItem>
      </EuiFlexGrid>
      <EuiSpacer />
      <EuiHorizontalRule />

      {integrationType === IntegrationTypes.SLACK && (
              <div>
              <EuiPageHeader
                iconType="logoSlack"
                pageTitle="Slack Connector"
                description="Send a message to a Slack channel or user by using Slack Incoming Webhooks."
              />
              <EuiHorizontalRule />
              <EuiFormRow label="Connector name">
                <EuiFieldText
                  value={connectorName}
                  onChange={(e: any) => setConnectorName(e.target.value)}
                />
              </EuiFormRow>
              <EuiSpacer />
              <EuiText size="m">
                <span>Connector Settings</span>
              </EuiText>
              <EuiSpacer size="s" />
              <EuiFormRow
                label="Webhook URL"
                helpText={
                  <EuiLink href={'https://api.slack.com/messaging/webhooks'} target="_blank">
                    Create a Slack Webhook URL
                  </EuiLink>
                }
              >
                <EuiFieldText
                  value={webhookUrl}
                  onChange={(e: any) => setWebhookUrl(e.target.value)}
                />
              </EuiFormRow>
      </div>
      )}
      {integrationType === IntegrationTypes.WEBHOOK && (
              <div>
              <EuiPageHeader
                iconType="logoWebhook"
                pageTitle="Webhook Connector"
                description="Send a JSON body with anomaly information to a webhook"
              />
              <EuiHorizontalRule />
              <EuiFormRow label="Connector name">
                <EuiFieldText
                  value={connectorName}
                  onChange={(e: any) => setConnectorName(e.target.value)}
                />
              </EuiFormRow>
              <EuiSpacer />
              <EuiText size="m">
                <span>Connector Settings</span>
              </EuiText>
              <EuiSpacer size="s" />
              <EuiFormRow
                label="Webhook URL"
                helpText={
                  <EuiLink href={'https://docs.monosi.dev/docs/integrations/webhooks'} target="_blank">
                    Learn more about what information the webhook body contains.
                  </EuiLink>
                }
              >
                <EuiFieldText
                  value={webhookUrl}
                  onChange={(e: any) => setWebhookUrl(e.target.value)}
                />
              </EuiFormRow>
      </div>
      )}

      <EuiSpacer />
      <EuiButton 
        fill 
        onClick={handleClick}
        disabled={process.env.REACT_APP_IS_DEMO === 'true'}
      >
        Create
      </EuiButton>
    </div>
  );
}
export default IntegrationForm;
