import { EuiButton, EuiCard, EuiFieldText, EuiFlexGrid, EuiFlexItem, EuiFormRow, EuiHorizontalRule, EuiIcon, EuiLink, EuiPageHeader, EuiSpacer, EuiText } from '@elastic/eui';
import React, { useState } from 'react';
import { PagerDutyLogo, WebhookLogo } from 'images';
import IntegrationService from 'services/integrations';

// TODO: Currently only configured for Slack

const IntegrationForm: React.FC = () => {
  const [connectorName, setConnectorName] = useState('');
  const [slackWebhookUrl, setSlackWebhookUrl] = useState('');

  const handleClick = async () => {
    const body = {
      name: connectorName,
      type: 'slack',
      config: {
        url: slackWebhookUrl,
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
              onClick: undefined,
              isSelected: true,
              isDisabled: false,
            }}
            title="Slack"
            description="Send a message to a Slack channel or user"
          />
        </EuiFlexItem>
        <EuiFlexItem>
          <EuiCard
            isDisabled
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
        <EuiFlexItem>
          <EuiCard
            isDisabled
            selectable={{
              onClick: undefined,
              isSelected: false,
              isDisabled: true,
            }}
            icon={<EuiIcon type={WebhookLogo} size="xl" />}
            title="Webhook"
            description="Send a request to a web service."
          />
        </EuiFlexItem>
      </EuiFlexGrid>
      <EuiSpacer />
      <EuiHorizontalRule />
      <EuiPageHeader
        iconType="logoSlack"
        pageTitle="Slack Connector"
        description="Send a message to a Slack channel or user."
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
          value={slackWebhookUrl}
          onChange={(e: any) => setSlackWebhookUrl(e.target.value)}
        />
      </EuiFormRow>
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
