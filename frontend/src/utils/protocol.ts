import axios from "axios";
import {API_BASE_URL} from "../shared-constants.ts";

// Instance Initialization --------------------------------------
const protocol = axios.create({
  baseURL: API_BASE_URL,
  timeout: 1000,
  withCredentials: true,
  responseType: "json",
  xsrfHeaderName: "X-CSRF-Token"
});

protocol.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response) {
      if (error.response.data) {
        return Promise.reject(error.response.data.error_code);
      } else
        return Promise.reject(error.response.status | 0x40000000);
    } else {
      return Promise.reject(0x7fffffff);
    }
  }
);

// API Functions ------------------------------------------------
export function login(username: string, password: string,
                      successCallback: (data: any) => void, errorCallback: (errorCode: number) => void) {
  protocol.post("/login", {
    username: username,
    password: password
  }).then(
    (data) => successCallback(data),
    (errorCode) => errorCallback(errorCode)
  );
}

// Error Codes --------------------------------------------------
export const ERROR_CODE_MAP = {
  0x7fffffff: "无法连接到服务器，请稍后再试！",
  1073742228: "无法访问服务器API，请稍后再试！" // 0x40000000 + 404
};