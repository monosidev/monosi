import { BaseService } from 'services/common/base';

class ExecutionService extends BaseService {
  constructor() {
    super('executions');
  }
}

export default new ExecutionService();

