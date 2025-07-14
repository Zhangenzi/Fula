import { defineStore } from 'pinia';
import { api } from '@/utils/api';

interface User {
id: number;
username: string;
email: string;
created_at: string;
}

interface UserStats {
    total_interviews: number;
    completed_interviews: number;
    average_score: number;
    total_time_minutes: number;
    best_score: number;
    skill_assessments: any[];
}

export const useUserStore = defineStore('user', {
state: () => ({
    user: null as User | null,
    stats: null as UserStats | null,
    isLoggedIn: false,
    token: localStorage.getItem('token') || null,
}),

actions: {
    async login(username: string, password: string) {
    try {
        const response = await api.login(username, password);
        if (response.code === 200 && response.data) {
        // 添加类型断言或更严格的类型检查
        const { token, user } = response.data as { token: string; user: User };
        this.token = token;
        this.user = user;
        this.isLoggedIn = true;
        localStorage.setItem('token', this.token);
        return { success: true };
        } else {
        return { success: false, message: response.msg };
        }
    } catch (error) {
        return { success: false, message: '登录失败，请检查网络连接' };
    }
    },

    async register(username: string, password: string, email: string) {
    try {
        // 修改：传递对象而不是独立参数
        const response = await api.register({
            username,
            password,
            email
        });
        if (response.code === 200) {
            return { success: true };
        } else {
            return { success: false, message: response.msg };
        }
    } catch (error) {
        return { success: false, message: '注册失败，请检查网络连接' };
    }
    },

    async logout() {
    try {
        await api.logout();
    } catch (error) {
        console.error('登出请求失败:', error);
    } finally {
        this.user = null;
        this.stats = null;
        this.isLoggedIn = false;
        this.token = null;
        localStorage.removeItem('token');
    }
    },

    async fetchUserProfile() {
    try {
        const response = await api.getUserProfile();
        if (response.code === 200 && response.data) {
        this.user = response.data as User;
        this.isLoggedIn = true;
        }
    } catch (error) {
        console.error('获取用户信息失败:', error);
        this.logout();
    }
    },

    async fetchUserStats() {
    try {
        const response = await api.getUserStats();
        if (response.code === 200 && response.data) {
        this.stats = response.data as UserStats;
        }
    } catch (error) {
        console.error('获取用户统计失败:', error);
    }
    },

    // 初始化用户状态
    async initializeAuth() {
    if (this.token) {
        await this.fetchUserProfile();
        await this.fetchUserStats();
    }
    },
},
});