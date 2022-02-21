import { BaseService } from 'services/common/base';

class DatasourceService extends BaseService {
  constructor() {
    super('datasources');
  }

  test(ds_id: any) {
        console.log("Not implemented.");
  }
}

export default new DatasourceService();
