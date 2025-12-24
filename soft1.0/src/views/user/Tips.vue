<template>
<div class="tips-container">
    <!-- 顶部导航 -->
    <div class="top-nav">
    <div class="nav-left">
        <el-button @click="$router.go(-1)" type="text" class="back-btn">
        <el-icon><ArrowLeft /></el-icon>
        返回
        </el-button>
        <h1>面试技巧</h1>
    </div>
    <div class="nav-right">
        <el-dropdown>
        <span class="user-info">
            <el-avatar :size="32" src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" />
            <span>{{ userInfo.name }}</span>
        </span>
        <template #dropdown>
            <el-dropdown-menu>
            <el-dropdown-item @click="$router.push('/profile')">个人中心</el-dropdown-item>
            <el-dropdown-item @click="logout" divided>退出登录</el-dropdown-item>
            </el-dropdown-menu>
        </template>
        </el-dropdown>
    </div>
    </div>

    <!-- 主要内容 -->
    <div class="main-content">
    <!-- 技巧分类 -->
    <div class="categories-section">
        <div class="category-tabs">
        <div 
            v-for="category in categories" 
            :key="category.id"
            :class="['category-tab', { active: activeCategory === category.id }]"
            @click="activeCategory = category.id"
        >
            <el-icon>{{ category.icon }}</el-icon>
            <span>{{ category.name }}</span>
        </div>
        </div>
    </div>

    <!-- 技巧内容 -->
    <div class="tips-content">
        <div class="tips-grid">
        <div v-for="tip in currentTips" :key="tip.id" class="tip-card">
            <el-card class="tip-item" @click="openTipDetail(tip)">
            <div class="tip-header">
                <div class="tip-icon">
                <el-icon>{{ tip.icon }}</el-icon>
                </div>
                <div class="tip-meta">
                <h3>{{ tip.title }}</h3>
                <div class="tip-tags">
                    <el-tag v-for="tag in tip.tags" :key="tag" size="small" type="info">{{ tag }}</el-tag>
                </div>
                </div>
                <div class="tip-difficulty">
                <el-rate v-model="tip.difficulty" disabled show-score text-color="#ff9900" />
                </div>
            </div>
            <div class="tip-preview">
                <p>{{ tip.preview }}</p>
            </div>
            <div class="tip-footer">
                <span class="read-time">阅读时间: {{ tip.readTime }}分钟</span>
                <el-button type="primary" size="small">查看详情</el-button>
            </div>
            </el-card>
        </div>
        </div>
    </div>

    <!-- 推荐资源 -->
    <div class="resources-section">
        <el-card class="resources-card">
        <template #header>
            <span>推荐学习资源</span>
        </template>
        <div class="resources-grid">
            <div v-for="resource in resources" :key="resource.id" class="resource-item">
            <div class="resource-icon">
                <el-icon>{{ resource.icon }}</el-icon>
            </div>
            <div class="resource-content">
                <h4>{{ resource.title }}</h4>
                <p>{{ resource.description }}</p>
                <el-button type="text" @click="openResource(resource)">访问资源</el-button>
            </div>
            </div>
        </div>
        </el-card>
    </div>
    </div>

    <!-- 技巧详情弹窗 -->
    <el-dialog v-model="showTipDetail" :title="selectedTip?.title" width="80%" class="tip-dialog">
    <div v-if="selectedTip" class="tip-detail">
        <div class="tip-detail-header">
        <div class="tip-detail-meta">
            <el-tag v-for="tag in selectedTip.tags" :key="tag" size="small">{{ tag }}</el-tag>
            <span class="difficulty">难度: </span>
            <el-rate v-model="selectedTip.difficulty" disabled show-score text-color="#ff9900" />
        </div>
        </div>
        <div class="tip-detail-content">
        <div v-for="section in selectedTip.content" :key="section.title" class="content-section">
            <h3>{{ section.title }}</h3>
            <div v-if="section.type === 'text'" class="text-content">
            <p v-for="paragraph in section.data" :key="paragraph">{{ paragraph }}</p>
            </div>
            <div v-else-if="section.type === 'list'" class="list-content">
            <ul>
                <li v-for="item in section.data" :key="item">{{ item }}</li>
            </ul>
            </div>
            <div v-else-if="section.type === 'steps'" class="steps-content">
            <el-steps :active="section.data.length" direction="vertical">
                <el-step v-for="(step, index) in section.data" :key="index" :title="step.title" :description="step.description" />
            </el-steps>
            </div>
        </div>
        </div>
    </div>
    </el-dialog>
