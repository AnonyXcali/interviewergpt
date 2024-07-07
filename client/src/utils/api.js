import axios from 'axios';

const api = axios.create({
  baseURL: 'http://34.132.153.144:5000',
});

export default api;
