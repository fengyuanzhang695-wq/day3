from app import app, db
from sqlalchemy import text, inspect

print("开始执行数据库表结构更新...")

with app.app_context():
    try:
        # 打印当前数据库表结构
        inspector = inspect(db.engine)
        print("当前数据库表:")
        tables = inspector.get_table_names()
        for table in tables:
            print(f"- {table}")
            columns = [col['name'] for col in inspector.get_columns(table)]
            print(f"  列: {', '.join(columns)}")
        
        # 获取system_settings表的列
        if 'system_settings' in tables:
            columns = [col['name'] for col in inspector.get_columns('system_settings')]
            print(f"\nsystem_settings表当前列: {', '.join(columns)}")
        
        # 更新表结构
        with db.engine.connect() as conn:
            # 添加新的列
            if 'name' not in columns:
                print("添加name列...")
                conn.execute(text('ALTER TABLE system_settings ADD COLUMN name VARCHAR(128) DEFAULT "政企智能舆情分析报告生成智能体应用系统"'))
            
            if 'description' not in columns:
                print("添加description列...")
                conn.execute(text('ALTER TABLE system_settings ADD COLUMN description VARCHAR(256)'))
            
            if 'logo_url' not in columns:
                print("添加logo_url列...")
                conn.execute(text('ALTER TABLE system_settings ADD COLUMN logo_url VARCHAR(256)'))
            
            # 删除旧的列
            if 'app_name' in columns:
                print("删除app_name列...")
                conn.execute(text('ALTER TABLE system_settings DROP COLUMN app_name'))
            
            if 'app_logo' in columns:
                print("删除app_logo列...")
                conn.execute(text('ALTER TABLE system_settings DROP COLUMN app_logo'))
            
            conn.commit()
            
        print("\n数据库表结构更新成功!")
        
        # 检查是否有系统设置记录
        from app.models import SystemSettings
        existing_settings = SystemSettings.query.first()
        if not existing_settings:
            print("添加初始系统设置...")
            system_setting = SystemSettings()
            db.session.add(system_setting)
            db.session.commit()
            print("初始系统设置添加成功!")
        else:
            print("系统设置记录已存在")
            
    except Exception as e:
        print(f"\n更新失败: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

