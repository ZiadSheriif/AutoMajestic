import axios from 'axios';

export const baseURL = 'http://127.0.0.1:5000/';


const API = axios.create({
  baseURL,
  headers: {
    'ngrok-skip-browser-warning': '69420'
  }
});

export const baseAPI = async (configObj: {
  method: string;
  url: string;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  requestConfig?: any;
}) => {
  const { method, url, requestConfig = {} } = configObj;
  const ctrl = new AbortController();



  const res = await API({
    method,
    url,
    ...requestConfig,
    signal: ctrl.signal
  });
  return res.data;
};
