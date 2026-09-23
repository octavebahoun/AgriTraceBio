import axios, { AxiosError } from 'axios'

const TOKEN_KEY = 'agritrace_token'

export const api = axios.create({
  baseURL: '/api',
  timeout: 15000,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem(TOKEN_KEY)
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (r) => r,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      localStorage.removeItem(TOKEN_KEY)
      if (!window.location.pathname.startsWith('/login') &&
          !window.location.pathname.startsWith('/trace')) {
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  },
)

export const authStorage = {
  get: () => localStorage.getItem(TOKEN_KEY),
  set: (t: string) => localStorage.setItem(TOKEN_KEY, t),
  clear: () => localStorage.removeItem(TOKEN_KEY),
}
