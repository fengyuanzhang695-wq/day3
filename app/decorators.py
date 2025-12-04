from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

# 登录检查装饰器
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('请先登录以访问此页面', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# 管理员角色检查装饰器
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('请先登录以访问此页面', 'warning')
            return redirect(url_for('login'))
        if current_user.role.name != '管理员':
            flash('您没有权限访问该页面', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# 角色权限检查装饰器
def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('请先登录以访问此页面', 'warning')
                return redirect(url_for('login'))
            if current_user.role.name != required_role:
                flash('您没有权限访问该页面', 'error')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# 多角色权限检查装饰器
def roles_required(required_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('请先登录以访问此页面', 'warning')
                return redirect(url_for('login'))
            if current_user.role.name not in required_roles:
                flash('您没有权限访问该页面', 'error')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
