<template>
  <div class="register-container">
    <el-card class="register-box" shadow="always">
      <div class="register-header">
        <div class="logo-container">
          <el-icon class="logo-icon" size="48">
            <UserFilled />
          </el-icon>
        </div>
        <h2 class="register-title">创建新账户</h2>
        <p class="register-subtitle">加入智能面试系统，开启您的求职之旅</p>
      </div>
      
      <el-form :model="form" :rules="rules" ref="formRef" class="register-form" size="large">
        <el-form-item prop="username">
          <el-input 
            v-model="form.username" 
            placeholder="请输入用户名"
            prefix-icon="User"
            class="register-input"
          />
        </el-form-item>
        
        <el-form-item prop="email">
          <el-input 
            v-model="form.email" 
            placeholder="请输入邮箱"
            prefix-icon="Message"
            class="register-input"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input 
            v-model="form.password" 
            type="password" 
            placeholder="请输入密码（至少6位）"
            prefix-icon="Lock"
            class="register-input"
            show-password
          />
        </el-form-item>
        
        <el-form-item prop="confirmPassword">
          <el-input 
            v-model="form.confirmPassword" 
            type="password" 
            placeholder="请确认密码"
            prefix-icon="Lock"
            class="register-input"
            show-password
          />
        </el-form-item>
        
        <el-form-item class="register-actions">
          <el-button 
            type="primary" 
            @click="handleRegister" 
            class="register-btn"
            size="large"
            :loading="loading"
          >
            注册账户
          </el-button>
        </el-form-item>
        
        <div class="login-link">
          <span>已有账户？</span>
          <el-button type="text" @click="goLogin" class="login-btn-link">
            立即登录
          </el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { UserFilled, User, Lock, Message } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()
const loading = ref(false)
const formRef = ref()

// 修改这里：使用 reactive 而不是 ref
const form = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const validateConfirmPassword = (rule, value, callback) => {
  // 修改这里：直接访问 form.password 而不是 form.value.password
  if (value !== form.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const rules = reactive({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度应在3-20位之间', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
})

const handleRegister = async () => {
  try {
    await formRef.value.validate()
    
    // 修改这里：直接访问 form 属性而不是 form.value
    console.log('发送的表单数据:', {
      username: form.username,
      password: form.password,
      email: form.email
    })
    
    loading.value = true
    const result = await userStore.register(
      form.username,
      form.password,
      form.email
    )
    
    if (result.success) {
      ElMessage.success('注册成功！即将跳转到登录页面')
      setTimeout(() => {
        router.push('/login')
      }, 1500)
    } else {
      ElMessage.error(result.message || '注册失败')
    }
  } catch (error) {
    if (error.message) {
      console.error('表单验证失败:', error)
    } else {
      console.error('注册失败:', error)
      ElMessage.error('网络连接失败，请稍后重试')
    }
  } finally {
    loading.value = false
  }
}

const goLogin = () => {
  router.push('/login')
}
</script>

<style scoped>
.register-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
  overflow: hidden;
}

.register-box {
  width: 450px;
  padding: 40px;
  border-radius: 20px;
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
  position: relative;
  z-index: 10;
}

.register-box:hover {
  transform: translateY(-5px);
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
}

.register-header {
  text-align: center;
  margin-bottom: 30px;
}

.logo-container {
  margin-bottom: 20px;
}

.logo-icon {
  color: #764ba2;
  background: linear-gradient(135deg, #764ba2, #667eea);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.register-title {
  font-size: 28px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 10px 0;
  background: linear-gradient(135deg, #764ba2, #667eea);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.register-subtitle {
  color: #7f8c8d;
  font-size: 14px;
  margin: 0;
}

.register-form {
  margin-top: 20px;
}

.register-input {
  margin-bottom: 20px;
}

.register-input :deep(.el-input__wrapper) {
  border-radius: 12px;
  padding: 12px 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid #e1e8ed;
  transition: all 0.3s ease;
}

.register-input :deep(.el-input__wrapper:hover) {
  border-color: #764ba2;
  box-shadow: 0 4px 12px rgba(118, 75, 162, 0.15);
}

.register-input :deep(.el-input__wrapper.is-focus) {
  border-color: #764ba2;
  box-shadow: 0 4px 12px rgba(118, 75, 162, 0.2);
}

.register-actions {
  margin-bottom: 20px;
}

.register-btn {
  width: 100%;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
  border: none;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.register-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(118, 75, 162, 0.3);
}

.login-link {
  text-align: center;
  color: #7f8c8d;
  font-size: 14px;
}

.login-btn-link {
  color: #764ba2;
  font-weight: 600;
  padding: 0;
  margin-left: 5px;
}

.login-btn-link:hover {
  color: #667eea;
}

@media (max-width: 480px) {
  .register-box {
    width: 90%;
    padding: 30px 20px;
  }
}
</style>