import type { InternalAxiosRequestConfig, AxiosResponse } from 'axios'
export interface AxiosInterceptor<T> {
  onfulfilledReq?: (
    config: InternalAxiosRequestConfig
  ) => InternalAxiosRequestConfig
  onrejectedReq?: (err: any) => any
  onfulfilledRes?: (res: T) => T
  onrejectedRes?: (err: any) => any
}

export interface AxiosReqConfig<T = AxiosResponse>
  extends InternalAxiosRequestConfig {
  interceptors?: AxiosInterceptor<T>
}
