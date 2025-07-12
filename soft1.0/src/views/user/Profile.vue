<template>
  <div class="profile-wrapper">
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
          <el-icon><User /></el-icon>
          个人中心
        </h1>
        <div class="nav-right"></div>
      </div>
    </header>

    <!-- 主要内容区域 -->
    <main class="main-content">
      <!-- 个人信息卡片 -->
      <section class="profile-card">
        <div class="profile-header">
          <div class="avatar-section">
            <div class="avatar-container">
              <img v-if="userInfo.avatar" :src="userInfo.avatar" alt="头像" class="avatar" />
              <div v-else class="avatar-placeholder">
                <el-icon><User /></el-icon>
              </div>
              <div class="avatar-overlay" @click="changeAvatar">
                <el-icon><Camera /></el-icon>
              </div>
            </div>
            <div class="upload-tip">点击更换头像</div>
          </div>
          
          <div class="profile-info">
            <h2 class="username">{{ userInfo.name }}</h2>
            <div class="user-meta">
              <el-tag :type="getLevelType(userInfo.level)" size="large">
                {{ userInfo.level }}
              </el-tag>
              <span class="join-date">加入时间: {{ userInfo.joinDate }}</span>
            </div>
            <div class="user-stats">
              <div class="stat-item">
                <span class="stat-number">{{ userInfo.totalInterviews }}</span>
                <span class="stat-label">面试次数</span>
              </div>
              <div class="stat-item">
                <span class="stat-number">{{ userInfo.avgScore }}%</span>
                <span class="stat-label">平均得分</span>
              </div>
              <div class="stat-item">
                <span class="stat-number">{{ userInfo.rank }}</span>
                <span class="stat-label">全站排名</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 功能区域 -->
      <div class="content-grid">
        <!-- 基本信息 -->
        <section class="info-section">
          <div class="section-header">
            <h3>
              <el-icon><EditPen /></el-icon>
              基本信息
            </h3>
            <el-button 
              type="primary" 
              size="small" 
              @click="editMode = !editMode"
            >
              {{ editMode ? '保存' : '编辑' }}
            </el-button>
          </div>
          
          <div class="info-form">
            <div class="form-row">
              <label>姓名</label>
              <el-input 
                v-if="editMode" 
                v-model="editForm.name" 
                placeholder="请输入姓名"
              />
              <span v-else class="info-value">{{ userInfo.name }}</span>
            </div>
            
            <div class="form-row">
              <label>邮箱</label>
              <el-input 
                v-if="editMode" 
                v-model="editForm.email" 
                placeholder="请输入邮箱"
              />
              <span v-else class="info-value">{{ userInfo.email }}</span>
            </div>
            
            <div class="form-row">
              <label>手机号</label>
              <el-input 
                v-if="editMode" 
                v-model="editForm.phone" 
                placeholder="请输入手机号"
              />
              <span v-else class="info-value">{{ userInfo.phone }}</span>
            </div>
            
            <div class="form-row">
              <label>学校/公司</label>
              <el-input 
                v-if="editMode" 
                v-model="editForm.organization" 
                placeholder="请输入学校或公司"
              />
              <span v-else class="info-value">{{ userInfo.organization }}</span>
            </div>
            
            <div class="form-row">
              <label>专业/岗位</label>
              <el-input 
                v-if="editMode" 
                v-model="editForm.major" 
                placeholder="请输入专业或岗位"
              />
              <span v-else class="info-value">{{ userInfo.major }}</span>
            </div>
            
            <div class="form-row">
              <label>个人简介</label>
              <el-input 
                v-if="editMode" 
                v-model="editForm.bio" 
                type="textarea" 
                :rows="3"
                placeholder="请输入个人简介"
              />
              <span v-else class="info-value bio">{{ userInfo.bio }}</span>
            </div>
          </div>
        </section>

        <!-- 偏好设置 -->
        <section class="preferences-section">
          <div class="section-header">
            <h3>
              <el-icon><Setting /></el-icon>
              偏好设置
            </h3>
          </div>
          
          <div class="preferences-form">
            <div class="preference-item">
              <div class="preference-label">
                <span>面试难度偏好</span>
                <el-tooltip content="选择您偏好的面试难度级别" placement="top">
                  <el-icon><QuestionFilled /></el-icon>
                </el-tooltip>
              </div>
              <el-select v-model="preferences.difficulty" placeholder="选择难度">
                <el-option label="初级" value="beginner"></el-option>
                <el-option label="中级" value="intermediate"></el-option>
                <el-option label="高级" value="advanced"></el-option>
              </el-select>
            </div>
            
            <div class="preference-item">
              <div class="preference-label">
                <span>面试时长偏好</span>
                <el-tooltip content="选择您偏好的面试时长" placement="top">
                  <el-icon><QuestionFilled /></el-icon>
                </el-tooltip>
              </div>
              <el-select v-model="preferences.duration" placeholder="选择时长">
                <el-option label="30分钟" value="30"></el-option>
                <el-option label="45分钟" value="45"></el-option>
                <el-option label="60分钟" value="60"></el-option>
              </el-select>
            </div>
            
            <div class="preference-item">
              <div class="preference-label">
                <span>语音识别</span>
                <el-tooltip content="开启后可以使用语音回答问题" placement="top">
                  <el-icon><QuestionFilled /></el-icon>
                </el-tooltip>
              </div>
              <el-switch v-model="preferences.voiceRecognition" />
            </div>
            
            <div class="preference-item">
              <div class="preference-label">
                <span>实时提示</span>
                <el-tooltip content="面试过程中显示实时提示" placement="top">
                  <el-icon><QuestionFilled /></el-icon>
                </el-tooltip>
              </div>
              <el-switch v-model="preferences.realTimeHints" />
            </div>
            
            <div class="preference-item">
              <div class="preference-label">
                <span>邮件通知</span>
                <el-tooltip content="接收面试结果和系统通知邮件" placement="top">
                  <el-icon><QuestionFilled /></el-icon>
                </el-tooltip>
              </div>
              <el-switch v-model="preferences.emailNotification" />
            </div>
          </div>
        </section>

        <!-- 技能标签 -->
        <section class="skills-section">
          <div class="section-header">
            <h3>
              <el-icon><Medal /></el-icon>
              技能标签
            </h3>
            <el-button type="primary" size="small" @click="showSkillDialog = true">
              <el-icon><Plus /></el-icon>
              添加技能
            </el-button>
          </div>
          
          <div class="skills-container">
            <div 
              v-for="skill in userSkills" 
              :key="skill.id"
              class="skill-tag"
            >
              <span class="skill-name">{{ skill.name }}</span>
              <div class="skill-level">
                <el-rate 
                  v-model="skill.level" 
                  :max="5" 
                  disabled 
                  show-score 
                  text-color="#ff9900"
                />
              </div>
              <el-button 
                type="danger" 
                size="small" 
                circle 
                @click="removeSkill(skill.id)"
              >
                <el-icon><Close /></el-icon>
              </el-button>
            </div>
          </div>
        </section>

        <!-- 安全设置 -->
        <section class="security-section">
          <div class="section-header">
            <h3>
              <el-icon><Lock /></el-icon>
              安全设置
            </h3>
          </div>
          
          <div class="security-items">
            <div class="security-item" @click="changePassword">
              <div class="security-info">
                <el-icon><Key /></el-icon>
                <div>
                  <h4>修改密码</h4>
                  <p>定期更换密码，保护账户安全</p>
                </div>
              </div>
              <el-icon class="arrow"><ArrowRight /></el-icon>
            </div>
            
            <div class="security-item" @click="bindPhone">
              <div class="security-info">
                <el-icon><Phone /></el-icon>
                <div>
                  <h4>手机绑定</h4>
                  <p>{{ userInfo.phone ? '已绑定' : '未绑定' }}</p>
                </div>
              </div>
              <el-icon class="arrow"><ArrowRight /></el-icon>
            </div>
            
            <div class="security-item" @click="bindEmail">
              <div class="security-info">
                <el-icon><Message /></el-icon>
                <div>
                  <h4>邮箱绑定</h4>
                  <p>{{ userInfo.email ? '已绑定' : '未绑定' }}</p>
                </div>
              </div>
              <el-icon class="arrow"><ArrowRight /></el-icon>
            </div>
          </div>
        </section>
      </div>
    </main>

    <!-- 添加技能对话框 -->
    <el-dialog v-model="showSkillDialog" title="添加技能" width="400px">
      <el-form :model="newSkill" label-width="80px">
        <el-form-item label="技能名称">
          <el-input v-model="newSkill.name" placeholder="请输入技能名称" />
        </el-form-item>
        <el-form-item label="熟练程度">
          <el-rate v-model="newSkill.level" :max="5" show-text />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showSkillDialog = false">取消</el-button>
        <el-button type="primary" @click="addSkill">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  ArrowLeft,
  User,
  Camera,
  EditPen,
  Setting,
  QuestionFilled,
  Medal,
  Plus,
  Close,
  Lock,
  Key,
  Phone,
  Message,
  ArrowRight
} from '@element-plus/icons-vue'

