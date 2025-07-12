<template>
<div class="analysis-wrapper">
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
        <el-icon><TrendCharts /></el-icon>
        能力分析
        </h1>
        <div class="nav-right">
        <el-button type="primary" @click="generateReport">
            <el-icon><Document /></el-icon>
            生成报告
        </el-button>
        </div>
    </div>
    </header>

    <!-- 主要内容区域 -->
    <main class="main-content">
    <!-- 总体评分卡片 -->
    <section class="overall-score">
        <div class="score-card">
        <div class="score-circle">
            <div class="score-number">{{ overallScore }}</div>
            <div class="score-label">综合评分</div>
        </div>
        <div class="score-details">
            <div class="detail-item">
            <span class="detail-label">技术能力</span>
            <div class="progress-bar">
                <div class="progress-fill" :style="{ width: technicalScore + '%' }"></div>
            </div>
            <span class="detail-score">{{ technicalScore }}%</span>
            </div>
            <div class="detail-item">
            <span class="detail-label">沟通表达</span>
            <div class="progress-bar">
                <div class="progress-fill" :style="{ width: communicationScore + '%' }"></div>
            </div>
            <span class="detail-score">{{ communicationScore }}%</span>
            </div>
            <div class="detail-item">
            <span class="detail-label">逻辑思维</span>
            <div class="progress-bar">
                <div class="progress-fill" :style="{ width: logicScore + '%' }"></div>
            </div>
            <span class="detail-score">{{ logicScore }}%</span>
            </div>
            <div class="detail-item">
            <span class="detail-label">学习能力</span>
            <div class="progress-bar">
                <div class="progress-fill" :style="{ width: learningScore + '%' }"></div>
            </div>
            <span class="detail-score">{{ learningScore }}%</span>
            </div>
        </div>
        </div>
    </section>

    <!-- 内容网格 -->
    <div class="content-grid">
        <!-- 技能雷达图 -->
        <!-- 第70-90行区域 -->
        <section class="radar-section">
            <div class="section-header">
                <h3>
                <!-- 第73行：将 Radar 替换为 PieChart -->
                <el-icon><PieChart /></el-icon>
                
                <!-- 第87行：将 Radar 替换为 PieChart -->
                <el-icon class="radar-icon"><PieChart /></el-icon>
                
                <!-- 第158行：将 Lightbulb 替换为 Sunny -->
                <el-icon><Sunny /></el-icon>
                技能雷达图
                </h3>
                <el-select v-model="selectedCategory" placeholder="选择分类">
                <el-option label="全部技能" value="all"></el-option>
                <el-option label="前端技能" value="frontend"></el-option>
                <el-option label="后端技能" value="backend"></el-option>
                <el-option label="算法能力" value="algorithm"></el-option>
                </el-select>
            </div>
            <div class="radar-container">
                <div class="radar-chart">
                <!-- 这里可以集成 ECharts 或其他图表库 -->
                <div class="radar-placeholder">
                    <el-icon class="radar-icon"><PieChart /></el-icon>
                    <p>技能雷达图</p>
                    <small>展示各项技能的掌握程度</small>
                </div>
                </div>
            </div>
            </section>

        <!-- 成长趋势 -->
        <section class="trend-section">
        <div class="section-header">
            <h3>
            <el-icon><TrendCharts /></el-icon>
            成长趋势
            </h3>
            <el-radio-group v-model="trendPeriod" size="small">
            <el-radio-button label="week">最近一周</el-radio-button>
            <el-radio-button label="month">最近一月</el-radio-button>
            <el-radio-button label="quarter">最近三月</el-radio-button>
            </el-radio-group>
        </div>
        <div class="trend-chart">
            <div class="chart-placeholder">
            <el-icon class="chart-icon"><TrendCharts /></el-icon>
            <p>成长趋势图</p>
            <small>显示能力提升轨迹</small>
            </div>
        </div>
        </section>

        <!-- 技能详情 -->
        <section class="skills-detail">
        <div class="section-header">
            <h3>
            <el-icon><Medal /></el-icon>
            技能详情
            </h3>
        </div>
        <div class="skills-list">
            <div 
            v-for="skill in skillsData" 
            :key="skill.name"
            class="skill-item"
            >
            <div class="skill-header">
                <span class="skill-name">{{ skill.name }}</span>
                <el-tag :type="getSkillLevel(skill.score)" size="small">
                {{ getSkillLevelText(skill.score) }}
                </el-tag>
            </div>
            <div class="skill-progress">
                <el-progress 
                :percentage="skill.score" 
                :color="getProgressColor(skill.score)"
                :stroke-width="8"
                />
            </div>
            <div class="skill-details">
                <span class="skill-score">{{ skill.score }}%</span>
                <span class="skill-change" :class="skill.change >= 0 ? 'positive' : 'negative'">
                {{ skill.change >= 0 ? '+' : '' }}{{ skill.change }}%
                </span>
            </div>
            </div>
        </div>
        </section>

        <!-- 改进建议 -->
        <section class="suggestions-section">
        <!-- 第155-165行区域 -->
        <div class="section-header">
            <h3>
            <el-icon><Sunny /></el-icon>
            改进建议
            </h3>
        </div>
        <div class="suggestions-list">
            <div 
            v-for="suggestion in suggestions" 
            :key="suggestion.id"
            class="suggestion-item"
            >
            <div class="suggestion-header">
                <el-icon :class="suggestion.priority">{{ suggestion.icon }}</el-icon>
                <h4>{{ suggestion.title }}</h4>
                <el-tag :type="getPriorityType(suggestion.priority)" size="small">
                {{ suggestion.priority }}
                </el-tag>
            </div>
            <p class="suggestion-content">{{ suggestion.content }}</p>
            <div class="suggestion-actions">
                <el-button size="small" type="primary">
                <el-icon><Link /></el-icon>
                查看资源
                </el-button>
                <el-button size="small">
                <el-icon><Check /></el-icon>
                标记完成
                </el-button>
            </div>
            </div>
        </div>
        </section>

        <!-- 面试表现分析 -->
        <section class="performance-section">
        <div class="section-header">
            <h3>
            <el-icon><DataAnalysis /></el-icon>
            面试表现分析
            </h3>
        </div>
        <div class="performance-grid">
            <div class="performance-card">
            <div class="performance-icon success">
                <el-icon><CircleCheck /></el-icon>
            </div>
            <div class="performance-info">
                <h4>优势领域</h4>
                <ul>
                <li v-for="strength in strengths" :key="strength">{{ strength }}</li>
                </ul>
            </div>
            </div>
            <div class="performance-card">
            <div class="performance-icon warning">
                <el-icon><Warning /></el-icon>
            </div>
            <div class="performance-info">
                <h4>待提升领域</h4>
                <ul>
                <li v-for="weakness in weaknesses" :key="weakness">{{ weakness }}</li>
                </ul>
            </div>
            </div>
        </div>
        </section>

        <!-- 学习路径推荐 -->
        <section class="learning-path">
        <div class="section-header">
            <h3>
            <el-icon><Guide /></el-icon>
            学习路径推荐
            </h3>
        </div>
        <div class="path-timeline">
            <div 
            v-for="(step, index) in learningPath" 
            :key="step.id"
            class="timeline-item"
            :class="{ completed: step.completed, current: step.current }"
            >
            <div class="timeline-marker">
                <span class="step-number">{{ index + 1 }}</span>
            </div>
            <div class="timeline-content">
                <h4>{{ step.title }}</h4>
                <p>{{ step.description }}</p>
                <div class="step-meta">
                <span class="duration">预计时长: {{ step.duration }}</span>
                <span class="difficulty">难度: {{ step.difficulty }}</span>
                </div>
                <el-button v-if="step.current" type="primary" size="small">
                开始学习
                </el-button>
            </div>
            </div>
        </div>
        </section>
    </div>
    </main>
