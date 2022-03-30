import React from 'react';

import { Alarm, Book, Collection, GearFill, HouseDoor, PersonCircle } from 'react-bootstrap-icons';

const Navigation: React.FC<{selectedTab: string}> = ({selectedTab}: any) => {

  const classSelector = (tabName: string) => {
    const nonActiveClassNames = "nav-link py-3 border-bottom";

    if (selectedTab === tabName) {
      return "active " + nonActiveClassNames;
    }
    return nonActiveClassNames;
  }

  return (
    <nav id="sidebarMenu" className="d-md-block bg-light sidebar collapse">
      <div className="position-sticky d-flex">

        <div className="d-flex flex-column flex-shrink-0 bg-light" style={{width: '4.5rem'}}>
          <a href="/" className="d-block p-3 link-dark text-decoration-none" title="Monosi" data-bs-toggle="tooltip" data-bs-placement="right">
            <img src="https://www.monosi.dev/images/monosi_logo.png" className="bi" width="40" height="32" />
            <span className="visually-hidden">Monosi</span>
          </a>
          <ul className="nav nav-pills nav-flush flex-column mb-auto text-center">
            <li className="nav-item">
              <a href="/" className={classSelector('dashboard') + " border-top"} aria-current="page" title="Home" data-bs-toggle="tooltip" data-bs-placement="right">
                <HouseDoor className="bi" width={24} height={24} />
              </a>
            </li>
            <li>
              <a href="/monitors" className={classSelector('monitors')} title="Monitors" data-bs-toggle="tooltip" data-bs-placement="right">
                <Collection className="bi" width={24} height={24} />
              </a>
            </li>
            <li>
              <a href="/executions" className={classSelector('executions')} title="Executions" data-bs-toggle="tooltip" data-bs-placement="right">
                <Alarm className="bi" width={24} height={24} />
              </a>
            </li>
            <li>
              <a href="/settings" className={classSelector('settings')} title="Settings" data-bs-toggle="tooltip" data-bs-placement="right">
                <GearFill className="bi" width={24} height={24} />
              </a>
            </li>
          </ul>
          <div className="border-top">
            <a target="_blank" href="https://docs.monosi.dev" className="nav-link py-3 d-flex align-items-center justify-content-center" title="Documentation" data-bs-toggle="tooltip" data-bs-placement="right">
              <Book className="bi" width={24} height={24} />
            </a>
          </div>
          {/* <div className="dropdown border-top">
            <a href="#" className="d-flex align-items-center justify-content-center p-3 text-decoration-none dropdown-toggle" id="dropdownUser3" data-bs-toggle="dropdown" aria-expanded="false">
              <PersonCircle className="bi" width={24} height={24} />
            </a>
            <ul className="dropdown-menu text-small shadow" aria-labelledby="dropdownUser3">
              <li><a className="dropdown-item" href="#">New project...</a></li>
              <li><a className="dropdown-item" href="#">Settings</a></li>
              <li><a className="dropdown-item" href="#">Profile</a></li>
              <li><hr className="dropdown-divider" /></li>
              <li><a className="dropdown-item" href="#">Sign out</a></li>
            </ul>
          </div> */ }
        </div>

        <div className="b-example-divider"></div>
      </div>
    </nav>
  );
};

export default Navigation;
