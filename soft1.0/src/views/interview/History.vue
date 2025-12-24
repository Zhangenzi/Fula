<template>
  <div class="history-wrapper">
    <!-- 顶部导航栏 -->
    <header class="header">
      <div class="header-content">
        <div class="nav-left">
          <el-button @click="goBack" type="text" class="back-btn">
            <el-icon><ArrowLeft /></el-icon>
            返回首页
          </el-button>
        </div>
        <h1 class="page-title">
          <el-icon><Document /></el-icon>
          面试记录
        </h1>
        <div class="nav-right"></div>
      </div>
    </header>

    <!-- 主要内容区域 -->
    <main class="main-content">
      <!-- 统计概览 -->
      <section class="stats-overview">
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon">
              <el-icon><TrendCharts /></el-icon>
            </div>
            <div class="stat-info">
              <span class="stat-number">{{ overallStats.totalInterviews }}</span>
              <span class="stat-label">总面试次数</span>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon success">
              <el-icon><CircleCheck /></el-icon>
            </div>
            <div class="stat-info">
              <span class="stat-number">{{ overallStats.avgScore }}%</span>
              <span class="stat-label">平均得分</span>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon warning">
              <el-icon><Clock /></el-icon>
            </div>
            <div class="stat-info">
              <span class="stat-number">{{ overallStats.totalTime }}</span>
              <span class="stat-label">总用时(小时)</span>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon info">
              <el-icon><Star /></el-icon>
            </div>
            <div class="stat-info">
              <span class="stat-number">{{ overallStats.bestScore }}%</span>
              <span class="stat-label">最高得分</span>
            </div>
          </div>
        </div>
      </section>

      <!-- 筛选和搜索 -->
      <section class="filter-section">
        <div class="filter-content">
          <div class="filter-left">
            <el-select v-model="filterJob" placeholder="选择岗位" clearable>
              <el-option label="全部岗位" value=""></el-option>
              <el-option 
                v-for="job in jobTypes" 
                :key="job.value" 
                :label="job.label" 
                :value="job.value"
              ></el-option>
            </el-select>
            <el-select v-model="filterScore" placeholder="选择分数范围" clearable>
              <el-option label="全部分数" value=""></el-option>
              <el-option label="90-100分" value="90-100"></el-option>
              <el-option label="80-89分" value="80-89"></el-option>
              <el-option label="70-79分" value="70-79"></el-option>
              <el-option label="60-69分" value="60-69"></el-option>
              <el-option label="60分以下" value="0-59"></el-option>
            </el-select>
            <el-date-picker
              v-model="dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
            />
          </div>
          <div class="filter-right">
            <el-input
              v-model="searchKeyword"
              placeholder="搜索面试记录..."
              clearable
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </div>
        </div>
      </section>

      <!-- 面试记录列表 -->
      <section class="records-section">
        <div class="records-header">
          <h2>面试记录列表</h2>
          <el-button type="primary" @click="exportRecords">
            <el-icon><Download /></el-icon>
            导出记录
          </el-button>
        </div>
        
        <div class="records-list">
          <div 
            v-for="record in filteredRecords" 
            :key="record.id" 
            class="record-card"
            @click="viewDetail(record)"
          >
            <div class="record-header">
              <div class="record-title">
                <h3>{{ record.jobName }}</h3>
                <el-tag :type="getScoreType(record.score)" size="large">
                  {{ record.score }}分
                </el-tag>
              </div>
              <div class="record-date">
                {{ formatDate(record.date) }}
              </div>
            </div>
            
            <div class="record-content">
              <div class="record-info">
                <div class="info-item">
                  <el-icon><Clock /></el-icon>
                  <span>用时: {{ record.duration }}</span>
                </div>
                <div class="info-item">
                  <el-icon><ChatDotRound /></el-icon>
                  <span>问题数: {{ record.questionCount }}</span>
                </div>
                <div class="info-item">
                  <el-icon><TrendCharts /></el-icon>
                  <span>难度: {{ record.difficulty }}</span>
                </div>
              </div>
              
              <div class="record-summary">
                <p>{{ record.summary }}</p>
              </div>
              
              <div class="record-skills">
                <span class="skills-label">技能评估:</span>
                <div class="skills-tags">
                  <el-tag 
                    v-for="skill in record.skills" 
                    :key="skill.name"
                    :type="getSkillType(skill.score)"
                    size="small"
                  >
                    {{ skill.name }}: {{ skill.score }}%
                  </el-tag>
                </div>
              </div>
            </div>
            
            <div class="record-actions">
              <el-button size="small" @click.stop="viewDetail(record)">
                <el-icon><View /></el-icon>
                查看详情
              </el-button>
              <el-button size="small" type="primary" @click.stop="retakeInterview(record)">
                <el-icon><Refresh /></el-icon>
                重新面试
              </el-button>
              <el-button size="small" type="danger" @click.stop="deleteRecord(record)">
                <el-icon><Delete /></el-icon>
                删除
              </el-button>
            </div>
          </div>
        </div>
        
        <!-- 空状态 -->
        <div v-if="filteredRecords.length === 0" class="empty-state">
          <el-icon class="empty-icon"><DocumentRemove /></el-icon>
          <h3>暂无面试记录</h3>
          <p>开始您的第一次面试吧！</p>
          <el-button type="primary" @click="goToHome">
            <el-icon><Plus /></el-icon>
            开始面试
          </el-button>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  ArrowLeft,
  Document,
  TrendCharts,
  CircleCheck,
  Clock,
  Star,
  Search,
  Download,
  ChatDotRound,
  View,
  Refresh,
  Delete,
  DocumentRemove,
  Plus
} from '@element-plus/icons-vue'

