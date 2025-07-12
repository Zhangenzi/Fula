<template>
  <div class="home-wrapper">
    <!-- 顶部导航栏 -->
    <header class="header">
      <div class="header-content">
        <div class="logo">
          <el-icon class="logo-icon"><ChatDotRound /></el-icon>
          <span class="logo-text">智能面试助手</span>
        </div>
        <div class="user-info">
          <el-dropdown @command="handleCommand">
            <span class="user-avatar">
              <el-icon><User /></el-icon>
              <span>{{ userInfo.name }}</span>
              <el-icon class="el-icon--right"><arrow-down /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人中心</el-dropdown-item>
                <el-dropdown-item command="history">面试记录</el-dropdown-item>
                <el-dropdown-item command="settings">设置</el-dropdown-item>
                <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </header>

    <!-- 主要内容区域 -->
    <main class="main-content">
      <!-- 欢迎区域 -->
      <section class="welcome-section">
        <div class="welcome-content">
          <h1 class="welcome-title">
            <el-icon class="title-icon"><Star /></el-icon>
            欢迎回来，{{ userInfo.name }}！
          </h1>
          <p class="welcome-subtitle">准备好开始您的智能面试之旅了吗？</p>
          <div class="stats">
            <div class="stat-item">
              <span class="stat-number">{{ stats.totalInterviews }}</span>
              <span class="stat-label">总面试次数</span>
            </div>
            <div class="stat-item">
              <span class="stat-number">{{ stats.avgScore }}%</span>
              <span class="stat-label">平均得分</span>
            </div>
            <div class="stat-item">
              <span class="stat-number">{{ stats.completedJobs }}</span>
              <span class="stat-label">已练习岗位</span>
            </div>
          </div>
        </div>
      </section>

      <!-- 功能模块区域 -->
      <section class="features-section">
        <h2 class="section-title">
          <el-icon><BrushFilled /></el-icon>
          选择面试岗位
        </h2>
        <div class="job-grid">
          <div 
            v-for="job in jobs" 
            :key="job.id" 
            class="job-card"
            @click="startInterview(job)"
          >
            <div class="job-icon">
              <el-icon :size="40">{{ job.icon }}</el-icon>
            </div>
            <h3 class="job-title">{{ job.name }}</h3>
            <p class="job-description">{{ job.description }}</p>
            <div class="job-stats">
              <span class="difficulty">难度: {{ job.difficulty }}</span>
              <span class="duration">时长: {{ job.duration }}</span>
            </div>
            <el-button type="primary" class="start-btn">
              <el-icon><VideoPlay /></el-icon>
              开始面试
            </el-button>
          </div>
        </div>
      </section>

      <!-- 快速功能区域 -->
      <section class="quick-actions">
        <h2 class="section-title">
          <el-icon><Lightning /></el-icon>
          快速功能
        </h2>
        <div class="action-grid">
          <div class="action-card" @click="goToHistory">
            <el-icon class="action-icon"><Document /></el-icon>
            <h3>面试记录</h3>
            <p>查看历史面试记录和分析报告</p>
          </div>
          <div class="action-card" @click="goToProfile">
            <el-icon class="action-icon"><User /></el-icon>
            <h3>个人中心</h3>
            <p>管理个人信息和偏好设置</p>
          </div>
          <div class="action-card" @click="goToAnalysis">
            <el-icon class="action-icon"><TrendCharts /></el-icon>
            <h3>能力分析</h3>
            <p>查看详细的能力评估报告</p>
          </div>
          <div class="action-card" @click="goToTips">
            <el-icon class="action-icon"><InfoFilled /></el-icon>
            <h3>面试技巧</h3>
            <p>学习面试技巧和常见问题</p>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  ChatDotRound,
  User,
  ArrowDown,
  Star,
  BrushFilled,
  VideoPlay,
  Lightning,
  Document,
  TrendCharts,
  InfoFilled
} from '@element-plus/icons-vue'

const router = useRouter()

// 用户信息
const userInfo = ref({
  name: '张同学',
  avatar: '',
  level: '初级'
})

// 统计数据
const stats = ref({
  totalInterviews: 12,
  avgScore: 85,
  completedJobs: 3
})

// 岗位数据
const jobs = ref([
  {
    id: 1,
    name: '前端开发工程师',
    description: 'Vue.js、React、JavaScript等前端技术栈面试',
    icon: 'Monitor',
    difficulty: '中级',
    duration: '30分钟'
  },
  {
    id: 2,
    name: '后端开发工程师',
    description: 'Java、Python、数据库等后端技术面试',
    icon: 'Server',
    difficulty: '中级',
    duration: '45分钟'
  },
  {
    id: 3,
    name: '人工智能工程师',
    description: '机器学习、深度学习、算法等AI技术面试',
    icon: 'Cpu',
    difficulty: '高级',
    duration: '60分钟'
  },
  {
    id: 4,
    name: '大数据工程师',
    description: 'Hadoop、Spark、数据处理等大数据技术面试',
    icon: 'DataAnalysis',
    difficulty: '高级',
    duration: '50分钟'
  },
  {
    id: 5,
    name: '产品经理',
    description: '产品设计、用户体验、项目管理等综合面试',
    icon: 'Management',
    difficulty: '中级',
    duration: '40分钟'
  },
  {
    id: 6,
    name: 'UI/UX设计师',
    description: '界面设计、用户体验、设计工具等设计面试',
    icon: 'Brush',
    difficulty: '初级',
    duration: '35分钟'
  }
])

