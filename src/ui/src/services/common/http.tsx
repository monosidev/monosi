import { SESSION_KEY } from 'services/common/constants';

export const ROOT_URL = process.env.REACT_APP_API_URL || '/v1/api/';

export class HttpService {
  headers = {};
  url_prefix = '';
  root_url = ROOT_URL;

  constructor(url_prefix = '') {
    this.url_prefix = url_prefix;
  }

  async get(url: string, queryParams: any = null) {
    this.getHeaders();

    try {
      let response = await fetch(
        this.root_url + this.getUrl(url) + this.mapQueryParams(queryParams),
        {
          headers: this.headers,
        }
      );
      let jsonResponse = await response.json();

      return jsonResponse;
    } catch (error) {
      console.log(error);
      return null;
    }
  }

  async post(url: string, body: any, queryParams = null) {
    this.getHeaders();

    try {
      let response = await fetch(
        this.root_url + this.getUrl(url) + this.mapQueryParams(queryParams),
        {
          method: 'POST',
          headers: this.headers,
          body: JSON.stringify(body),
        }
      );
      let jsonResponse = await response.json();

      return jsonResponse;
    } catch (error) {
      console.log(error);
      return null;
    }
  }

  async put(url: string, body: any, queryParams = null) {
    this.getHeaders();

    try {
      let response = await fetch(
        this.root_url + this.getUrl(url) + this.mapQueryParams(queryParams),
        {
          method: 'PUT',
          headers: this.headers,
          body: JSON.stringify(body),
        }
      );
      let jsonResponse = await response.json();

      return jsonResponse;
    } catch (error) {
      console.log(error);
      return null;
    }
  }

  async remove(url: string, queryParams: any = null) {
    this.getHeaders();

    try {
      let response = await fetch(
        ROOT_URL + this.getUrl(url) + this.mapQueryParams(queryParams),
        {
          method: 'DELETE',
          headers: this.headers,
        }
      );
      let jsonResponse = await response.json();

      return jsonResponse;
    } catch (error) {
      console.log(error);

      return null;
    }
  }

  getUrl(url: string) {
    return this.url_prefix + url;
  }

  getHeaders() {
    this.headers = {
      'Content-Type': 'application/json',
      Accept: 'application/json',
    };
    if (this.checkSession()) {
      let jwtToken = this.getSession();
      this.headers = {
        ...this.headers,
        Authorization: `Bearer ${jwtToken}`,
      };
    }
  }

  getSession() {
    let session = localStorage.getItem(SESSION_KEY);
    return session;
  }

  checkSession() {
    return localStorage.getItem(SESSION_KEY) !== null;
  }

  mapQueryParams(queryParams: any) {
    return queryParams
      ? Object.keys(queryParams)
          .map(function (key) {
            return key + '=' + queryParams[key];
          })
          .join('&')
      : '';
  }
}
