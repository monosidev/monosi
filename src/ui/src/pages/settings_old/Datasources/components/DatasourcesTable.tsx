import React, { useState, useEffect } from 'react';
import {
  EuiEmptyPrompt,
  EuiInMemoryTable,
  EuiPopover,
  EuiButtonIcon,
  EuiContextMenuPanel,
  EuiContextMenuItem,
  EuiGlobalToastList,
} from '@elastic/eui';

import datasourceService from 'services/datasources';

const DatasourcesTable: React.FC = () => {
  const [datasources, setDatasources] = useState<any[]>([{name: "mock data", type: "postgres", created_at: Date.now(), id: 1}]);
  const [loading, setLoading] = useState<boolean>(false);
  const [testing, setTesting] = useState<boolean>(false);
  // TODO: Componentize this
  const [toasts, setToasts] = useState<any[]>([]);

  const [itemIdToOpenActionsPopoverMap, setItemIdToOpenActionsPopoverMap] =
    useState<{ [key: string]: boolean }>({});

  useEffect(() => {
    async function loadDatasources() {
      setLoading(true);
      let res = await datasourceService.getAll();
      if (res !== null && res.datasources) {
        setDatasources(res.datasources);
      }
      setLoading(false);
    }
    loadDatasources();
  }, []);

  const emptyState = (
    <EuiEmptyPrompt
      title={<h3>No data sources</h3>}
      titleSize="xs"
      body="Looks like you haven&rsquo;t connected any data sources. Let&rsquo;s create your first connection!"
    />
  );

  const columns = [
    {
      field: 'name',
      name: 'Name',
    },
    {
      field: 'type',
      name: 'Connection Type',
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
                  key="test"
                  icon="temperature"
                  disabled={process.env.REACT_APP_IS_DEMO === 'true'}
                  onClick={() => {
                    testConnectionDatasource(item.id);
                  }}
                >
                  Test Connection
                </EuiContextMenuItem>,
                <EuiContextMenuItem
                  key="delete"
                  icon="trash"
                  disabled={process.env.REACT_APP_IS_DEMO === 'true'}
                  onClick={() => {
                    deleteDatasource(item.id);
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

  const deleteDatasource = (itemId: any) => {
    const response = datasourceService.delete(itemId);
    // remove user from state based on response
    closePopover(itemId);

    window.location.reload();
  };

  const testConnectionDatasource = async (itemId: any) => {
    setTesting(true)
    const response = await datasourceService.test(itemId);
    if (response && response.status) {
      setToasts(toasts.concat(testConnectionSuccessToast));
    } else {
      setToasts(toasts.concat(testConnectionFailedToast));
    }

    setTesting(false)
  };

  const testConnectionSuccessToast = {
    title: 'Connection successful',
    color: 'success',
  };

  const testConnectionFailedToast = {
    title: 'Connection failed',
    color: 'danger',
    iconType: 'help',
    text: <p>Check your connection settings and try again.</p>,
  };

  const removeToast = (removedToast: any) => {
    setToasts(toasts.filter((toast) => toast.id !== removedToast.id));
  };

  return (
    <>
      <EuiInMemoryTable
        items={datasources}
        message={emptyState}
        loading={loading}
        columns={columns}
        pagination={false}
      />
      <EuiGlobalToastList
        toasts={toasts}
        dismissToast={removeToast}
        toastLifeTimeMs={5000}
      />
    </>
  );
};

export default DatasourcesTable;
