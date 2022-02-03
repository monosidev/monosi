import { BaseService } from 'services/common/base';

class IntegrationService extends BaseService {
  constructor() {
    super('integrations');
  }
}

export default new IntegrationService();
