import React, { useState, useEffect } from 'react';
import {
  EuiEmptyPrompt,
  EuiInMemoryTable,
  EuiPopover,
  EuiButtonIcon,
  EuiContextMenuPanel,
  EuiContextMenuItem,
} from '@elastic/eui';

import IntegrationService from 'services/integrations';

// TODO: Abstract component for integrations and datasources tables.

const IntegrationsTable: React.FC = () => {
  const [itemIdToOpenActionsPopoverMap, setItemIdToOpenActionsPopoverMap] =
    useState<{ [key: string]: boolean }>({});

  const [integrations, setIntegrations] = useState([]);
  const [message, setMessage] = useState(<>Loading integrations...</>);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const emptyState = (
      <EuiEmptyPrompt
        title={<h3>No integrations</h3>}
        titleSize="xs"
        body="Looks like you haven&rsquo;t created any integrations. Let&rsquo;s create your first integration!"
      />
    );

    async function loadIntegrations() {
      let res = await IntegrationService.getAll();
      if (res !== null && res.integrations) {
        setIntegrations(res.integrations);

        if (res.integrations.length === 0) {
          setMessage(emptyState);
        }
      } else {
        setMessage(emptyState);
      }
    }

    loadIntegrations();
  }, []);

  const togglePopover = (itemId: any) => {
    const isPopped: boolean = !itemIdToOpenActionsPopoverMap[itemId];
    const newItemIdToOpenActionsPopoverMap: any = {
      ...itemIdToOpenActionsPopoverMap,
      [itemId]: isPopped,
    };

    setItemIdToOpenActionsPopoverMap(newItemIdToOpenActionsPopoverMap);
  };

  const closePopover = (itemId: any) => {
    // only update the state if this item's popover is open
    if (isPopoverOpen(itemId)) {
      const newItemIdToOpenActionsPopoverMap: any = {
        ...itemIdToOpenActionsPopoverMap,
        [itemId]: false,
      };

      setItemIdToOpenActionsPopoverMap(newItemIdToOpenActionsPopoverMap);
    }
  };

  const isPopoverOpen = (itemId: any) => {
    return itemIdToOpenActionsPopoverMap[itemId];
  };

  const deleteIntegration = async (itemId: any) => {
    const response = await IntegrationService.delete(itemId);

    // Update state instead
    // closePopover(itemId);
    window.location.reload();
  };

  const columns = [
    {
      field: 'name',
      name: 'Name',
    },
    {
      field: 'type',
      name: 'Integration Type',
    },
    {
      field: 'created_at',
      name: 'Created At',
    },
    {
      name: 'Actions',
      render: (item: any) => {
        return (
          <EuiPopover
            id={`${item.id}-actions`}
            button={
              <EuiButtonIcon
                aria-label="Actions"
                iconType="gear"
                size="s"
                color="text"
                onClick={() => togglePopover(item.id)}
              />
            }
            isOpen={isPopoverOpen(item.id)}
            closePopover={() => closePopover(item.id)}
            panelPaddingSize="none"
            anchorPosition="leftCenter"
          >
            <EuiContextMenuPanel
              items={[
                <EuiContextMenuItem
                  key="C"
                  icon="trash"
                  onClick={() => {
                    deleteIntegration(item.id);
                  }}
                >
                  Delete
                </EuiContextMenuItem>,
              ]}
            />
          </EuiPopover>
        );
      },
    },
  ];

  return (
    <>
      <EuiInMemoryTable
        items={integrations}
        message={message}
        loading={loading}
        columns={columns}
        pagination={true}
      />
    </>
  );
};

export default IntegrationsTable;
