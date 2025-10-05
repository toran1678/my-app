// API 설정
export const API_CONFIG = {
  // 개발 환경
  development: {
    baseURL: 'http://10.0.2.2:8000', // Android 에뮬레이터용
  },
  // 프로덕션 환경
  production: {
    baseURL: process.env.EXPO_PUBLIC_API_URL || 'https://your-api-domain.com',
  },
  // 테스트 환경
  test: {
    baseURL: 'http://10.0.2.2:8000', // Android 에뮬레이터용
  },
};

// 현재 환경에 따른 API URL 가져오기
const getApiUrl = (): string => {
  const env = process.env.NODE_ENV || 'development';
  return API_CONFIG[env as keyof typeof API_CONFIG]?.baseURL || API_CONFIG.development.baseURL;
};

// 환경변수에서 API URL 가져오기 (우선순위)
export const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL || getApiUrl();

// API 설정 객체
export const apiSettings = {
  baseURL: API_BASE_URL,
  timeout: 10000, // 10초
  retryAttempts: 3,
  retryDelay: 1000, // 1초
};

console.log('API Base URL:', API_BASE_URL);
