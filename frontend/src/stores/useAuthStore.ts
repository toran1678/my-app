import { create } from 'zustand';
import { apiService, User } from '../services/api';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  setLoading: (loading: boolean) => void;
  getCurrentUser: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  isAuthenticated: false,
  isLoading: false,
  
  // 로그인 함수 - 실제 API 호출
  login: async (email: string, password: string) => {
    set({ isLoading: true });
    
    try {
      // 1. 로그인 API 호출하여 토큰 받기
      const loginResponse = await apiService.login(email, password);
      
      // 2. 토큰을 API 서비스에 저장
      apiService.setToken(loginResponse.access_token);
      
      // 3. 현재 사용자 정보 가져오기
      const user = await apiService.getCurrentUser();
      
      // 4. 상태 업데이트
      set({ 
        user, 
        isAuthenticated: true, 
        isLoading: false 
      });
      
    } catch (error) {
      console.error('로그인 실패:', error);
      set({ isLoading: false });
      throw error;
    }
  },
  
  // 로그아웃 함수
  logout: () => {
    apiService.setToken(null);
    set({ user: null, isAuthenticated: false });
  },
  
  // 로딩 상태 설정
  setLoading: (isLoading: boolean) => set({ isLoading }),
  
  // 현재 사용자 정보 가져오기
  getCurrentUser: async () => {
    try {
      const user = await apiService.getCurrentUser();
      set({ user, isAuthenticated: true });
    } catch (error) {
      console.error('사용자 정보 가져오기 실패:', error);
      set({ user: null, isAuthenticated: false });
    }
  },
}));
