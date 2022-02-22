import { BaseService } from 'services/common/base';

class DatasourceService extends BaseService {
  constructor() {
    super('datasources');
  }

  async test(id: string) {
    return await this.http.get(`/${id}/test`);
  }
}

export default new DatasourceService();
