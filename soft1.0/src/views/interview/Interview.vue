<template>
<div class="interview-container">
    <!-- 顶部信息栏 -->
    <div class="top-info">
    <div class="interview-header">
        <div class="position-info">
        <h2>{{ positionInfo.name }}</h2>
        <div class="interview-meta">
            <el-tag type="info">{{ positionInfo.difficulty }}</el-tag>
            <span class="duration">预计时长: {{ positionInfo.duration }}分钟</span>
        </div>
        </div>
        <div class="timer-section">
        <div class="timer">
            <el-icon><Timer /></el-icon>
            <span class="time-display">{{ formatTime(remainingTime) }}</span>
        </div>
        <div class="progress-info">
            <span>{{ currentQuestionIndex + 1 }} / {{ questions.length }}</span>
        </div>
        </div>
    </div>
    </div>

    <!-- 主要面试区域 -->
    <div class="interview-main">
    <!-- 问题显示区域 -->
    <div class="question-section">
        <el-card class="question-card">
        <div class="question-header">
            <div class="question-type">
                <el-icon>
                    <component :is="getQuestionIcon(currentQuestion.type)" />
                </el-icon>
            <span>{{ getQuestionTypeName(currentQuestion.type) }}</span>
            </div>
            <div class="question-difficulty">
            <el-rate v-model="currentQuestion.difficulty" disabled show-score text-color="#ff9900" />
            </div>
        </div>
        <div class="question-content">
            <h3>{{ currentQuestion.title }}</h3>
            <div class="question-description" v-html="currentQuestion.description"></div>
            <div v-if="currentQuestion.codeTemplate" class="code-template">
            <h4>代码模板:</h4>
            <pre><code>{{ currentQuestion.codeTemplate }}</code></pre>
            </div>
        </div>
        </el-card>
    </div>

    <!-- 回答区域 -->
    <div class="answer-section">
        <el-card class="answer-card">
        <template #header>
            <div class="answer-header">
            <span>您的回答</span>
            <div class="answer-tools">
                <el-button v-if="!isRecording" @click="startRecording" type="primary" size="small">
                <el-icon><Microphone /></el-icon>
                开始录音
                </el-button>
                <el-button v-else @click="stopRecording" type="danger" size="small">
                <el-icon><VideoPause /></el-icon>
                停止录音
                </el-button>
                <el-button @click="clearAnswer" size="small">
                <el-icon><Delete /></el-icon>
                清空
                </el-button>
            </div>
            </div>
        </template>
        
        <!-- 文本回答 -->
        <div v-if="currentQuestion.type !== 'coding'" class="text-answer">
            <el-input
            v-model="currentAnswer.text"
            type="textarea"
            :rows="8"
            placeholder="请输入您的回答..."
            show-word-limit
            maxlength="2000"
            />
        </div>
        
        <!-- 代码回答 -->
        <div v-else class="code-answer">
            <div class="code-editor">
            <el-select v-model="selectedLanguage" placeholder="选择编程语言" style="width: 200px; margin-bottom: 1rem;">
                <el-option label="JavaScript" value="javascript" />
                <el-option label="Python" value="python" />
                <el-option label="Java" value="java" />
                <el-option label="C++" value="cpp" />
            </el-select>
            <el-input
                v-model="currentAnswer.code"
                type="textarea"
                :rows="12"
                placeholder="请输入您的代码..."
                class="code-input"
            />
            </div>
            <div class="code-actions">
            <el-button @click="runCode" type="success" size="small">
                <el-icon><CaretRight /></el-icon>
                运行代码
            </el-button>
            <el-button @click="formatCode" size="small">
                <el-icon><Document /></el-icon>
                格式化
            </el-button>
            </div>
        </div>
        
        <!-- 录音状态显示 -->
        <div v-if="isRecording" class="recording-status">
            <div class="recording-indicator">
            <div class="recording-dot"></div>
            <span>正在录音... {{ formatTime(recordingTime) }}</span>
            </div>
            <div class="audio-visualizer">
            <div v-for="i in 20" :key="i" class="audio-bar" :style="{ height: Math.random() * 100 + '%' }"></div>
            </div>
        </div>
        </el-card>
    </div>
    </div>

    <!-- 底部操作栏 -->
    <div class="bottom-actions">
    <div class="action-buttons">
        <el-button @click="previousQuestion" :disabled="currentQuestionIndex === 0" size="large">
        <el-icon><ArrowLeft /></el-icon>
        上一题
        </el-button>
        
        <el-button @click="saveAnswer" type="info" size="large">
        <el-icon><DocumentAdd /></el-icon>
        保存回答
        </el-button>
        
        <el-button @click="skipQuestion" size="large">
        <el-icon><Right /></el-icon>
        跳过
        </el-button>
        
        <el-button 
        v-if="currentQuestionIndex < questions.length - 1"
        @click="nextQuestion" 
        type="primary" 
        size="large"
        >
        下一题
        <el-icon><ArrowRight /></el-icon>
        </el-button>
        
        <el-button 
        v-else
        @click="finishInterview" 
        type="success" 
        size="large"
        >
        完成面试
        <el-icon><Check /></el-icon>
        </el-button>
    </div>
    
    <div class="help-section">
        <el-button @click="showHint" type="text" size="small">
        <el-icon><QuestionFilled /></el-icon>
        提示
        </el-button>
        <el-button @click="pauseInterview" type="text" size="small">
        <el-icon><VideoPause /></el-icon>
        暂停
        </el-button>
        <el-button @click="exitInterview" type="text" size="small">
        <el-icon><Close /></el-icon>
        退出
        </el-button>
    </div>
    </div>

    <!-- 提示弹窗 -->
    <el-dialog v-model="showHintDialog" title="答题提示" width="50%">
    <div class="hint-content">
        <p>{{ currentQuestion.hint }}</p>
        <div class="hint-tags">
        <el-tag v-for="tag in currentQuestion.tags" :key="tag" size="small">{{ tag }}</el-tag>
        </div>
    </div>
    </el-dialog>

    <!-- 暂停弹窗 -->
    <el-dialog v-model="showPauseDialog" title="面试已暂停" width="40%" :show-close="false">
    <div class="pause-content">
        <el-icon size="48" color="#409eff"><VideoPause /></el-icon>
        <p>面试已暂停，您可以稍作休息</p>
        <p class="pause-time">暂停时间: {{ formatTime(pausedTime) }}</p>
    </div>
    <template #footer>
        <el-button @click="resumeInterview" type="primary">继续面试</el-button>
    </template>
    </el-dialog>
