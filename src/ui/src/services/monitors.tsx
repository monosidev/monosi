import { BaseService } from 'services/common/base';

class MonitorService extends BaseService {
  constructor() {
    super('monitors');
  }

  async getMetrics(id: string, ) {
    return await this.http.get(`/${id}/metrics`);
  }

  async getMetricData(id: string, column_name: string, metric: string) {
    return await this.http.get(`/${id}/metrics?column_name=${column_name}&metric=${metric}`);
  }
}

export default new MonitorService();
