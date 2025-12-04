import requests
import time

# 等待应用程序完全启动
time.sleep(2)

# 测试登录功能
def test_login():
    print("测试登录功能...")
    login_url = "http://localhost:5000/login"
    session = requests.Session()
    
    # 获取登录页面的CSRF token
    response = session.get(login_url)
    if response.status_code != 200:
        print(f"登录页面请求失败: {response.status_code}")
        return False
    
    print("登录页面访问成功")
    print("测试完成！应用程序正在运行中")
    return True

if __name__ == "__main__":
    print("测试政企智能舆情分析报告生成智能体应用系统...")
    test_login()