</div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
Timer, Microphone, VideoPause, Delete, CaretRight, Document,
ArrowLeft, ArrowRight, DocumentAdd, Right, Check, QuestionFilled,
Close, ChatDotRound, Setting, User
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

// 岗位信息
const positionInfo = reactive({
id: route.params.id,
name: '人工智能工程师',
difficulty: '中级',
duration: 60
})

// 面试状态
const remainingTime = ref(3600) // 60分钟
const currentQuestionIndex = ref(0)
const isRecording = ref(false)
const recordingTime = ref(0)
const selectedLanguage = ref('javascript')
const showHintDialog = ref(false)
const showPauseDialog = ref(false)
const pausedTime = ref(0)
const isPaused = ref(false)

// 当前回答
const currentAnswer = reactive({
text: '',
code: '',
audioBlob: null
})

// 面试问题数据
const questions = ref([
{
    id: 1,
    type: 'behavioral',
    title: '请简单介绍一下您自己',
    description: '请用3-5分钟的时间介绍您的教育背景、技能特长、项目经验以及为什么对这个岗位感兴趣。',
    difficulty: 2,
    hint: '可以按照教育背景 → 技能特长 → 项目经验 → 职业目标的顺序来组织回答',
    tags: ['自我介绍', '基础问题']
},
{
    id: 2,
    type: 'technical',
    title: '什么是机器学习？请解释监督学习和无监督学习的区别',
    description: '请详细解释机器学习的概念，并说明监督学习和无监督学习的主要区别，各自的应用场景。',
    difficulty: 3,
    hint: '可以从定义、数据特点、算法类型、应用场景等角度来对比',
    tags: ['机器学习', '基础概念']
},
{
    id: 3,
    type: 'coding',
    title: '实现一个简单的线性回归算法',
    description: '请用您熟悉的编程语言实现一个简单的线性回归算法，包括训练和预测功能。',
    difficulty: 4,
    hint: '可以使用梯度下降法来优化参数，注意处理数据的标准化',
    tags: ['算法实现', '线性回归'],
    codeTemplate: `# Python 模板
class LinearRegression:
    def __init__(self):
        self.weights = None
        self.bias = None
    
    def fit(self, X, y):
        # 实现训练逻辑
        pass
    
    def predict(self, X):
        # 实现预测逻辑
        pass`
},
{
    id: 4,
    type: 'scenario',
    title: '如何处理数据不平衡问题？',
    description: '在实际项目中，经常会遇到数据不平衡的问题。请描述您会如何识别和解决这类问题。',
    difficulty: 4,
    hint: '可以从数据层面、算法层面、评估层面来考虑解决方案',
    tags: ['数据处理', '实际应用']
},
{
    id: 5,
    type: 'behavioral',
    title: '描述一次您解决技术难题的经历',
    description: '请详细描述一次您在项目中遇到技术难题并成功解决的经历，包括问题的背景、解决过程和最终结果。',
    difficulty: 3,
    hint: '可以使用STAR法则来组织回答：情境、任务、行动、结果',
    tags: ['问题解决', '项目经验']
}
])

