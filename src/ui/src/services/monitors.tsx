import { BaseService } from 'services/common/base';

class MonitorService extends BaseService {
  constructor() {
    super('monitors');
  }

  async getMetrics(database: string, schema: string, table: string) {
    return await this.http.get(`/${database}/${schema}/${table}/metrics`);
  }

  async getMetricData(database: string, schema: string, table: string, column_name: string, metric: string) {
    return await this.http.get(`/${database}/${schema}/${table}/metrics?column_name=${column_name}&metric=${metric}`);
  }
}

export default new MonitorService();
