import React from 'react';
import { CloudDownloadFill, PersonCircle, Tools } from 'react-bootstrap-icons';
import BootstrapPage from 'components/BootstrapPage';

import ProfileForm from 'components/forms/ProfileForm';

const ProfileSettings: React.FC = () => {
  return (
      <BootstrapPage selectedTab="settings">
         <div style={{paddingLeft: 96}} className="bg-light">
           <div className="container">
             <main className="col-md-12 ms-sm-auto col-lg-12">
               <div className="container">
                  <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
                     <h1 className="h2">Settings</h1>
                     <div className="btn-toolbar mb-2 mb-md-0">
                     </div>
                  </div>
                  <div className="d-flex align-items-start">
                     <div className="nav flex-column nav-pills me-3 col-md-3" id="v-pills-tab" role="tablist" aria-orientation="vertical">
                        <div className="list-group">
                           <a href="/settings/profile" className="list-group-item list-group-item-action active" aria-current="true">
                              <div className="d-flex w-100">
                                 <PersonCircle className="bi" width="24" height="24" />
                                 <h5 className="mb-1 mx-3">Profile</h5>
                              </div>
                              <small>Edit account details</small>
                           </a>
                           <a href="/settings/sources" className="list-group-item list-group-item-action">
                              <div className="d-flex w-100">
                                 <CloudDownloadFill className="bi" width="24" height="24" />
                                 <h5 className="mb-1 mx-3">Data Sources</h5>
                              </div>
                              <small className="text-muted">Manage connected data sources</small>
                           </a>
                           <a href="/settings/integrations" className="list-group-item list-group-item-action">
                              <div className="d-flex w-100">
                                 <Tools className="bi" width="24" height="24" />
                                 <h5 className="mb-1 mx-3">Integrations</h5>
                              </div>
                              <small className="text-muted">Manage third-party connections</small>
                           </a>
                        </div>
                     </div>
                     <div className="tab-content w-100 mx-4" id="v-pills-tabContent">
                        <div className="tab-pane fade show active" id="v-pills-home" role="tabpanel" aria-labelledby="v-pills-home-tab">
                           <div className="d-flex flex-wrap justify-content-center">
                              <form className="col-12 col-lg-auto mb-2 mb-lg-0 me-lg-auto">
                                 <h2>Profile</h2>
                              </form>
                           </div>
                           <hr className="mb-4" />
                           <ProfileForm />
                        </div>
                     </div>
                  </div>
               </div>
             </main>
           </div>
         </div>
      </BootstrapPage>
  );
};

export default ProfileSettings;
