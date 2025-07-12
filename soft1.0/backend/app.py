from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import json
from datetime import datetime, timedelta
import secrets

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})  # 5173是Vite默认端口

# 数据库配置
db_config = {
    'host': 'localhost',      # 数据库地址
    'user': 'root',           # 数据库用户名
    'password': '123456',     # 数据库密码
    'database': 'interview',  # 数据库名
    'auth_plugin': 'mysql_native_password'
}

# 简单的session存储
user_sessions = {}

def get_db():
    return mysql.connector.connect(**db_config)

def generate_session_token():
    return secrets.token_hex(32)

def get_user_from_session(token):
    if token in user_sessions:
        session_data = user_sessions[token]
        if datetime.now() < session_data['expires']:
            return session_data['user_id']
        else:
            del user_sessions[token]
    return None

# 用户认证相关接口
@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        print(f"接收到的原始数据: {data}")
        
        if not data:
            return jsonify({'code': 400, 'msg': '请求数据为空'}), 400
        
        # 处理可能的数组格式
        username = data.get('username')
        if isinstance(username, list):
            username = username[0] if username else ''
        
        password = data.get('password')
        if isinstance(password, list):
            password = password[0] if password else ''
        
        email = data.get('email')
        if isinstance(email, list):
            email = email[0] if email else ''
        
        print(f"解析后的字段: username={username}, password={password}, email={email}")
        
        if not username or not password or not email:
            return jsonify({'code': 400, 'msg': '用户名、密码和邮箱不能为空'}), 400
        
        hashed_password = generate_password_hash(password)
        
        try:
            conn = get_db()
            cursor = conn.cursor()
            # 修改表名为 users
            cursor.execute('INSERT INTO users (username, password, email) VALUES (%s, %s, %s)',
                        (username, hashed_password, email))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'code': 200, 'msg': '注册成功'})
        except mysql.connector.IntegrityError:
            cursor.close()
            conn.close()
            return jsonify({'code': 409, 'msg': '用户名已存在'}), 409
            
    except Exception as e:
        print(f"注册错误: {str(e)}")
        return jsonify({'code': 500, 'msg': f'注册失败: {str(e)}'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'code': 400, 'msg': '用户名和密码不能为空'}), 400
        
        conn = get_db()
        cursor = conn.cursor()
        # 修改表名为 users
        cursor.execute('SELECT id, password, username FROM users WHERE username=%s', (username,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if result and check_password_hash(result[1], password):
            # 生成session token
            token = generate_session_token()
            user_sessions[token] = {
                'user_id': result[0],
                'expires': datetime.now() + timedelta(hours=24)
            }
            
            return jsonify({
                'code': 200, 
                'msg': '登录成功',
                'data': {
                    'token': token,
                    'user': {
                        'id': result[0],
                        'username': result[2]
                    }
                }
            })
        else:
            return jsonify({'code': 401, 'msg': '用户名或密码错误'}), 401
    except Exception as e:
        print(f"登录错误: {str(e)}")
        return jsonify({'code': 500, 'msg': f'登录失败: {str(e)}'}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    token = request.headers.get('Authorization')
    if token and token in user_sessions:
        del user_sessions[token]
    return jsonify({'code': 200, 'msg': '退出成功'})

# 用户信息相关接口
@app.route('/api/user/profile', methods=['GET'])
def get_user_profile():
    token = request.headers.get('Authorization')
    user_id = get_user_from_session(token)
    
    if not user_id:
        return jsonify({'code': 401, 'msg': '请先登录'}), 401
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT username, real_name, email, phone, major, grade, avatar_url, created_at
        FROM users WHERE id = %s
    ''', (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if result:
        return jsonify({
            'code': 200,
            'data': {
                'username': result[0],
                'realName': result[1],
                'email': result[2],
                'phone': result[3],
                'major': result[4],
                'grade': result[5],
                'avatarUrl': result[6],
                'createdAt': result[7].isoformat() if result[7] else None
            }
        })
    else:
        return jsonify({'code': 404, 'msg': '用户不存在'}), 404

@app.route('/api/user/stats', methods=['GET'])
def get_user_stats():
    token = request.headers.get('Authorization')
    user_id = get_user_from_session(token)
    
    if not user_id:
        return jsonify({'code': 401, 'msg': '请先登录'}), 401
    
    conn = get_db()
    cursor = conn.cursor()
    
    # 获取总面试次数
    cursor.execute('SELECT COUNT(*) FROM interview_records WHERE user_id = %s AND status = "已完成"', (user_id,))
    total_interviews = cursor.fetchone()[0]
    
    # 获取平均得分
    cursor.execute('SELECT AVG(score) FROM interview_records WHERE user_id = %s AND status = "已完成"', (user_id,))
    avg_score_result = cursor.fetchone()[0]
    avg_score = int(avg_score_result) if avg_score_result else 0
    
    # 获取总用时
    cursor.execute('SELECT SUM(duration_minutes) FROM interview_records WHERE user_id = %s AND status = "已完成"', (user_id,))
    total_time_result = cursor.fetchone()[0]
    total_time = round(total_time_result / 60, 1) if total_time_result else 0
    
    # 获取最高得分
    cursor.execute('SELECT MAX(score) FROM interview_records WHERE user_id = %s AND status = "已完成"', (user_id,))
    best_score_result = cursor.fetchone()[0]
    best_score = best_score_result if best_score_result else 0
    
    # 获取已练习岗位数
    cursor.execute('SELECT COUNT(DISTINCT job_position_id) FROM interview_records WHERE user_id = %s AND status = "已完成"', (user_id,))
    completed_jobs = cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
    
    return jsonify({
        'code': 200,
        'data': {
            'totalInterviews': total_interviews,
            'avgScore': avg_score,
            'totalTime': total_time,
            'bestScore': best_score,
            'completedJobs': completed_jobs
        }
    })

# 岗位相关接口
@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, description, difficulty, duration, icon FROM job_positions WHERE is_active = TRUE')
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    jobs = []
    for result in results:
        jobs.append({
            'id': result[0],
            'name': result[1],
            'description': result[2],
            'difficulty': result[3],
            'duration': f'{result[4]}分钟',
            'icon': result[5]
        })
    
    return jsonify({'code': 200, 'data': jobs})

@app.route('/api/jobs/<int:job_id>/questions', methods=['GET'])
def get_job_questions(job_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, type, title, description, difficulty, hint, code_template, tags
        FROM questions WHERE job_position_id = %s AND is_active = TRUE
        ORDER BY RAND() LIMIT 5
    ''', (job_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    questions = []
    for result in results:
        questions.append({
            'id': result[0],
            'type': result[1],
            'title': result[2],
            'description': result[3],
            'difficulty': result[4],
            'hint': result[5],
            'codeTemplate': result[6],
            'tags': json.loads(result[7]) if result[7] else []
        })
    
    return jsonify({'code': 200, 'data': questions})

# 面试相关接口
@app.route('/api/interview/start', methods=['POST'])
def start_interview():
    token = request.headers.get('Authorization')
    user_id = get_user_from_session(token)
    
    if not user_id:
        return jsonify({'code': 401, 'msg': '请先登录'}), 401
    
    data = request.get_json()
    job_position_id = data.get('jobPositionId')
    
    if not job_position_id:
        return jsonify({'code': 400, 'msg': '岗位ID不能为空'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    # 创建面试记录
    cursor.execute('''
        INSERT INTO interview_records (user_id, job_position_id, status)
        VALUES (%s, %s, "进行中")
    ''', (user_id, job_position_id))
    interview_id = cursor.lastrowid
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({
        'code': 200,
        'data': {
            'interviewId': interview_id
        }
    })

@app.route('/api/interview/<int:interview_id>/answer', methods=['POST'])
def save_answer(interview_id):
    token = request.headers.get('Authorization')
    user_id = get_user_from_session(token)
    
    if not user_id:
        return jsonify({'code': 401, 'msg': '请先登录'}), 401
    
    data = request.get_json()
    question_id = data.get('questionId')
    question_order = data.get('questionOrder')
    answer_text = data.get('answerText', '')
    answer_code = data.get('answerCode', '')
    programming_language = data.get('programmingLanguage', '')
    time_spent = data.get('timeSpent', 0)
    is_skipped = data.get('isSkipped', False)
    
    conn = get_db()
    cursor = conn.cursor()
    
    # 检查面试记录是否属于当前用户
    cursor.execute('SELECT user_id FROM interview_records WHERE id = %s', (interview_id,))
    result = cursor.fetchone()
    
    if not result or result[0] != user_id:
        cursor.close()
        conn.close()
        return jsonify({'code': 403, 'msg': '无权限操作此面试记录'}), 403
    
    # 保存答题记录
    cursor.execute('''
        INSERT INTO interview_question_records 
        (interview_record_id, question_id, question_order, answer_text, answer_code, 
        programming_language, time_spent, is_skipped)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        answer_text = VALUES(answer_text),
        answer_code = VALUES(answer_code),
        programming_language = VALUES(programming_language),
        time_spent = VALUES(time_spent),
        is_skipped = VALUES(is_skipped)
    ''', (interview_id, question_id, question_order, answer_text, answer_code, 
        programming_language, time_spent, is_skipped))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({'code': 200, 'msg': '答案保存成功'})

@app.route('/api/interview/<int:interview_id>/finish', methods=['POST'])
def finish_interview(interview_id):
    token = request.headers.get('Authorization')
    user_id = get_user_from_session(token)
    
    if not user_id:
        return jsonify({'code': 401, 'msg': '请先登录'}), 401
    
    data = request.get_json()
    duration_minutes = data.get('durationMinutes', 0)
    
    conn = get_db()
    cursor = conn.cursor()
    
    # 检查面试记录是否属于当前用户
    cursor.execute('SELECT user_id FROM interview_records WHERE id = %s', (interview_id,))
    result = cursor.fetchone()
    
    if not result or result[0] != user_id:
        cursor.close()
        conn.close()
        return jsonify({'code': 403, 'msg': '无权限操作此面试记录'}), 403
    
    # 计算总分（简单的评分逻辑，可以后续优化）
    cursor.execute('''
        SELECT COUNT(*) as total, 
            SUM(CASE WHEN is_skipped = FALSE THEN 1 ELSE 0 END) as answered
        FROM interview_question_records 
        WHERE interview_record_id = %s
    ''', (interview_id,))
    score_result = cursor.fetchone()
    
    total_questions = score_result[0] if score_result[0] else 1
    answered_questions = score_result[1] if score_result[1] else 0
    score = int((answered_questions / total_questions) * 100)
    
    # 更新面试记录
    cursor.execute('''
        UPDATE interview_records 
        SET status = "已完成", score = %s, duration_minutes = %s, end_time = NOW(),
            summary = "面试已完成，共回答了%s道题目中的%s道"
        WHERE id = %s
    ''', (score, duration_minutes, total_questions, answered_questions, interview_id))
    
    # 添加技能评估（示例数据）
    skills = [
        {'name': '技术基础', 'score': min(score + 5, 100)},
        {'name': '逻辑思维', 'score': max(score - 5, 0)},
        {'name': '表达能力', 'score': score},
        {'name': '项目经验', 'score': max(score - 10, 0)}
    ]
    
    for skill in skills:
        cursor.execute('''
            INSERT INTO skill_assessments (interview_record_id, skill_name, score)
            VALUES (%s, %s, %s)
        ''', (interview_id, skill['name'], skill['score']))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({
        'code': 200,
        'msg': '面试完成',
        'data': {
            'score': score,
            'skills': skills
        }
    })

# 面试记录相关接口
@app.route('/api/interview/history', methods=['GET'])
def get_interview_history():
    token = request.headers.get('Authorization')
    user_id = get_user_from_session(token)
    
    if not user_id:
        return jsonify({'code': 401, 'msg': '请先登录'}), 401
    
    # 获取查询参数
    job_type = request.args.get('jobType', '')
    score_range = request.args.get('scoreRange', '')
    start_date = request.args.get('startDate', '')
    end_date = request.args.get('endDate', '')
    keyword = request.args.get('keyword', '')
    
    conn = get_db()
    cursor = conn.cursor()
    
    # 构建查询条件
    where_conditions = ['ir.user_id = %s', 'ir.status = "已完成"']
    params = [user_id]
    
    if job_type:
        where_conditions.append('jp.name LIKE %s')
        params.append(f'%{job_type}%')
    
    if score_range:
        if '-' in score_range:
            min_score, max_score = score_range.split('-')
            where_conditions.append('ir.score BETWEEN %s AND %s')
            params.extend([int(min_score), int(max_score)])
    
    if start_date:
        where_conditions.append('DATE(ir.created_at) >= %s')
        params.append(start_date)
    
    if end_date:
        where_conditions.append('DATE(ir.created_at) <= %s')
        params.append(end_date)
    
    if keyword:
        where_conditions.append('(jp.name LIKE %s OR ir.summary LIKE %s)')
        params.extend([f'%{keyword}%', f'%{keyword}%'])
    
    where_clause = ' AND '.join(where_conditions)
    
    # 查询面试记录
    cursor.execute(f'''
        SELECT ir.id, jp.name as job_name, ir.score, ir.duration_minutes,
            ir.created_at, ir.summary, jp.difficulty,
            (SELECT COUNT(*) FROM interview_question_records iqr WHERE iqr.interview_record_id = ir.id) as question_count
        FROM interview_records ir
        JOIN job_positions jp ON ir.job_position_id = jp.id
        WHERE {where_clause}
        ORDER BY ir.created_at DESC
    ''', params)
    
    records = []
    for result in cursor.fetchall():
        record_id = result[0]
        
        # 获取技能评估
        cursor.execute('''
            SELECT skill_name, score FROM skill_assessments 
            WHERE interview_record_id = %s
        ''', (record_id,))
        skills = [{'name': skill[0], 'score': skill[1]} for skill in cursor.fetchall()]
        
        records.append({
            'id': record_id,
            'jobName': result[1],
            'jobType': result[1].replace('工程师', '').replace('师', ''),
            'score': result[2],
            'duration': f'{result[3]}分钟' if result[3] else '未知',
            'date': result[4].strftime('%Y-%m-%d'),
            'summary': result[5] or '暂无总结',
            'difficulty': result[6],
            'questionCount': result[7],
            'skills': skills
        })
    
    cursor.close()
    conn.close()
    
    return jsonify({'code': 200, 'data': records})

@app.route('/api/interview/<int:record_id>', methods=['DELETE'])
def delete_interview_record(record_id):
    token = request.headers.get('Authorization')
    user_id = get_user_from_session(token)
    
    if not user_id:
        return jsonify({'code': 401, 'msg': '请先登录'}), 401
    
    conn = get_db()
    cursor = conn.cursor()
    
    # 检查记录是否属于当前用户
    cursor.execute('SELECT user_id FROM interview_records WHERE id = %s', (record_id,))
    result = cursor.fetchone()
    
    if not result or result[0] != user_id:
        cursor.close()
        conn.close()
        return jsonify({'code': 403, 'msg': '无权限删除此记录'}), 403
    
    # 删除记录（级联删除相关数据）
    cursor.execute('DELETE FROM interview_records WHERE id = %s', (record_id,))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({'code': 200, 'msg': '删除成功'})

@app.route('/')
def hello():
    return "Flask后端运行成功！"


if __name__ == '__main__':
    app.run(debug=True)

