import { BaseService } from 'services/common/base';

class MonitorService extends BaseService {
  constructor() {
    super('monitors');
  }
}

export default new MonitorService();
