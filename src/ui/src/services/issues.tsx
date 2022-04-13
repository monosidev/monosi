import { BaseService } from 'services/common/base';

class IssueService extends BaseService {
  constructor() {
    super('issues');
  }
}

export default new IssueService();