// 当前问题
const currentQuestion = computed(() => questions.value[currentQuestionIndex.value])

// 定时器
let timer: number | null = null
let recordingTimer: number | null = null
let pauseTimer: number | null = null

// 获取问题类型图标
const getQuestionIcon = (type: string) => {
const icons = {
    behavioral: User,
    technical: ChatDotRound,
    coding: Setting,
    scenario: QuestionFilled
}
return icons[type as keyof typeof icons] || QuestionFilled
}

// 获取问题类型名称
const getQuestionTypeName = (type: string) => {
const names = {
    behavioral: '行为面试',
    technical: '技术问答',
    coding: '编程题',
    scenario: '场景题'
}
return names[type as keyof typeof names] || '其他'
}

// 格式化时间
const formatTime = (seconds: number) => {
const mins = Math.floor(seconds / 60)
const secs = seconds % 60
return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

// 开始录音
const startRecording = async () => {
try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    isRecording.value = true
    recordingTime.value = 0
    
    recordingTimer = setInterval(() => {
    recordingTime.value++
    }, 1000)
    
    ElMessage.success('开始录音')
} catch (error) {
    ElMessage.error('无法访问麦克风，请检查权限设置')
}
}

// 停止录音
const stopRecording = () => {
isRecording.value = false
if (recordingTimer) {
    clearInterval(recordingTimer)
    recordingTimer = null
}
ElMessage.success('录音已停止')
}

// 清空回答
const clearAnswer = () => {
currentAnswer.text = ''
currentAnswer.code = ''
ElMessage.success('已清空回答')
}

// 运行代码
const runCode = () => {
ElMessage.info('代码运行功能开发中...')
}

// 格式化代码
const formatCode = () => {
ElMessage.info('代码格式化功能开发中...')
}

// 保存回答
const saveAnswer = () => {
// 这里可以实现保存逻辑
ElMessage.success('回答已保存')
}

// 上一题
const previousQuestion = () => {
if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--
    clearAnswer()
}
}

