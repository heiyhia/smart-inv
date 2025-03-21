import streamlit as st
from app.database.session import SessionLocal
from app.database.init_db import init_db
from app.pages.login import login_page
from app.pages.register import register_page
from app.pages.admin import admin_page
from app.pages.home import home_page
from app.auth.middleware import check_auth

# 设置页面配置
st.set_page_config(
    page_title="数据分析系统",
    page_icon="📈",
    layout="wide"
)

# 初始化数据库
db = SessionLocal()
try:
    init_db(db)
finally:
    db.close()

# 页面路由
def main():
    # 获取当前页面
    query_params = st.experimental_get_query_params()
    page = query_params.get("page", [""])[0]

    # 检查认证状态
    is_authenticated = check_auth()
    
    # 路由到相应的页面
    if page == "register" and not is_authenticated:
        register_page()
    elif page == "admin" and is_authenticated:
        admin_page()
    elif is_authenticated:
        home_page()  # 已登录用户默认显示主页
    else:
        login_page()  # 未登录用户显示登录页面

if __name__ == "__main__":
    main() 