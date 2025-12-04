import os

class Config:
    # 密钥设置，用于会话管理和表单验证
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    
    # SQLite数据库配置
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, '..', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 禁用SQLAlchemy的事件系统，提高性能
    
    # 静态文件和模板文件配置
    STATIC_FOLDER = os.path.join(BASE_DIR, '..', 'static')
    TEMPLATE_FOLDER = os.path.join(BASE_DIR, '..', 'templates')