const router = useRouter()

// 编辑模式
const editMode = ref(false)
const showSkillDialog = ref(false)

// 用户信息
const userInfo = ref({
  name: '张同学',
  email: 'zhang@example.com',
  phone: '138****8888',
  organization: '某某大学',
  major: '计算机科学与技术',
  bio: '热爱编程，喜欢学习新技术，目标是成为一名优秀的软件工程师。',
  avatar: '',
  level: '中级',
  joinDate: '2023-09-01',
  totalInterviews: 15,
  avgScore: 82,
  rank: 156
})

// 编辑表单
const editForm = reactive({
  name: userInfo.value.name,
  email: userInfo.value.email,
  phone: userInfo.value.phone,
  organization: userInfo.value.organization,
  major: userInfo.value.major,
  bio: userInfo.value.bio
})

// 偏好设置
const preferences = reactive({
  difficulty: 'intermediate',
  duration: '45',
  voiceRecognition: true,
  realTimeHints: false,
  emailNotification: true
})

// 用户技能
const userSkills = ref([
  { id: 1, name: 'JavaScript', level: 4 },
  { id: 2, name: 'Vue.js', level: 4 },
  { id: 3, name: 'Python', level: 3 },
  { id: 4, name: 'Java', level: 3 },
  { id: 5, name: '算法与数据结构', level: 3 }
])