// 开始面试
const startInterview = (job) => {
  ElMessage.success(`准备开始${job.name}面试`)
  router.push(`/interview/${job.id}`)
}

// 处理用户菜单命令
const handleCommand = (command) => {
  switch (command) {
    case 'profile':
      goToProfile()
      break
    case 'history':
      goToHistory()
      break
    case 'settings':
      ElMessage.info('设置功能开发中...')
      break
    case 'logout':
      logout()
      break
  }
}

// 快速功能导航
const goToHistory = () => {
  router.push('/history')
}

const goToProfile = () => {
  router.push('/profile')
}

const goToAnalysis = () => {
  router.push('/analysis')
}

const goToTips = () => {
  router.push('/tips')
}

// 退出登录
const logout = () => {
  ElMessage.success('已退出登录')
  router.push('/login')
}

// 组件挂载时获取用户信息
onMounted(() => {
  // 这里可以调用API获取用户信息和统计数据
  console.log('Home页面已加载')
})
</script>

<style scoped>
.home-wrapper {
  min-height: 100vh;
  width: 100%; 
  height: auto;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  background-size: cover; 
  background-repeat: no-repeat; 
  position: relative;
}

.home-wrapper::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="%23ffffff" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>') repeat;
  pointer-events: none;
}

/* 头部样式 */
.header {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  height: 70px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  color: white;
  font-weight: bold;
  font-size: 20px;
}

.logo-icon {
  font-size: 28px;
  color: #ffd700;
}

.user-avatar {
  display: flex;
  align-items: center;
  gap: 8px;
  color: white;
  cursor: pointer;
  padding: 8px 16px;
  border-radius: 25px;
  background: rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.user-avatar:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

/* 主要内容区域 */
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  position: relative;
  z-index: 1;
}

/* 欢迎区域 */
.welcome-section {
  text-align: center;
  margin-bottom: 50px;
}

.welcome-content {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(15px);
  border-radius: 20px;
  padding: 40px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.welcome-title {
  color: white;
  font-size: 2.5rem;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.title-icon {
  color: #ffd700;
  font-size: 2.5rem;
}

.welcome-subtitle {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.2rem;
  margin-bottom: 30px;
}

.stats {
  display: flex;
  justify-content: center;
  gap: 40px;
  flex-wrap: wrap;
}

.stat-item {
  text-align: center;
}

.stat-number {
  display: block;
  color: #ffd700;
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 5px;
}

.stat-label {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
}

/* 功能区域 */
.features-section {
  margin-bottom: 50px;
}

.section-title {
  color: white;
  font-size: 1.8rem;
  margin-bottom: 30px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.job-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 25px;
}

.job-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(15px);
  border-radius: 16px;
  padding: 30px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.job-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  transition: left 0.5s ease;
}

.job-card:hover::before {
  left: 100%;
}

.job-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
  background: rgba(255, 255, 255, 0.15);
}

.job-icon {
  color: #ffd700;
  margin-bottom: 20px;
}

.job-title {
  color: white;
  font-size: 1.3rem;
  margin-bottom: 15px;
  font-weight: 600;
}

.job-description {
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 20px;
  line-height: 1.6;
}

.job-stats {
  display: flex;
  justify-content: space-between;
  margin-bottom: 25px;
  font-size: 0.9rem;
}

.difficulty,
.duration {
  color: rgba(255, 255, 255, 0.7);
  background: rgba(255, 255, 255, 0.1);
  padding: 4px 12px;
  border-radius: 12px;
}

.start-btn {
  width: 100%;
  height: 45px;
  font-size: 1rem;
  border-radius: 12px;
  background: linear-gradient(45deg, #667eea, #764ba2);
  border: none;
  transition: all 0.3s ease;
}

.start-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

/* 快速功能区域 */
.quick-actions {
  margin-bottom: 30px;
}

.action-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.action-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(15px);
  border-radius: 16px;
  padding: 25px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
}

.action-card:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.15);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
}

.action-icon {
  color: #ffd700;
  font-size: 2.5rem;
  margin-bottom: 15px;
}

.action-card h3 {
  color: white;
  font-size: 1.2rem;
  margin-bottom: 10px;
}

.action-card p {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
  line-height: 1.5;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-content {
    padding: 0 15px;
  }
  
  .main-content {
    padding: 20px 15px;
  }
  
  .welcome-title {
    font-size: 2rem;
  }
  
  .stats {
    gap: 20px;
  }
  
  .job-grid {
    grid-template-columns: 1fr;
  }
  
  .action-grid {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  }
}

@media (max-width: 480px) {
  .welcome-content {
    padding: 25px;
  }
  
  .welcome-title {
    font-size: 1.8rem;
    flex-direction: column;
    gap: 10px;
  }
  
  .stats {
    flex-direction: column;
    gap: 15px;
  }
}
</style>