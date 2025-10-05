import { API_BASE_URL, apiSettings } from '../config/api';

// API 응답 타입 정의
export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface User {
  id: number;
  email: string;
  username: string;
  full_name: string;
  is_active: boolean;
  created_at: string;
}

// API 클래스
class ApiService {
  private baseURL: string;
  private token: string | null = null;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  // 토큰 설정
  setToken(token: string | null) {
    this.token = token;
  }

  // 기본 요청 헤더
  private getHeaders(): HeadersInit {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    if (this.token) {
      headers.Authorization = `Bearer ${this.token}`;
    }

    return headers;
  }

  // 요청 실행 (타임아웃 및 재시도 포함)
  private async makeRequest(
    url: string, 
    options: RequestInit, 
    retryCount: number = 0
  ): Promise<Response> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), apiSettings.timeout);

    try {
      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
      });
      
      clearTimeout(timeoutId);
      return response;
    } catch (error) {
      clearTimeout(timeoutId);
      
      // 재시도 로직
      if (retryCount < apiSettings.retryAttempts) {
        console.log(`요청 실패, ${apiSettings.retryDelay}ms 후 재시도... (${retryCount + 1}/${apiSettings.retryAttempts})`);
        await new Promise(resolve => setTimeout(resolve, apiSettings.retryDelay));
        return this.makeRequest(url, options, retryCount + 1);
      }
      
      throw error;
    }
  }

  // 로그인 API
  async login(email: string, password: string): Promise<LoginResponse> {
    try {
      // JSON 형태로 로그인 시도
      const response = await this.makeRequest(`${this.baseURL}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: email,
          password: password,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `로그인에 실패했습니다. (${response.status})`);
      }

      return response.json();
    } catch (error) {
      throw error;
    }
  }

  // 현재 사용자 정보 조회 API
  async getCurrentUser(): Promise<User> {
    const response = await this.makeRequest(`${this.baseURL}/api/auth/me`, {
      method: 'GET',
      headers: this.getHeaders(),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || '사용자 정보를 가져올 수 없습니다.');
    }

    return response.json();
  }

  // 회원가입 API (임시로 사용)
  async register(email: string, username: string, fullName: string, password: string): Promise<User> {
    const response = await this.makeRequest(`${this.baseURL}/api/users/`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({
        email,
        username,
        full_name: fullName,
        password,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || '회원가입에 실패했습니다.');
    }

    return response.json();
  }
}

// 싱글톤 인스턴스 생성 (환경변수 사용)
export const apiService = new ApiService();
