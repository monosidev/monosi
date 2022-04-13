import React, { useEffect, useState } from 'react';
import { Button, Form } from 'react-bootstrap';

import UserService from 'services/users';

const OnboardingGettingStarted: React.FC = () => {
  const [email, setEmail] = useState('');
  const [anonymizeUsageData, setAnonymizeUsageData] = useState(false);
  const [receiveUpdates, setReceiveUpdates] = useState(true);

  const handleSubmit = async () => {
    const body = {
      email: email,
      anonymize_usage_data: anonymizeUsageData,
      receive_updates: receiveUpdates,
    };

    const resp = await UserService.create(body);

    window.location.reload(); // TODO: Fix - dirty
  };

  return (
  <div className="bg-light faux-body">
    <div className="container">
      <div className="py-5">
        <img className="d-block mx-auto mb-4" src="https://www.monosi.dev/images/monosi_logo.png" alt="" width="72" height="57" />
        <div className="col-md-4 mx-auto">
          <div className="h-100 p-5 border rounded-3" style={{backgroundColor: 'white'}}>
          <div className="text-center">
            <h2>Welcome to MonoSi</h2>
            <p className="lead">OSS Data Observability</p>
          </div>
          <Form className="mb-5" onSubmit={handleSubmit}>
            <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Label>Email address</Form.Label>
                <Form.Control type="email" placeholder="Enter email" onChange={(e) => setEmail(e.target.value)} />
              </Form.Group>

              <Form.Group className="mb-3" controlId="anonymize">
                <Form.Check type="checkbox" label="Anonymize usage data" onChange={(e) => setAnonymizeUsageData(e.target.checked)} />
              </Form.Group>
              <Form.Group className="mb-3" controlId="updates">
                <Form.Check type="checkbox" label="Receive updates" defaultChecked={true} onChange={(e) => setReceiveUpdates(e.target.checked)} />
              </Form.Group>
              <Button variant="primary" type="submit" style={{"float": "right"}}>
                Continue
              </Button>
            </Form>
          </div>
        </div>
      </div>
    </div>
  </div>
  );
};

export default OnboardingGettingStarted;