</div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
ArrowLeft,
TrendCharts,
Document,
Medal,
Link,
Check,
DataAnalysis,
CircleCheck,
Warning,
Guide,
// 添加替代图标
PieChart,       // 替代 Radar
Sunny          // 替代 Lightbulb
} from '@element-plus/icons-vue'

const router = useRouter()

// 筛选条件
const selectedCategory = ref('all')
const trendPeriod = ref('month')

// 总体评分数据
const overallScore = ref(82)
const technicalScore = ref(85)
const communicationScore = ref(78)
const logicScore = ref(88)
const learningScore = ref(80)

// 技能数据
const skillsData = ref([
{ name: 'JavaScript', score: 88, change: 5 },
{ name: 'Vue.js', score: 85, change: 3 },
{ name: 'Python', score: 75, change: -2 },
{ name: '算法与数据结构', score: 70, change: 8 },
{ name: '系统设计', score: 65, change: 12 },
{ name: '数据库', score: 80, change: 0 },
{ name: '网络协议', score: 72, change: 6 },
{ name: '项目管理', score: 68, change: 4 }
])

// 改进建议
const suggestions = ref([
{
    id: 1,
    title: '加强算法练习',
    content: '建议每天练习1-2道算法题，重点关注动态规划和图算法。可以使用LeetCode等平台进行系统性练习。',
    priority: '高优先级',
    icon: 'Warning'
},
{
    id: 2,
    title: '提升系统设计能力',
    content: '学习分布式系统设计原理，了解微服务架构，可以通过阅读《设计数据密集型应用》等书籍来提升。',
    priority: '高优先级',
    icon: 'Warning'
},
{
    id: 3,
    title: '完善项目经验',
    content: '参与开源项目或独立完成一个完整的项目，积累实际开发经验，提升工程能力。',
    priority: '中优先级',
    icon: 'InfoFilled'
},
{
    id: 4,
    title: '加强沟通表达',
    content: '多参与技术分享和讨论，练习技术方案的表达和展示能力，可以尝试写技术博客。',
    priority: '中优先级',
    icon: 'InfoFilled'
}
])