const router = useRouter()

// 筛选条件
const filterJob = ref('')
const filterScore = ref('')
const dateRange = ref([])
const searchKeyword = ref('')

// 统计数据
const overallStats = ref({
  totalInterviews: 15,
  avgScore: 82,
  totalTime: 12.5,
  bestScore: 95
})

// 岗位类型
const jobTypes = ref([
  { label: '前端开发工程师', value: 'frontend' },
  { label: '后端开发工程师', value: 'backend' },
  { label: '人工智能工程师', value: 'ai' },
  { label: '大数据工程师', value: 'bigdata' },
  { label: '产品经理', value: 'pm' },
  { label: 'UI/UX设计师', value: 'design' }
])

// 面试记录数据
const records = ref([
  {
    id: 1,
    jobName: '前端开发工程师',
    jobType: 'frontend',
    score: 88,
    date: '2024-01-15',
    duration: '45分钟',
    questionCount: 12,
    difficulty: '中级',
    summary: '在Vue.js和JavaScript基础方面表现良好，但在算法优化方面还需要加强练习。',
    skills: [
      { name: 'JavaScript', score: 85 },
      { name: 'Vue.js', score: 90 },
      { name: '算法', score: 75 },
      { name: '项目经验', score: 88 }
    ]
  },
  {
    id: 2,
    jobName: '人工智能工程师',
    jobType: 'ai',
    score: 92,
    date: '2024-01-10',
    duration: '60分钟',
    questionCount: 15,
    difficulty: '高级',
    summary: '机器学习理论扎实，深度学习实践经验丰富，数学基础优秀。',
    skills: [
      { name: '机器学习', score: 95 },
      { name: '深度学习', score: 90 },
      { name: '数学基础', score: 88 },
      { name: 'Python', score: 92 }
    ]
  },
  {
    id: 3,
    jobName: '后端开发工程师',
    jobType: 'backend',
    score: 76,
    date: '2024-01-05',
    duration: '50分钟',
    questionCount: 10,
    difficulty: '中级',
    summary: 'Java基础扎实，但在分布式系统设计方面经验不足，需要更多实践。',
    skills: [
      { name: 'Java', score: 82 },
      { name: '数据库', score: 78 },
      { name: '分布式系统', score: 65 },
      { name: '系统设计', score: 70 }
    ]
  }
])

// 过滤后的记录
const filteredRecords = computed(() => {
  let filtered = records.value
  
  // 按岗位筛选
  if (filterJob.value) {
    filtered = filtered.filter(record => record.jobType === filterJob.value)
  }
  
  // 按分数筛选
  if (filterScore.value) {
    const [min, max] = filterScore.value.split('-').map(Number)
    filtered = filtered.filter(record => record.score >= min && record.score <= max)
  }
  
  // 按日期筛选
  if (dateRange.value && dateRange.value.length === 2) {
    const [startDate, endDate] = dateRange.value
    filtered = filtered.filter(record => {
      return record.date >= startDate && record.date <= endDate
    })
  }
  
  // 按关键词搜索
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    filtered = filtered.filter(record => 
      record.jobName.toLowerCase().includes(keyword) ||
      record.summary.toLowerCase().includes(keyword)
    )
  }
  
  return filtered.sort((a, b) => new Date(b.date) - new Date(a.date))
})

// 获取分数类型
const getScoreType = (score) => {
  if (score >= 90) return 'success'
  if (score >= 80) return 'primary'
  if (score >= 70) return 'warning'
  return 'danger'
}

