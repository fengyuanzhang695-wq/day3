from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, Optional


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=6, max=20)])
    submit = SubmitField('登录')


class UserForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[Optional(), Length(min=6, max=20)])
    role_id = SelectField('角色', coerce=int, validators=[DataRequired()])
    submit = SubmitField('提交')


class RoleForm(FlaskForm):
    name = StringField('角色名称', validators=[DataRequired(), Length(min=2, max=20)])
    description = TextAreaField('角色描述', validators=[Optional()])
    submit = SubmitField('提交')


class SystemSettingsForm(FlaskForm):
    name = StringField('系统名称', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('系统描述', validators=[Optional()])
    logo_url = StringField('LOGO URL', validators=[Optional()])
    submit = SubmitField('保存设置')


class NewsScrapingForm(FlaskForm):
    keyword = StringField('搜索关键字', validators=[DataRequired(), Length(min=1, max=100)])
    rtt = SelectField('排序方式', coerce=int, choices=[(1, '按时间排序'), (2, '按焦点排序')], default=1)
    bsst = SelectField('是否只显示有图新闻', coerce=int, choices=[(1, '仅显示有图新闻'), (0, '显示所有新闻')], default=1)
    rn = SelectField('每页显示数量', coerce=int, choices=[(10, '10条'), (20, '20条'), (50, '50条')], default=10)
    submit = SubmitField('开始抓取')