// 优势和劣势
const strengths = ref([
'JavaScript基础扎实',
'Vue.js框架熟练',
'逻辑思维清晰',
'学习能力强'
])

const weaknesses = ref([
'算法能力需要提升',
'系统设计经验不足',
'大型项目经验缺乏',
'沟通表达有待加强'
])

// 学习路径
const learningPath = ref([
{
    id: 1,
    title: '算法基础强化',
    description: '系统学习数据结构与算法，掌握常见算法模式',
    duration: '4周',
    difficulty: '中等',
    completed: true,
    current: false
},
{
    id: 2,
    title: '系统设计入门',
    description: '学习分布式系统基础概念，了解常见架构模式',
    duration: '6周',
    difficulty: '中等',
    completed: false,
    current: true
},
{
    id: 3,
    title: '项目实战练习',
    description: '完成一个完整的全栈项目，应用所学知识',
    duration: '8周',
    difficulty: '较难',
    completed: false,
    current: false
},
{
    id: 4,
    title: '高级系统设计',
    description: '深入学习大规模系统设计，掌握性能优化技巧',
    duration: '10周',
    difficulty: '困难',
    completed: false,
    current: false
}
])

// 获取技能等级
const getSkillLevel = (score) => {
if (score >= 85) return 'success'
if (score >= 70) return 'warning'
return 'danger'
}

// 获取技能等级文本
const getSkillLevelText = (score) => {
if (score >= 85) return '熟练'
if (score >= 70) return '一般'
return '待提升'
}

// 获取进度条颜色
const getProgressColor = (score) => {
if (score >= 85) return '#67c23a'
if (score >= 70) return '#e6a23c'
return '#f56c6c'
}

// 获取优先级类型
const getPriorityType = (priority) => {
const types = {
    '高优先级': 'danger',
    '中优先级': 'warning',
    '低优先级': 'info'
}
return types[priority] || 'info'
}

// 返回首页
const goBack = () => {
router.push('/home')
}

// 生成报告
const generateReport = () => {
ElMessage.success('正在生成能力分析报告...')
// 这里可以实现PDF报告生成功能
}

// 组件挂载
onMounted(() => {
console.log('能力分析页面已加载')
})
</script>

