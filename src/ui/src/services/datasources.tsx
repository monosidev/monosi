import { BaseService } from 'services/common/base';

class DatasourceService extends BaseService {
  constructor() {
    super('datasources');
  }
}

export default new DatasourceService();
