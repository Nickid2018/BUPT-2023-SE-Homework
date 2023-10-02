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
      return Promise.reject(error.response.data.error_code);
    } else {
      return Promise.reject(-1);
    }
  }
);

// API Functions ------------------------------------------------
export function login(username: string, password: string,
                      successCallback: () => void, errorCallback: (errorCode: number) => void) {
  protocol.post("/login", {
    username: username,
    password: password
  }).then(
    (data) => successCallback(),
    (errorCode) => errorCallback(errorCode)
  );
}

// Error Codes --------------------------------------------------
export const ERROR_CODE_MAP = {

};