// 获取技能类型
const getSkillType = (score) => {
  if (score >= 85) return 'success'
  if (score >= 75) return 'primary'
  if (score >= 65) return 'warning'
  return 'danger'
}

// 格式化日期
const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// 返回首页
const goBack = () => {
  router.push('/home')
}

// 去首页
const goToHome = () => {
  router.push('/home')
}

// 查看详情
const viewDetail = (record) => {
  ElMessage.info(`查看面试记录详情: ${record.jobName}`)
  // 这里可以跳转到详情页面或打开模态框
}

// 重新面试
const retakeInterview = (record) => {
  ElMessage.success(`准备重新开始${record.jobName}面试`)
  // 根据记录的岗位类型跳转到对应面试
  router.push(`/interview/${record.jobType}`)
}

// 删除记录
const deleteRecord = async (record) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除这条面试记录吗？此操作不可恢复。`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    // 从数组中移除记录
    const index = records.value.findIndex(r => r.id === record.id)
    if (index > -1) {
      records.value.splice(index, 1)
      ElMessage.success('删除成功')
    }
  } catch {
    ElMessage.info('已取消删除')
  }
}

// 导出记录
const exportRecords = () => {
  ElMessage.success('导出功能开发中...')
  // 这里可以实现导出Excel或PDF功能
}

// 组件挂载
onMounted(() => {
  console.log('面试记录页面已加载')
})
</script>

<style scoped>
.history-wrapper {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
}

.history-wrapper::before {
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

.back-btn {
  color: white;
  font-size: 16px;
  padding: 8px 16px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateX(-3px);
}

.page-title {
  color: white;
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0;
}

/* 主要内容 */
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px 20px;
  position: relative;
  z-index: 1;
}

/* 统计概览 */
.stats-overview {
  margin-bottom: 30px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.stat-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(15px);
  border-radius: 16px;
  padding: 25px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  gap: 20px;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-3px);
  background: rgba(255, 255, 255, 0.15);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.2);
  color: #ffd700;
  font-size: 24px;
}

.stat-icon.success {
  background: rgba(103, 194, 58, 0.2);
  color: #67c23a;
}

.stat-icon.warning {
  background: rgba(230, 162, 60, 0.2);
  color: #e6a23c;
}

.stat-icon.info {
  background: rgba(64, 158, 255, 0.2);
  color: #409eff;
}

.stat-number {
  display: block;
  color: white;
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 5px;
}

.stat-label {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
}

/* 筛选区域 */
.filter-section {
  margin-bottom: 30px;
}

.filter-content {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(15px);
  border-radius: 16px;
  padding: 25px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
}

.filter-left {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.filter-right {
  min-width: 250px;
}

/* 记录区域 */
.records-section {
  margin-bottom: 30px;
}

.records-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.records-header h2 {
  color: white;
  font-size: 1.5rem;
  margin: 0;
}

.records-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.record-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(15px);
  border-radius: 16px;
  padding: 25px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  cursor: pointer;
  transition: all 0.3s ease;
}

.record-card:hover {
  transform: translateY(-3px);
  background: rgba(255, 255, 255, 0.15);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
}

.record-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.record-title {
  display: flex;
  align-items: center;
  gap: 15px;
}

.record-title h3 {
  color: white;
  font-size: 1.3rem;
  margin: 0;
}

.record-date {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
}

.record-content {
  margin-bottom: 20px;
}

.record-info {
  display: flex;
  gap: 25px;
  margin-bottom: 15px;
  flex-wrap: wrap;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
}

.record-summary {
  margin-bottom: 15px;
}

.record-summary p {
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.6;
  margin: 0;
}

.record-skills {
  display: flex;
  align-items: center;
  gap: 15px;
  flex-wrap: wrap;
}

.skills-label {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
  font-weight: 500;
}

.skills-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.record-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(15px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.empty-icon {
  font-size: 4rem;
  color: rgba(255, 255, 255, 0.5);
  margin-bottom: 20px;
}

.empty-state h3 {
  color: white;
  font-size: 1.5rem;
  margin-bottom: 10px;
}

.empty-state p {
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 25px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-content {
    padding: 0 15px;
  }
  
  .main-content {
    padding: 20px 15px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .filter-content {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filter-left {
    justify-content: center;
  }
  
  .records-header {
    flex-direction: column;
    gap: 15px;
    align-items: stretch;
  }
  
  .record-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .record-info {
    flex-direction: column;
    gap: 10px;
  }
  
  .record-actions {
    justify-content: center;
    flex-wrap: wrap;
  }
}
</style>