</div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft, Document, ChatDotRound, User, Setting, Link } from '@element-plus/icons-vue'

const router = useRouter()

// 用户信息
const userInfo = reactive({
name: '张同学',
studentId: '2021001'
})

// 当前选中的分类
const activeCategory = ref('basic')

// 技巧分类
const categories = ref([
{ id: 'basic', name: '基础准备', icon: Document },
{ id: 'communication', name: '沟通技巧', icon: ChatDotRound },
{ id: 'behavior', name: '行为面试', icon: User },
{ id: 'technical', name: '技术面试', icon: Setting }
])

// 1. 定义 Tip 类型
interface Tip {
  id: number
  category: string
  title: string
  preview: string
  tags: string[]
  difficulty: number
  readTime: number
  icon: any
  content: any[]
}

// 所有技巧数据
const allTips = ref([
// 基础准备
{
    id: 1,
    category: 'basic',
    title: '面试前的充分准备',
    preview: '了解如何在面试前做好充分的准备工作，包括公司调研、简历优化等。',
    tags: ['准备工作', '简历', '公司调研'],
    difficulty: 2,
    readTime: 5,
    icon: Document,
    content: [
    {
        title: '公司背景调研',
        type: 'text',
        data: [
        '深入了解目标公司的业务模式、发展历程、企业文化和最新动态。',
        '研究公司的产品或服务，了解其在行业中的地位和竞争优势。',
        '关注公司的技术栈、团队结构和工作环境。'
        ]
    },
    {
        title: '简历优化要点',
        type: 'list',
        data: [
        '突出与目标岗位相关的技能和经验',
        '使用具体的数据和成果来证明能力',
        '保持简历格式清晰、内容简洁',
        '检查语法错误和拼写错误'
        ]
    }
    ]
},
{
    id: 2,
    category: 'basic',
    title: '着装与形象管理',
    preview: '学习如何通过得体的着装和良好的形象给面试官留下专业的第一印象。',
    tags: ['着装', '形象', '第一印象'],
    difficulty: 1,
    readTime: 3,
    icon: User,
    content: [
    {
        title: '着装建议',
        type: 'text',
        data: [
        '选择适合行业和公司文化的着装风格。',
        '保持服装整洁、合身，避免过于花哨的装饰。',
        '注意细节，如鞋子的清洁、配饰的搭配等。'
        ]
    }
    ]
},
// 沟通技巧
{
    id: 3,
    category: 'communication',
    title: '有效的自我介绍',
    preview: '掌握如何在短时间内进行有效的自我介绍，突出个人优势和价值。',
    tags: ['自我介绍', '表达技巧', '个人品牌'],
    difficulty: 3,
    readTime: 8,
    icon: ChatDotRound,
    content: [
    {
        title: '自我介绍结构',
        type: 'steps',
        data: [
        { title: '开场问候', description: '简洁的问候和感谢' },
        { title: '基本信息', description: '姓名、专业、学校等基本信息' },
        { title: '核心优势', description: '突出与岗位相关的技能和经验' },
        { title: '职业目标', description: '表达对岗位和公司的兴趣' },
        { title: '结束语', description: '表达期待和感谢' }
        ]
    }
    ]
},
// 行为面试
{
    id: 4,
    category: 'behavior',
    title: 'STAR法则应用',
    preview: '学习使用STAR法则来回答行为面试问题，让你的回答更有说服力。',
    tags: ['STAR法则', '行为面试', '案例分析'],
    difficulty: 4,
    readTime: 10,
    icon: Setting,
    content: [
    {
        title: 'STAR法则详解',
        type: 'steps',
        data: [
        { title: 'Situation (情境)', description: '描述具体的情境或背景' },
        { title: 'Task (任务)', description: '说明你需要完成的任务或目标' },
        { title: 'Action (行动)', description: '详细描述你采取的具体行动' },
        { title: 'Result (结果)', description: '说明最终的结果和收获' }
        ]
    }
    ]
},
// 技术面试
{
    id: 5,
    category: 'technical',
    title: '算法题解题思路',
    preview: '掌握算法面试的解题思路和技巧，提高技术面试的通过率。',
    tags: ['算法', '编程', '解题技巧'],
    difficulty: 5,
    readTime: 15,
    icon: Setting,
    content: [
    {
        title: '解题步骤',
        type: 'steps',
        data: [
        { title: '理解题意', description: '仔细阅读题目，确保完全理解要求' },
        { title: '分析思路', description: '思考可能的解决方案，选择最优方法' },
        { title: '编写代码', description: '按照思路编写清晰的代码' },
        { title: '测试验证', description: '用示例数据验证代码的正确性' },
        { title: '优化改进', description: '分析时间复杂度，考虑优化方案' }
        ]
    }
    ]
}
])

