from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.models import User
from app.forms import LoginForm

# 登录路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    # 如果用户已经登录，重定向到后台管理仪表盘
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # 根据用户名查找用户
        user = User.query.filter_by(username=form.username.data).first()
        
        # 检查用户是否存在且密码正确
        if user is None or not user.check_password(form.password.data):
            flash('用户名或密码错误')
            return redirect(url_for('login'))
        
        # 登录用户
        login_user(user)
        
        # 获取用户想要访问的页面（如果有）
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('admin.dashboard')
            
        return redirect(next_page)
    
    return render_template('login.html', form=form)

# 退出路由
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# 首页路由
@app.route('/')
@login_required
def index():
    return redirect(url_for('admin.dashboard'))

# 测试路由
@app.route('/test')
def test():
    return "Hello, Flask is working!"
