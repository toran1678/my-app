import React, { useState } from 'react';
import { View, Text, StyleSheet, TextInput, TouchableOpacity, Alert } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useAuthStore } from '../stores/useAuthStore';
import { useThemeStore } from '../stores/useThemeStore';

const LoginScreen: React.FC = () => {
  const { login } = useAuthStore();
  const { isDark } = useThemeStore();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = () => {
    if (!email || !password) {
      Alert.alert('오류', '이메일과 비밀번호를 입력해주세요.');
      return;
    }

    // 간단한 로그인 로직 (실제로는 API 호출)
    const user = {
      id: '1',
      name: '사용자',
      email: email,
    };
    
    login(user);
  };

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: isDark ? '#1C1C1E' : '#FFFFFF' }]}>
      <View style={styles.content}>
        <Text style={[styles.title, { color: isDark ? '#FFFFFF' : '#000000' }]}>
          로그인
        </Text>

        <TextInput
          style={[styles.input, { 
            backgroundColor: isDark ? '#2C2C2E' : '#F8F9FA',
            color: isDark ? '#FFFFFF' : '#000000',
            borderColor: isDark ? '#3A3A3C' : '#DEE2E6'
          }]}
          placeholder="이메일"
          placeholderTextColor={isDark ? '#8E8E93' : '#8E8E93'}
          value={email}
          onChangeText={setEmail}
          keyboardType="email-address"
          autoCapitalize="none"
        />

        <TextInput
          style={[styles.input, { 
            backgroundColor: isDark ? '#2C2C2E' : '#F8F9FA',
            color: isDark ? '#FFFFFF' : '#000000',
            borderColor: isDark ? '#3A3A3C' : '#DEE2E6'
          }]}
          placeholder="비밀번호"
          placeholderTextColor={isDark ? '#8E8E93' : '#8E8E93'}
          value={password}
          onChangeText={setPassword}
          secureTextEntry
        />

        <TouchableOpacity
          style={[styles.button, { backgroundColor: isDark ? '#007AFF' : '#007AFF' }]}
          onPress={handleLogin}
        >
          <Text style={styles.buttonText}>로그인</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    padding: 20,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 32,
  },
  input: {
    borderWidth: 1,
    borderRadius: 8,
    paddingHorizontal: 16,
    paddingVertical: 12,
    marginBottom: 16,
    fontSize: 16,
  },
  button: {
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 8,
    alignItems: 'center',
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
  },
});

export default LoginScreen;