// 推荐资源
const resources = ref([
{
    id: 1,
    title: 'LeetCode 算法练习',
    description: '提供大量算法题目，帮助提升编程能力',
    icon: Link
},
{
    id: 2,
    title: '面试经验分享社区',
    description: '查看其他求职者的面试经验和技巧分享',
    icon: ChatDotRound
},
{
    id: 3,
    title: '在线模拟面试平台',
    description: '通过模拟面试提升面试表现和自信心',
    icon: User
},
{
    id: 4,
    title: '技术文档学习',
    description: '学习最新的技术文档和行业趋势',
    icon: Document
}
])

// 当前分类的技巧
const currentTips = computed(() => {
return allTips.value.filter(tip => tip.category === activeCategory.value)
})

// 技巧详情弹窗
const showTipDetail = ref(false)
const selectedTip = ref<Tip | null>(null)

// 打开技巧详情
const openTipDetail = (tip: any) => {
selectedTip.value = tip
showTipDetail.value = true
}

// 打开资源链接
const openResource = (resource: any) => {
ElMessage.info(`正在打开: ${resource.title}`)
// 这里可以添加实际的链接跳转逻辑
}

// 退出登录
const logout = () => {
ElMessage.success('已退出登录')
router.push('/login')
}
</script>

<style scoped>
.tips-container {
position: fixed;
top: 0;
left: 0;
width: 100vw;
height: 100vh;
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
overflow-y: auto;
padding: 0;
}

