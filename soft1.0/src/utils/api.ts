// API请求工具
const API_BASE_URL = 'http://localhost:5000/api';

interface ApiResponse<T = any> {
  code: number;
  msg: string;
  data?: T;
}

// 更新数据类型定义，匹配数据库结构
interface User {
  id: number;
  username: string;
  password?: string;
  real_name?: string;
  email?: string;
  phone?: string;
  major?: string;
  grade?: string;
  avatar_url?: string;
  created_at: string;
  updated_at: string;
}

interface JobPosition {
  id: number;
  name: string;
  description: string;
  difficulty: '初级' | '中级' | '高级';
  duration: number;
  icon: string;
  is_active: boolean;
  created_at: string;
}

interface InterviewRecord {
  id: number;
  user_id: number;
  job_position_id: number;
  score: number;
  duration_minutes?: number;
  status: '进行中' | '已完成' | '已中断';
  start_time: string;
  end_time?: string;
  summary?: string;
  created_at: string;
  job_position?: JobPosition;
}

interface Question {
  id: number;
  job_position_id: number;
  type: 'behavioral' | 'technical' | 'coding' | 'scenario';
  title: string;
  description?: string;
  difficulty: number;
  hint?: string;
  code_template?: string;
  tags?: string[];
  is_active: boolean;
  created_at: string;
}

interface InterviewQuestionRecord {
  id: number;
  interview_record_id: number;
  question_id: number;
  question_order: number;
  answer_text?: string;
  answer_code?: string;
  programming_language?: string;
  audio_file_path?: string;
  score: number;
  time_spent?: number;
  is_skipped: boolean;
  created_at: string;
  question?: Question;
}

interface SkillAssessment {
  id: number;
  interview_record_id: number;
  skill_name: string;
  score: number;
  created_at: string;
}

class ApiClient {
  private async request<T>(url: string, options: RequestInit = {}): Promise<ApiResponse<T>> {
    const token = localStorage.getItem('token');
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(`${API_BASE_URL}${url}`, config);
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('API请求失败:', error);
      throw error;
    }
  }

  // 用户认证
  async register(userData: {
    username: string;
    password: string;
    email: string;
    real_name?: string;
    phone?: string;
    major?: string;
    grade?: string;
  }): Promise<ApiResponse> {
    return this.request('/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async login(username: string, password: string): Promise<ApiResponse<{
    token: string;
    user: User;
  }>> {
    return this.request('/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
  }

  // 用户信息管理
  async getUserProfile(): Promise<ApiResponse<User>> {
    return this.request<User>('/user/profile');
  }

  async updateUserProfile(userData: Partial<User>): Promise<ApiResponse<User>> {
    return this.request<User>('/user/profile', {
      method: 'PUT',
      body: JSON.stringify(userData),
    });
  }

  async getUserStats(): Promise<ApiResponse<{
    total_interviews: number;
    completed_interviews: number;
    average_score: number;
    total_time_minutes: number;
    best_score: number;
    skill_assessments: SkillAssessment[];
  }>> {
    return this.request('/user/stats');
  }

  // 岗位管理
  async getJobPositions(): Promise<ApiResponse<JobPosition[]>> {
    return this.request<JobPosition[]>('/job-positions');
  }

  async getJobPosition(id: number): Promise<ApiResponse<JobPosition>> {
    return this.request<JobPosition>(`/job-positions/${id}`);
  }

  // 问题管理
  async getQuestionsByPosition(positionId: number): Promise<ApiResponse<Question[]>> {
    return this.request<Question[]>(`/job-positions/${positionId}/questions`);
  }

  // 面试管理
  async startInterview(positionId: number): Promise<ApiResponse<{
    interview_record: InterviewRecord;
    questions: Question[];
  }>> {
    return this.request('/interviews/start', {
      method: 'POST',
      body: JSON.stringify({ job_position_id: positionId }),
    });
  }

  async getInterviewRecord(interviewId: number): Promise<ApiResponse<{
    interview_record: InterviewRecord;
    questions: Question[];
    answers: InterviewQuestionRecord[];
  }>> {
    return this.request(`/interviews/${interviewId}`);
  }

  async saveAnswer(data: {
    interview_record_id: number;
    question_id: number;
    question_order: number;
    answer_text?: string;
    answer_code?: string;
    programming_language?: string;
    time_spent?: number;
  }): Promise<ApiResponse<InterviewQuestionRecord>> {
    return this.request('/interviews/answer', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async finishInterview(interviewId: number, summary?: string): Promise<ApiResponse<{
    interview_record: InterviewRecord;
    skill_assessments: SkillAssessment[];
  }>> {
    return this.request(`/interviews/${interviewId}/finish`, {
      method: 'POST',
      body: JSON.stringify({ summary }),
    });
  }

  // 面试记录查询
  async getInterviewHistory(params?: {
    job_position_id?: number;
    status?: string;
    start_date?: string;
    end_date?: string;
    page?: number;
    limit?: number;
  }): Promise<ApiResponse<{
    records: InterviewRecord[];
    total: number;
    page: number;
    limit: number;
  }>> {
    const queryParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          queryParams.append(key, value.toString());
        }
      });
    }
    const queryString = queryParams.toString();
    return this.request(`/interviews/history${queryString ? '?' + queryString : ''}`);
  }

  async deleteInterviewRecord(interviewId: number): Promise<ApiResponse> {
    return this.request(`/interviews/${interviewId}`, {
      method: 'DELETE',
    });
  }

  // 技能评估
  async getSkillAssessments(interviewId?: number): Promise<ApiResponse<SkillAssessment[]>> {
    const url = interviewId ? `/skill-assessments?interview_id=${interviewId}` : '/skill-assessments';
    return this.request<SkillAssessment[]>(url);
  }
}

export const api = new ApiClient();
export type { 
  ApiResponse, 
  User, 
  JobPosition, 
  InterviewRecord, 
  Question, 
  InterviewQuestionRecord, 
  SkillAssessment 
};