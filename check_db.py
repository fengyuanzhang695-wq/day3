from app import app, db

with app.app_context():
    # 打印所有表名（使用新方法）
    print("数据库中的表:")
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    for table in tables:
        print(f"- {table}")
    
    # 尝试创建表（如果不存在）
    print("\n尝试创建表...")
    db.create_all()
    
    # 再次打印所有表名
    print("\n创建表后的表列表:")
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    for table in tables:
        print(f"- {table}")
    
    # 添加初始角色数据
    from app.models import Role
    
    # 检查是否已有角色
    existing_roles = Role.query.all()
    if not existing_roles:
        print("\n添加初始角色...")
        # 创建管理员角色
        admin_role = Role(name='管理员', description='拥有所有功能的权限')
        db.session.add(admin_role)
        
        # 创建普通用户角色
        user_role = Role(name='普通用户', description='登录后可以看到数据报表和最新的报告')
        db.session.add(user_role)
        
        db.session.commit()
        print("初始角色添加成功!")
    
    # 添加初始系统设置
    from app.models import SystemSettings
    
    # 检查是否已有系统设置
    existing_settings = SystemSettings.query.first()
    if not existing_settings:
        print("\n添加初始系统设置...")
        system_setting = SystemSettings()
        db.session.add(system_setting)
        db.session.commit()
        print("初始系统设置添加成功!")
    
    # 添加初始管理员用户
    from app.models import User
    
    # 检查是否已有用户
    existing_users = User.query.all()
    if not existing_users:
        print("\n添加初始管理员用户...")
        admin_user = User(username='admin', email='admin@example.com', role_id=1)
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        db.session.commit()
        print("初始管理员用户添加成功!")
        print("用户名: admin, 密码: admin123")
