import streamlit as st
from datetime import datetime, timedelta
from app.database.session import SessionLocal
from app.services.user import authenticate_user
from app.auth.manager import create_access_token
from app.redis.client import get_redis

def logout():
    """退出登录"""
    redis_client = get_redis()
    if "token" in st.session_state:
        redis_client.delete(f"token:{st.session_state.token}")
    # 清除会话状态
    for key in ["user", "token"]:
        if key in st.session_state:
            del st.session_state[key]
    # 清除查询参数
    st.query_params.clear()
    st.rerun()

def login_page():
    st.title("登录")
    
    # 如果已经登录，重定向到主页
    if "user" in st.session_state:
        st.query_params["token"] = st.session_state.token  # 保持 token 在 URL 中
        st.rerun()
        return

    # 登录表单
    with st.form("login_form"):
        username = st.text_input("用户名")
        password = st.text_input("密码", type="password")
        remember_me = st.checkbox("记住我", value=True)
        submitted = st.form_submit_button("登录")

        if submitted:
            if not username or not password:
                st.error("请输入用户名和密码")
                return

            # 验证用户
            db = SessionLocal()
            try:
                user = authenticate_user(db, username, password)
                if user is None:
                    st.error("用户名或密码错误")
                    return
                if not user.is_active:
                    st.error("账号未激活，请等待管理员审批")
                    return

                # 创建访问令牌
                token = create_access_token({"sub": user.username})
                
                # 存储令牌到 Redis
                redis_client = get_redis()
                redis_client.setex(
                    f"token:{token}",
                    7 * 24 * 3600 if remember_me else 24 * 3600,  # 根据"记住我"选项设置过期时间
                    user.username
                )

                # 保存用户信息到会话状态
                st.session_state.user = {
                    "id": user.id,
                    "username": user.username,
                    "is_admin": user.is_admin
                }
                st.session_state.token = token

                st.success("登录成功！")
                # 重定向到主页，并保持 token 在 URL 中
                st.query_params["token"] = token
                st.rerun()
            finally:
                db.close()

    # 注册链接
    st.markdown("还没有账号？[点击注册](/?page=register)")

if __name__ == "__main__":
    login_page() 