// 下一题
const nextQuestion = () => {
if (currentQuestionIndex.value < questions.value.length - 1) {
    currentQuestionIndex.value++
    clearAnswer()
}
}

// 跳过问题
const skipQuestion = () => {
ElMessageBox.confirm('确定要跳过这道题吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
}).then(() => {
    nextQuestion()
})
}

// 显示提示
const showHint = () => {
showHintDialog.value = true
}

// 暂停面试
const pauseInterview = () => {
isPaused.value = true
showPauseDialog.value = true
pausedTime.value = 0

if (timer) {
    clearInterval(timer)
}

pauseTimer = setInterval(() => {
    pausedTime.value++
}, 1000)
}

// 继续面试
const resumeInterview = () => {
isPaused.value = false
showPauseDialog.value = false

if (pauseTimer) {
    clearInterval(pauseTimer)
    pauseTimer = null
}

startTimer()
}

// 退出面试
const exitInterview = () => {
ElMessageBox.confirm('确定要退出面试吗？退出后将无法恢复当前进度。', '确认退出', {
    confirmButtonText: '确定退出',
    cancelButtonText: '取消',
    type: 'warning'
}).then(() => {
    router.push('/home')
})
}

// 完成面试
const finishInterview = () => {
ElMessageBox.confirm('确定要完成面试吗？', '完成面试', {
    confirmButtonText: '完成',
    cancelButtonText: '继续答题',
    type: 'success'
}).then(() => {
    ElMessage.success('面试已完成！')
    router.push('/history')
})
}

// 开始计时
const startTimer = () => {
timer = setInterval(() => {
    if (!isPaused.value && remainingTime.value > 0) {
    remainingTime.value--
    }
    if (remainingTime.value === 0) {
    ElMessage.warning('面试时间已到！')
    finishInterview()
    }
}, 1000)
}

// 组件挂载
onMounted(() => {
// 根据路由参数设置岗位信息
const positionMap = {
    '1': { name: '前端开发工程师', difficulty: '中级', duration: 30 },
    '2': { name: '后端开发工程师', difficulty: '高级', duration: 45 },
    '3': { name: '人工智能工程师', difficulty: '初级', duration: 30 },
    '4': { name: '大数据工程师', difficulty: '高级', duration: 50 },
    '5': { name: '产品经理', difficulty: '中级', duration: 40 },
    '6': { name: 'UI/UX设计师', difficulty: '初级', duration: 35 }
}

const position = positionMap[route.params.id as keyof typeof positionMap]
if (position) {
    Object.assign(positionInfo, position)
    remainingTime.value = position.duration * 60
}

startTimer()
})

// 组件卸载
onUnmounted(() => {
if (timer) clearInterval(timer)
if (recordingTimer) clearInterval(recordingTimer)
if (pauseTimer) clearInterval(pauseTimer)
})
</script>

<style scoped>
.interview-container {
min-height: 100vh;
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
display: flex;
flex-direction: column;
}

