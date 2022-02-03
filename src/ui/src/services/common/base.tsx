import { HttpService } from './http';

export class BaseService {
  http;

  constructor(url_prefix = '') {
    this.http = new HttpService(url_prefix);
  }

  async getAll() {
    return await this.http.get(``);
  }

  async get(id: string) {
    return await this.http.get(`/${id}`);
  }

  async create(body: any) {
    return await this.http.post(``, body);
  }

  async update(id: string, body: any) {
    return await this.http.put(`/${id}`, body);
  }

  async delete(id: string) {
    return await this.http.remove(`/${id}`);
  }
}
