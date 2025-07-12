<template>
<div class="history">
    <div class="header">
    <h1>面试历史</h1>
    <p>查看你的所有面试记录和成绩</p>
    </div>

    <div class="filters">
    <el-select v-model="statusFilter" placeholder="筛选状态" clearable>
        <el-option label="全部" value=""></el-option>
        <el-option label="已完成" value="completed"></el-option>
        <el-option label="进行中" value="in_progress"></el-option>
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

    <div class="interview-list" v-loading="loading">
    <div 
        v-for="interview in filteredInterviews" 
        :key="interview.id"
        class="interview-card"
    >
        <div class="interview-info">
        <h3>{{ interview.position_name }}</h3>
        <div class="interview-meta">
            <span class="date">{{ formatDate(interview.created_at) }}</span>
            <span class="status" :class="interview.status">
            {{ getStatusText(interview.status) }}
            </span>
        </div>
        </div>
        
        <div class="interview-stats" v-if="interview.status === 'completed'">
        <div class="stat">
            <span class="label">得分</span>
            <span class="value">{{ interview.score || 'N/A' }}</span>
        </div>
        <div class="stat">
            <span class="label">用时</span>
            <span class="value">{{ interview.duration || 'N/A' }} 分钟</span>
        </div>
        </div>
        
        <div class="interview-actions">
        <el-button 
            v-if="interview.status === 'in_progress'"
            type="primary"
            @click="continueInterview(interview.id)"
        >
            继续面试
        </el-button>
        <el-button 
            v-if="interview.status === 'completed'"
            @click="viewDetails(interview.id)"
        >
            查看详情
        </el-button>
        <el-button 
            type="danger" 
            @click="deleteInterview(interview.id)"
            :disabled="interview.status === 'in_progress'"
        >
            删除
        </el-button>
        </div>
    </div>
    
    <div v-if="filteredInterviews.length === 0" class="empty-state">
        <p>暂无面试记录</p>
        <el-button type="primary" @click="$router.push('/home')">
        开始第一次面试
        </el-button>
    </div>
    </div>
</div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { api } from '@/utils/api';
import { ElMessage, ElMessageBox } from 'element-plus';

const router = useRouter();

interface Interview {
  id: number;
  position_name: string;
  status: string;
  score: number | null;
  duration: number | null;
  created_at: string;
}

// 修复：明确指定类型
const interviews = ref<Interview[]>([]);
const loading = ref(false);
const statusFilter = ref('');
const dateRange = ref<string[]>([]);

const filteredInterviews = computed(() => {
  let filtered = interviews.value;
  
  if (statusFilter.value) {
    filtered = filtered.filter((interview: Interview) => interview.status === statusFilter.value);
  }
  
  if (dateRange.value && dateRange.value.length === 2) {
    const [startDate, endDate] = dateRange.value;
    filtered = filtered.filter((interview: Interview) => {
      const interviewDate = interview.created_at.split('T')[0];
      return interviewDate >= startDate && interviewDate <= endDate;
    });
  }
  
  return filtered;
});

const fetchInterviews = async () => {
  try {
    loading.value = true;
    const response = await api.getInterviewHistory();
    if (response.code === 200 && response.data) {
      interviews.value = response.data as Interview[];
    }
  } catch (error) {
    ElMessage.error('获取面试历史失败');
  } finally {
    loading.value = false;
  }
};

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

// 修复：明确指定参数和返回类型
const getStatusText = (status: string): string => {
  const statusMap: Record<string, string> = {
    'completed': '已完成',
    'in_progress': '进行中',
    'cancelled': '已取消'
  };
  return statusMap[status] || status;
};

const continueInterview = (interviewId: number) => {
  router.push({
    name: 'Interview',
    params: { interviewId: interviewId.toString() }
  });
};

const viewDetails = (interviewId: number) => {
  ElMessage.info('详情功能开发中...');
};

const deleteInterview = async (interviewId: number) => {
  try {
    const result = await ElMessageBox.confirm(
      '确定要删除这条面试记录吗？此操作不可恢复。',
      '确认删除',
      {
        confirmButtonText: '删除',
        cancelButtonText: '取消',
        type: 'warning',
      }
    );
    
    if (result === 'confirm') {
      const response = await api.deleteInterview(interviewId);
      if (response.code === 200) {
        ElMessage.success('删除成功');
        await fetchInterviews();
      }
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败');
    }
  }
};

onMounted(() => {
  fetchInterviews();
});
</script>

<style scoped>
.history {
max-width: 1200px;
margin: 0 auto;
padding: 20px;
}

.header {
text-align: center;
margin-bottom: 30px;
}

.header h1 {
font-size: 2.5rem;
color: #2c3e50;
margin-bottom: 10px;
}

.header p {
font-size: 1.1rem;
color: #7f8c8d;
}

.filters {
display: flex;
gap: 20px;
margin-bottom: 30px;
padding: 20px;
background: white;
border-radius: 10px;
box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.interview-list {
display: flex;
flex-direction: column;
gap: 20px;
}

.interview-card {
background: white;
padding: 25px;
border-radius: 10px;
box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
display: flex;
justify-content: space-between;
align-items: center;
}

.interview-info h3 {
font-size: 1.3rem;
color: #2c3e50;
margin-bottom: 10px;
}

.interview-meta {
display: flex;
gap: 15px;
align-items: center;
}

.date {
color: #7f8c8d;
font-size: 0.9rem;
}

.status {
padding: 4px 12px;
border-radius: 12px;
font-size: 0.8rem;
font-weight: bold;
}

.status.completed {
background: #d4edda;
color: #155724;
}

.status.in_progress {
background: #fff3cd;
color: #856404;
}

.interview-stats {
display: flex;
gap: 30px;
}

.stat {
text-align: center;
}

.stat .label {
display: block;
font-size: 0.9rem;
color: #7f8c8d;
margin-bottom: 5px;
}

.stat .value {
display: block;
font-size: 1.2rem;
font-weight: bold;
color: #2c3e50;
}

.interview-actions {
display: flex;
gap: 10px;
}

.empty-state {
text-align: center;
padding: 60px 20px;
color: #7f8c8d;
}

.empty-state p {
font-size: 1.1rem;
margin-bottom: 20px;
}
</style>