.top-nav {
background: rgba(255, 255, 255, 0.95);
backdrop-filter: blur(10px);
padding: 1rem 2rem;
display: flex;
justify-content: space-between;
align-items: center;
box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.nav-left {
display: flex;
align-items: center;
gap: 1rem;
}

.back-btn {
color: #409eff;
font-size: 16px;
}

.nav-left h1 {
margin: 0;
color: #2c3e50;
font-size: 24px;
font-weight: 600;
}

.user-info {
display: flex;
align-items: center;
gap: 8px;
cursor: pointer;
color: #2c3e50;
}

.main-content {
padding: 2rem;
max-width: 1200px;
margin: 0 auto;
}

.categories-section {
margin-bottom: 2rem;
}

.category-tabs {
display: flex;
gap: 1rem;
flex-wrap: wrap;
}

.category-tab {
display: flex;
align-items: center;
gap: 0.5rem;
padding: 0.75rem 1.5rem;
background: rgba(255, 255, 255, 0.9);
border-radius: 25px;
cursor: pointer;
transition: all 0.3s ease;
color: #606266;
font-weight: 500;
}

.category-tab:hover {
background: rgba(255, 255, 255, 1);
transform: translateY(-2px);
box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.category-tab.active {
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
color: white;
box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.tips-content {
margin-bottom: 2rem;
}

.tips-grid {
display: grid;
grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
gap: 1.5rem;
}

.tip-card {
cursor: pointer;
transition: transform 0.3s ease;
}

.tip-card:hover {
transform: translateY(-4px);
}

.tip-item {
border-radius: 16px;
border: none;
box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
overflow: hidden;
}

.tip-header {
display: flex;
align-items: flex-start;
gap: 1rem;
margin-bottom: 1rem;
}

.tip-icon {
width: 48px;
height: 48px;
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
border-radius: 12px;
display: flex;
align-items: center;
justify-content: center;
color: white;
font-size: 20px;
flex-shrink: 0;
}

.tip-meta {
flex: 1;
}

.tip-meta h3 {
margin: 0 0 0.5rem 0;
color: #2c3e50;
font-size: 16px;
font-weight: 600;
}

.tip-tags {
display: flex;
gap: 0.5rem;
flex-wrap: wrap;
}

.tip-difficulty {
flex-shrink: 0;
}

.tip-preview {
margin-bottom: 1rem;
}

.tip-preview p {
margin: 0;
color: #606266;
line-height: 1.6;
}

.tip-footer {
display: flex;
justify-content: space-between;
align-items: center;
padding-top: 1rem;
border-top: 1px solid #f0f0f0;
}

.read-time {
font-size: 14px;
color: #909399;
}

.resources-section {
margin-bottom: 2rem;
}

.resources-card {
border-radius: 16px;
box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
border: none;
}

.resources-grid {
display: grid;
grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
gap: 1rem;
padding: 1rem 0;
}

.resource-item {
display: flex;
gap: 1rem;
padding: 1rem;
background: #f8f9fa;
border-radius: 12px;
border: 1px solid #e9ecef;
transition: all 0.3s ease;
}

.resource-item:hover {
background: #e9ecef;
transform: translateY(-2px);
}

.resource-icon {
width: 40px;
height: 40px;
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
border-radius: 50%;
display: flex;
align-items: center;
justify-content: center;
color: white;
flex-shrink: 0;
}

.resource-content h4 {
margin: 0 0 0.5rem 0;
color: #2c3e50;
font-size: 14px;
}

.resource-content p {
margin: 0 0 0.5rem 0;
color: #606266;
font-size: 12px;
line-height: 1.4;
}

.tip-dialog {
border-radius: 16px;
}

.tip-detail-header {
margin-bottom: 1.5rem;
padding-bottom: 1rem;
border-bottom: 1px solid #f0f0f0;
}

.tip-detail-meta {
display: flex;
align-items: center;
gap: 1rem;
flex-wrap: wrap;
}

.difficulty {
color: #606266;
font-weight: 500;
}

.content-section {
margin-bottom: 2rem;
}

.content-section h3 {
color: #2c3e50;
margin-bottom: 1rem;
font-size: 18px;
}

.text-content p {
margin-bottom: 0.8rem;
line-height: 1.6;
color: #606266;
}

.list-content ul {
padding-left: 1.5rem;
}

.list-content li {
margin-bottom: 0.5rem;
line-height: 1.6;
color: #606266;
}

.steps-content {
margin-top: 1rem;
}

@media (max-width: 768px) {
.main-content {
    padding: 1rem;
}

.top-nav {
    padding: 1rem;
}

.category-tabs {
    justify-content: center;
}

.tips-grid {
    grid-template-columns: 1fr;
}

.resources-grid {
    grid-template-columns: 1fr;
}

.tip-header {
    flex-direction: column;
    align-items: center;
    text-align: center;
}
}
</style>