.top-info {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
padding: 1rem 2rem;
box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.bottom-actions {
background: linear-gradient(0deg, #ffffff 0%, #f8f9fa 100%);
padding: 1.5rem 2rem;
display: flex;
justify-content: space-between;
align-items: center;
box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
}

.interview-header {
display: flex;
justify-content: space-between;
align-items: center;
}

.position-info h2 {
margin: 0 0 0.5rem 0;
color: #2c3e50;
font-size: 24px;
}

.interview-meta {
display: flex;
align-items: center;
gap: 1rem;
}

.duration {
color: #606266;
font-size: 14px;
}

.timer-section {
display: flex;
align-items: center;
gap: 2rem;
}

.timer {
display: flex;
align-items: center;
gap: 0.5rem;
font-size: 18px;
font-weight: 600;
color: #409eff;
}

.time-display {
font-family: 'Courier New', monospace;
}

.progress-info {
color: #606266;
font-weight: 500;
}

.interview-main {
flex: 1;
display: grid;
grid-template-columns: 1fr 1fr;
gap: 2rem;
padding: 2rem;
max-width: 1400px;
margin: 0 auto;
width: 100%;
}

.question-card, .answer-card {
border-radius: 16px;
box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
border: none;
height: fit-content;
}

.question-header {
display: flex;
justify-content: space-between;
align-items: center;
margin-bottom: 1.5rem;
}

.question-type {
display: flex;
align-items: center;
gap: 0.5rem;
color: #409eff;
font-weight: 500;
}

.question-content h3 {
color: #2c3e50;
margin-bottom: 1rem;
font-size: 18px;
line-height: 1.6;
}

.question-description {
color: #606266;
line-height: 1.8;
margin-bottom: 1rem;
}

.code-template {
background: #f8f9fa;
border-radius: 8px;
padding: 1rem;
margin-top: 1rem;
}

.code-template h4 {
margin: 0 0 0.5rem 0;
color: #2c3e50;
}

.code-template pre {
margin: 0;
font-family: 'Courier New', monospace;
font-size: 14px;
color: #2c3e50;
white-space: pre-wrap;
}

.answer-header {
display: flex;
justify-content: space-between;
align-items: center;
}

.answer-tools {
display: flex;
gap: 0.5rem;
}

.code-editor {
margin-bottom: 1rem;
}

.code-input {
font-family: 'Courier New', monospace;
}

.code-actions {
display: flex;
gap: 0.5rem;
justify-content: flex-end;
}

.recording-status {
margin-top: 1rem;
padding: 1rem;
background: #f0f9ff;
border-radius: 8px;
border: 1px solid #409eff;
}

.recording-indicator {
display: flex;
align-items: center;
gap: 0.5rem;
margin-bottom: 1rem;
color: #409eff;
font-weight: 500;
}

.recording-dot {
width: 8px;
height: 8px;
background: #f56c6c;
border-radius: 50%;
animation: pulse 1s infinite;
}

@keyframes pulse {
0% { opacity: 1; }
50% { opacity: 0.5; }
100% { opacity: 1; }
}

.audio-visualizer {
display: flex;
align-items: end;
gap: 2px;
height: 40px;
}

.audio-bar {
width: 3px;
background: linear-gradient(to top, #409eff, #67c23a);
border-radius: 2px;
animation: wave 1s infinite ease-in-out;
}

.audio-bar:nth-child(even) {
animation-delay: 0.1s;
}

@keyframes wave {
0%, 100% { height: 10%; }
50% { height: 100%; }
}

.bottom-actions {
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
backdrop-filter: blur(10px);
padding: 1.5rem 2rem;
display: flex;
justify-content: space-between;
align-items: center;
box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
}

.action-buttons {
display: flex;
gap: 1rem;
}

.help-section {
display: flex;
gap: 0.5rem;
}

.hint-content {
text-align: center;
}

.hint-content p {
margin-bottom: 1rem;
color: #606266;
line-height: 1.6;
}

.hint-tags {
display: flex;
justify-content: center;
gap: 0.5rem;
flex-wrap: wrap;
}

.pause-content {
text-align: center;
padding: 2rem 0;
}

.pause-content p {
margin: 1rem 0;
color: #606266;
}

.pause-time {
font-size: 18px;
font-weight: 600;
color: #409eff;
font-family: 'Courier New', monospace;
}

@media (max-width: 1024px) {
.interview-main {
    grid-template-columns: 1fr;
    gap: 1rem;
    padding: 1rem;
}

.interview-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
}

.timer-section {
    justify-content: center;
}

.bottom-actions {
    flex-direction: column;
    gap: 1rem;
}

.action-buttons {
    flex-wrap: wrap;
    justify-content: center;
}
}

@media (max-width: 768px) {
.top-info, .bottom-actions {
    padding: 1rem;
}

.action-buttons {
    flex-direction: column;
    width: 100%;
}

.action-buttons .el-button {
    width: 100%;
}
}
</style>