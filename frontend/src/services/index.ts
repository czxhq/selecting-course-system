import { AxiosHeaders } from 'axios'
import { BASE_URL, TIME_OUT } from './config'
import AxiosRequest from './request'

const axiosrequest = new AxiosRequest({
  baseURL: BASE_URL,
  timeout: TIME_OUT,
  headers: new AxiosHeaders()
})

export default axiosrequest
