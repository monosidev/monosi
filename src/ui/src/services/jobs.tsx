import { BaseService } from 'services/common/base';

class JobService extends BaseService {
  constructor() {
    super('jobs');
  }
}

export default new JobService();


