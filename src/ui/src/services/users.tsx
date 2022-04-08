import { BaseService } from 'services/common/base';

class UserService extends BaseService {
  constructor() {
    super('users');
  }
}

export default new UserService();

