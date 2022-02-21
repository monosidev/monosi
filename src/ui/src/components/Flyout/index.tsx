import React, { useState } from 'react';
import {
  Button,
  Offcanvas,
} from 'react-bootstrap';

import './flyout.css';

const Flyout = ({name, form}: any) => {
  const [isFlyoutVisible, setIsFlyoutVisible] = useState(false);

  const handleClose = () => setIsFlyoutVisible(false);
  const handleShow = () => setIsFlyoutVisible(true);

  return (
    <>
      <Button variant="primary" onClick={handleShow}>
        Create {name}
      </Button>

      <Offcanvas 
        show={isFlyoutVisible} 
        onHide={handleClose}
        placement="end">
        <Offcanvas.Header closeButton>
          <Offcanvas.Title>Create {name}</Offcanvas.Title>
        </Offcanvas.Header>
        <Offcanvas.Body>
          {form}
        </Offcanvas.Body>
      </Offcanvas>
    </>
  );
}

export default Flyout;
