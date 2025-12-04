from datetime import datetime
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import User, Role, SystemSettings
from app.admin import admin_bp
from app.forms import UserForm, RoleForm, SystemSettingsForm, NewsScrapingForm
from app.scraper import BaiduNewsScraper

# 从装饰器模块导入权限控制装饰器
from app.decorators import admin_required

# 仪表盘路由
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    # 获取用户统计信息
    user_count = User.query.count()
    admin_count = User.query.join(Role).filter(Role.name == '管理员').count()
    normal_user_count = User.query.join(Role).filter(Role.name == '普通用户').count()
    
    # 获取系统信息
    system_settings = SystemSettings.query.first()
    system_name = system_settings.name if system_settings else '政企智能舆情分析报告生成智能体应用系统'
    
    current_time = datetime.now()
    
    return render_template('admin/dashboard.html', 
                          user_count=user_count, 
                          admin_count=admin_count, 
                          normal_user_count=normal_user_count, 
                          system_name=system_name, 
                          current_time=current_time)

# 用户列表路由
@admin_bp.route('/users')
@admin_required
def user_list():
    users = User.query.all()
    return render_template('admin/user_list.html', users=users)

# 用户添加路由
@admin_bp.route('/user/add', methods=['GET', 'POST'])
@admin_required
def user_add():
    form = UserForm()
    form.role_id.choices = [(role.id, role.name) for role in Role.query.all()]
    
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            role_id=form.role_id.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('用户添加成功', 'success')
        return redirect(url_for('admin.user_list'))
    
    return render_template('admin/user_form.html', form=form, title='添加用户')

# 用户编辑路由
@admin_bp.route('/user/edit/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def user_edit(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    form.role_id.choices = [(role.id, role.name) for role in Role.query.all()]
    
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.role_id = form.role_id.data
        
        if form.password.data:
            user.set_password(form.password.data)
        
        db.session.commit()
        
        flash('用户更新成功', 'success')
        return redirect(url_for('admin.user_list'))
    
    return render_template('admin/user_form.html', form=form, title='编辑用户', user=user)

# 用户删除路由
@admin_bp.route('/user/delete/<int:user_id>', methods=['POST'])
@admin_required
def user_delete(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('不能删除当前登录用户', 'error')
        return redirect(url_for('admin.user_list'))
    
    db.session.delete(user)
    db.session.commit()
    
    flash('用户删除成功', 'success')
    return redirect(url_for('admin.user_list'))

# 角色列表路由
@admin_bp.route('/roles')
@admin_required
def role_list():
    roles = Role.query.all()
    return render_template('admin/role_list.html', roles=roles)

# 角色添加路由
@admin_bp.route('/role/add', methods=['GET', 'POST'])
@admin_required
def role_add():
    form = RoleForm()
    
    if form.validate_on_submit():
        role = Role(
            name=form.name.data,
            description=form.description.data
        )
        
        db.session.add(role)
        db.session.commit()
        
        flash('角色添加成功', 'success')
        return redirect(url_for('admin.role_list'))
    
    return render_template('admin/role_form.html', form=form, title='添加角色')

# 角色编辑路由
@admin_bp.route('/role/edit/<int:role_id>', methods=['GET', 'POST'])
@admin_required
def role_edit(role_id):
    role = Role.query.get_or_404(role_id)
    form = RoleForm(obj=role)
    
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        
        db.session.commit()
        
        flash('角色更新成功', 'success')
        return redirect(url_for('admin.role_list'))
    
    return render_template('admin/role_form.html', form=form, title='编辑角色', role=role)

# 角色删除路由
@admin_bp.route('/role/delete/<int:role_id>', methods=['POST'])
@admin_required
def role_delete(role_id):
    role = Role.query.get_or_404(role_id)
    
    # 检查是否有用户使用该角色
    user_count = User.query.filter_by(role_id=role_id).count()
    if user_count > 0:
        flash(f'该角色正在被{user_count}个用户使用，不能删除', 'error')
        return redirect(url_for('admin.role_list'))
    
    db.session.delete(role)
    db.session.commit()
    
    flash('角色删除成功', 'success')
    return redirect(url_for('admin.role_list'))

# 系统设置路由
@admin_bp.route('/settings', methods=['GET', 'POST'])
@admin_required
def system_settings():
    from datetime import datetime
    
    system_settings = SystemSettings.query.first()
    
    if not system_settings:
        system_settings = SystemSettings(
            name='政企智能舆情分析报告生成智能体应用系统',
            description='用于生成政企智能舆情分析报告的系统'
        )
        db.session.add(system_settings)
        db.session.commit()
    
    form = SystemSettingsForm(obj=system_settings)
    
    if form.validate_on_submit():
        system_settings.name = form.name.data
        system_settings.description = form.description.data
        system_settings.logo_url = form.logo_url.data
        
        db.session.commit()
        
        flash('系统设置更新成功', 'success')
        return redirect(url_for('admin.system_settings'))
    
    current_time = datetime.now()
    
    return render_template('admin/system_settings.html', form=form, title='系统设置', current_time=current_time)

# 数据抓取路由
@admin_bp.route('/scrape', methods=['GET', 'POST'])
@login_required
def scrape_news():
    form = NewsScrapingForm()
    news_list = []
    
    if form.validate_on_submit():
        try:
            # 创建百度新闻抓取器实例
            scraper = BaiduNewsScraper()
            
            # 抓取新闻数据
            news_list = scraper.fetch_news(
                keyword=form.keyword.data,
                rtt=form.rtt.data,
                bsst=form.bsst.data,
                rn=form.rn.data
            )
            
            if news_list:
                flash(f'成功抓取到 {len(news_list)} 条新闻', 'success')
            else:
                flash('没有抓取到新闻，请尝试其他关键字', 'warning')
                
        except Exception as e:
            flash(f'抓取新闻时出错: {str(e)}', 'error')
    
    return render_template('admin/scrape.html', form=form, news_list=news_list, title='数据抓取')
