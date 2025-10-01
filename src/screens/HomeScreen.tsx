import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useAuthStore } from '../stores/useAuthStore';
import { useThemeStore } from '../stores/useThemeStore';

const HomeScreen: React.FC = () => {
  const { user, logout } = useAuthStore();
  const { theme, toggleTheme, isDark } = useThemeStore();

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: isDark ? '#1C1C1E' : '#FFFFFF' }]}>
      <View style={styles.content}>
        <Text style={[styles.title, isDark ? styles.titleDark : styles.titleLight]}>
          홈 화면
        </Text>
        
        <Text style={[styles.subtitle, isDark ? styles.subtitleDark : styles.subtitleLight]}>
          안녕하세요, {user?.name || '사용자'}님!
        </Text>

        <TouchableOpacity
          style={[styles.button, { backgroundColor: isDark ? '#007AFF' : '#007AFF' }]}
          onPress={toggleTheme}
        >
          <Text style={styles.buttonText}>
            {theme === 'light' ? '다크 모드' : '라이트 모드'}
          </Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.button, { backgroundColor: isDark ? '#FF3B30' : '#FF3B30' }]}
          onPress={logout}
        >
          <Text style={styles.buttonText}>로그아웃</Text>
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
    alignItems: 'center',
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 16,
  },
  titleLight: {
    color: '#000000',
  },
  titleDark: {
    color: '#FFFFFF',
  },
  subtitle: {
    fontSize: 16,
    marginBottom: 32,
  },
  subtitleLight: {
    color: '#6C757D',
  },
  subtitleDark: {
    color: '#8E8E93',
  },
  button: {
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 8,
    marginBottom: 16,
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
  },
});

export default HomeScreen;