// 新技能
const newSkill = reactive({
  name: '',
  level: 1
})

// 获取等级类型
const getLevelType = (level) => {
  const types = {
    '初级': 'info',
    '中级': 'warning',
    '高级': 'success',
    '专家': 'danger'
  }
  return types[level] || 'info'
}

// 返回首页
const goBack = () => {
  router.push('/home')
}

// 更换头像
const changeAvatar = () => {
  ElMessage.info('头像上传功能开发中...')
  // 这里可以实现文件上传功能
}

// 添加技能
const addSkill = () => {
  if (!newSkill.name.trim()) {
    ElMessage.warning('请输入技能名称')
    return
  }
  
  const skill = {
    id: Date.now(),
    name: newSkill.name,
    level: newSkill.level
  }
  
  userSkills.value.push(skill)
  newSkill.name = ''
  newSkill.level = 1
  showSkillDialog.value = false
  ElMessage.success('技能添加成功')
}

// 移除技能
const removeSkill = (skillId) => {
  const index = userSkills.value.findIndex(skill => skill.id === skillId)
  if (index > -1) {
    userSkills.value.splice(index, 1)
    ElMessage.success('技能移除成功')
  }
}

// 修改密码
const changePassword = () => {
  ElMessage.info('修改密码功能开发中...')
}

// 绑定手机
const bindPhone = () => {
  ElMessage.info('手机绑定功能开发中...')
}

// 绑定邮箱
const bindEmail = () => {
  ElMessage.info('邮箱绑定功能开发中...')
}

// 组件挂载
onMounted(() => {
  console.log('个人中心页面已加载')
})
</script>

<style scoped>
.profile-wrapper {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
}

.profile-wrapper::before {
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

/* 个人信息卡片 */
.profile-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(15px);
  border-radius: 20px;
  padding: 40px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  margin-bottom: 30px;
}

.profile-header {
  display: flex;
  gap: 40px;
  align-items: center;
}

.avatar-section {
  text-align: center;
}

.avatar-container {
  position: relative;
  width: 120px;
  height: 120px;
  margin: 0 auto 15px;
}

.avatar,
.avatar-placeholder {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}

.avatar-placeholder {
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 3rem;
}

.avatar-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
  opacity: 0;
  cursor: pointer;
  transition: opacity 0.3s ease;
}

.avatar-container:hover .avatar-overlay {
  opacity: 1;
}

.upload-tip {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.8rem;
}

.profile-info {
  flex: 1;
}

.username {
  color: white;
  font-size: 2rem;
  margin-bottom: 15px;
}

.user-meta {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 25px;
}

.join-date {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
}

.user-stats {
  display: flex;
  gap: 40px;
}

.stat-item {
  text-align: center;
}

.stat-number {
  display: block;
  color: #ffd700;
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 5px;
}

.stat-label {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
}

/* 内容网格 */
.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}

/* 通用区域样式 */
.info-section,
.preferences-section,
.skills-section,
.security-section {
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

/* 基本信息表单 */
.info-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-row {
  display: flex;
  align-items: center;
  gap: 15px;
}

.form-row label {
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
  min-width: 80px;
  text-align: right;
}

.info-value {
  color: white;
  flex: 1;
}

.info-value.bio {
  line-height: 1.6;
}

/* 偏好设置 */
.preferences-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.preference-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.preference-label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: rgba(255, 255, 255, 0.9);
}

/* 技能标签 */
.skills-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.skill-tag {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 15px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 15px;
}

.skill-name {
  color: white;
  font-weight: 500;
  min-width: 100px;
}

.skill-level {
  flex: 1;
}

/* 安全设置 */
.security-items {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.security-item {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  transition: all 0.3s ease;
}

.security-item:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateX(5px);
}

.security-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.security-info h4 {
  color: white;
  margin: 0 0 5px 0;
  font-size: 1rem;
}

.security-info p {
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
  font-size: 0.9rem;
}

.arrow {
  color: rgba(255, 255, 255, 0.5);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-content {
    padding: 0 15px;
  }
  
  .main-content {
    padding: 20px 15px;
  }
  
  .profile-header {
    flex-direction: column;
    text-align: center;
    gap: 25px;
  }
  
  .user-stats {
    justify-content: center;
    gap: 25px;
  }
  
  .content-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .form-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .form-row label {
    min-width: auto;
    text-align: left;
  }
  
  .preference-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .skill-tag {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
}
</style>