<style scoped>

.analysis-wrapper {
position: fixed;
top: 0;
left: 0;
width: 100vw;
height: 100vh;
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
overflow-y: auto;
min-height: 100vh;
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
position: relative;
}

.analysis-wrapper::before {
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
max-width: 1400px;
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
max-width: 1400px;
margin: 0 auto;
padding: 30px 20px;
position: relative;
z-index: 1;
}

/* 总体评分 */
.overall-score {
margin-bottom: 30px;
}

.score-card {
background: rgba(255, 255, 255, 0.1);
backdrop-filter: blur(15px);
border-radius: 20px;
padding: 40px;
border: 1px solid rgba(255, 255, 255, 0.2);
display: flex;
align-items: center;
gap: 50px;
}

.score-circle {
width: 150px;
height: 150px;
border-radius: 50%;
background: conic-gradient(from 0deg, #667eea 0%, #764ba2 100%);
display: flex;
flex-direction: column;
align-items: center;
justify-content: center;
position: relative;
}

.score-circle::before {
content: '';
position: absolute;
width: 120px;
height: 120px;
border-radius: 50%;
background: rgba(255, 255, 255, 0.1);
backdrop-filter: blur(10px);
}

.score-number {
font-size: 2.5rem;
font-weight: bold;
color: white;
z-index: 1;
}

.score-label {
color: rgba(255, 255, 255, 0.9);
font-size: 0.9rem;
z-index: 1;
}

.score-details {
flex: 1;
display: flex;
flex-direction: column;
gap: 20px;
}

.detail-item {
display: flex;
align-items: center;
gap: 20px;
}

.detail-label {
color: rgba(255, 255, 255, 0.9);
min-width: 80px;
font-weight: 500;
}

.progress-bar {
flex: 1;
height: 8px;
background: rgba(255, 255, 255, 0.2);
border-radius: 4px;
overflow: hidden;
}

.progress-fill {
height: 100%;
background: linear-gradient(90deg, #67c23a, #85ce61);
border-radius: 4px;
transition: width 0.3s ease;
}

.detail-score {
color: white;
font-weight: bold;
min-width: 50px;
text-align: right;
}

/* 内容网格 */
.content-grid {
display: grid;
grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
gap: 25px;
}

/* 通用区域样式 */
.radar-section,
.trend-section,
.skills-detail,
.suggestions-section,
.performance-section,
.learning-path {
background: rgba(255, 255, 255, 0.1);
backdrop-filter: blur(15px);
border-radius: 16px;
padding: 25px;
border: 1px solid rgba(255, 255, 255, 0.2);
}

.section-header {
display: flex;
justify-content: space-between;
align-items: center;
margin-bottom: 25px;
}

.section-header h3 {
color: white;
font-size: 1.2rem;
display: flex;
align-items: center;
gap: 10px;
margin: 0;
}

/* 雷达图 */
.radar-container {
height: 300px;
display: flex;
align-items: center;
justify-content: center;
}

.radar-placeholder,
.chart-placeholder {
text-align: center;
color: rgba(255, 255, 255, 0.7);
}

.radar-icon,
.chart-icon {
font-size: 4rem;
margin-bottom: 15px;
color: rgba(255, 255, 255, 0.5);
}

/* 趋势图 */
.trend-chart {
height: 250px;
display: flex;
align-items: center;
justify-content: center;
}

/* 技能详情 */
.skills-list {
display: flex;
flex-direction: column;
gap: 20px;
}

.skill-item {
background: rgba(255, 255, 255, 0.1);
border-radius: 12px;
padding: 20px;
}

.skill-header {
display: flex;
justify-content: space-between;
align-items: center;
margin-bottom: 15px;
}

.skill-name {
color: white;
font-weight: 500;
font-size: 1.1rem;
}

.skill-progress {
margin-bottom: 10px;
}

.skill-details {
display: flex;
justify-content: space-between;
align-items: center;
}

.skill-score {
color: white;
font-weight: bold;
}

.skill-change {
font-size: 0.9rem;
font-weight: 500;
}

.skill-change.positive {
color: #67c23a;
}

.skill-change.negative {
color: #f56c6c;
}

/* 改进建议 */
.suggestions-list {
display: flex;
flex-direction: column;
gap: 20px;
}

.suggestion-item {
background: rgba(255, 255, 255, 0.1);
border-radius: 12px;
padding: 20px;
}

.suggestion-header {
display: flex;
align-items: center;
gap: 12px;
margin-bottom: 15px;
}

.suggestion-header h4 {
color: white;
margin: 0;
flex: 1;
}

.suggestion-content {
color: rgba(255, 255, 255, 0.9);
line-height: 1.6;
margin-bottom: 15px;
}

.suggestion-actions {
display: flex;
gap: 10px;
}

/* 面试表现分析 */
.performance-grid {
display: grid;
grid-template-columns: 1fr 1fr;
gap: 20px;
}

.performance-card {
background: rgba(255, 255, 255, 0.1);
border-radius: 12px;
padding: 20px;
display: flex;
gap: 15px;
}

.performance-icon {
width: 50px;
height: 50px;
border-radius: 50%;
display: flex;
align-items: center;
justify-content: center;
font-size: 1.5rem;
flex-shrink: 0;
}

.performance-icon.success {
background: rgba(103, 194, 58, 0.2);
color: #67c23a;
}

.performance-icon.warning {
background: rgba(230, 162, 60, 0.2);
color: #e6a23c;
}

.performance-info h4 {
color: white;
margin: 0 0 10px 0;
}

.performance-info ul {
margin: 0;
padding-left: 20px;
color: rgba(255, 255, 255, 0.8);
}

.performance-info li {
margin-bottom: 5px;
}

/* 学习路径 */
.path-timeline {
position: relative;
}

.path-timeline::before {
content: '';
position: absolute;
left: 20px;
top: 0;
bottom: 0;
width: 2px;
background: rgba(255, 255, 255, 0.3);
}

.timeline-item {
position: relative;
padding-left: 60px;
margin-bottom: 30px;
}

.timeline-marker {
position: absolute;
left: 0;
top: 0;
width: 40px;
height: 40px;
border-radius: 50%;
background: rgba(255, 255, 255, 0.2);
display: flex;
align-items: center;
justify-content: center;
border: 2px solid rgba(255, 255, 255, 0.3);
}

.timeline-item.completed .timeline-marker {
background: #67c23a;
border-color: #67c23a;
}

.timeline-item.current .timeline-marker {
background: #409eff;
border-color: #409eff;
animation: pulse 2s infinite;
}

@keyframes pulse {
0% {
    box-shadow: 0 0 0 0 rgba(64, 158, 255, 0.7);
}
70% {
    box-shadow: 0 0 0 10px rgba(64, 158, 255, 0);
}
100% {
    box-shadow: 0 0 0 0 rgba(64, 158, 255, 0);
}
}

.step-number {
color: white;
font-weight: bold;
font-size: 0.9rem;
}

.timeline-content {
background: rgba(255, 255, 255, 0.1);
border-radius: 12px;
padding: 20px;
}

.timeline-content h4 {
color: white;
margin: 0 0 10px 0;
}

.timeline-content p {
color: rgba(255, 255, 255, 0.8);
margin-bottom: 15px;
line-height: 1.6;
}

.step-meta {
display: flex;
gap: 20px;
margin-bottom: 15px;
font-size: 0.9rem;
}

.duration,
.difficulty {
color: rgba(255, 255, 255, 0.7);
}

/* 响应式设计 */
@media (max-width: 768px) {
    .header-content {
        padding: 0 15px;
    }

    .main-content {
        padding: 20px 15px;
    }

    .score-card {
        flex-direction: column;
        text-align: center;
        gap: 30px;
    }

    .content-grid {
        grid-template-columns: 1fr;
    }

    .performance-grid {
        grid-template-columns: 1fr;
    }

    .detail-item {
        flex-direction: column;
        align-items: flex-start;
        gap: 10px;
    }

    .detail-label {
        min-width: auto;
    }
}
</style>

