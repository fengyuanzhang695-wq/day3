import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# 获取项目根目录
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# 创建Flask应用实例
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)

# 加载配置
app.config.from_object('app.config.Config')

# 初始化数据库
db = SQLAlchemy(app)

# 初始化迁移工具
migrate = Migrate(app, db)

# 初始化登录管理器
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # 设置登录视图
login_manager.login_message = '请先登录以访问此页面'

# 注册蓝图
from app.admin import admin_bp
app.register_blueprint(admin_bp, url_prefix='/admin')

# 导入路由和模型
from app import routes, models

# 导入装饰器
from app import decorators

# 登录用户加载函数
@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))
