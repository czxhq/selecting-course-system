import axios from 'axios'
import type { AxiosInstance } from 'axios'
import type { AxiosReqConfig } from './type'
class AxiosRequest {
  instance: AxiosInstance

  constructor(config: AxiosReqConfig) {
    this.instance = axios.create(config)
    this.instance.interceptors.request.use(
      (config) => {
        return config
      },
      (err) => {
        return err
      }
    )
    this.instance.interceptors.response.use(
      (config) => {
        return config
      },
      (err) => {
        return err
      }
    )

    this.instance.interceptors.request.use(
      config.interceptors?.onfulfilledReq,
      config.interceptors?.onrejectedReq
    )
    this.instance.interceptors.response.use(
      config.interceptors?.onfulfilledRes,
      config.interceptors?.onrejectedRes
    )
  }

  request<T = any>(config: AxiosReqConfig<T>) {
    if (config.interceptors?.onfulfilledReq) {
      config = config.interceptors.onfulfilledReq(config)
    }
    return new Promise<T>((resolve, reject) => {
      this.instance
        .request<any, T>(config)
        .then((res) => {
          if (config.interceptors?.onfulfilledRes) {
            res = config.interceptors.onfulfilledRes(res)
          }
          resolve(res)
        })
        .catch((err) => {
          reject(err)
        })
    })
  }

  get<T = any>(config: AxiosReqConfig<T>) {
    return this.request({ ...config, method: 'GET' })
  }

  post<T = any>(config: AxiosReqConfig<T>) {
    return this.request({ ...config, method: 'POST' })
  }

  delete<T = any>(config: AxiosReqConfig<T>) {
    return this.request({ ...config, method: 'DELETE' })
  }

  patch<T = any>(config: AxiosReqConfig<T>) {
    return this.request({ ...config, method: 'PATCH' })
  }
}

export default AxiosRequest
