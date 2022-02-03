import React, { useState, useEffect } from 'react';

import { EuiSpacer, EuiSearchBar } from '@elastic/eui';

const initialQuery = EuiSearchBar.Query.MATCH_ALL;

const SearchAndFilters: React.FC<{ setTableQuery: any; monitors: any }> = ({
  setTableQuery,
  monitors,
}) => {
  const [query, setQuery] = useState(initialQuery);
  const [error, setError] = useState(null);

  useEffect(() => {
    setTableQuery(query);
  }, [query]);

  const onChange = ({ query, error }: any) => {
    if (error) {
      setError(error);
    } else {
      setError(null);
      setQuery(query);
    }
  };

  const distinct = (value: any, index: any, self: any) => {
    return self.indexOf(value) === index;
  };

  const renderSearch = () => {
    const filters = [
      {
        type: 'field_value_selection' as 'field_value_selection',
        field: 'type',
        name: 'Type',
        options: monitors
          ? monitors
              .map((monitor: any) => monitor.type)
              .filter(distinct)
              .map((el: any) => {
                return { value: el };
              })
          : [],
        onChange: onChange,
      },
      {
        type: 'field_value_selection' as 'field_value_selection',
        field: 'datasource',
        name: 'Source',
        options: monitors
          ? monitors
              .map((monitor: any) => monitor.datasource)
              .filter(distinct)
              .map((el: any) => {
                return { value: el };
              })
          : [],
        onChange: onChange,
      },
    ];

    return (
      <EuiSearchBar
        defaultQuery={initialQuery}
        box={{
          placeholder: 'Search monitors...',
          incremental: true,
        }}
        filters={filters}
        onChange={onChange}
      />
    );
  };

  return (
    <>
      <EuiSpacer size="l" />
      {renderSearch()}
    </>
  );
};

export default SearchAndFilters;
