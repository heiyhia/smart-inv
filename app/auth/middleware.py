import streamlit as st
from functools import wraps
from app.redis.client import get_redis
from app.database.session import SessionLocal
from app.services.user import get_user_by_username

def restore_session():
    """从 Redis 恢复会话状态"""
    # 如果已经有会话状态，直接返回
    if "user" in st.session_state and "token" in st.session_state:
        return True

    # 尝试从查询参数获取 token
    query_params = st.experimental_get_query_params()
    token = query_params.get("token", [None])[0]
    if not token:
        return False

    # 验证 token 是否有效
    redis_client = get_redis()
    username = redis_client.get(f"token:{token}")
    
    if username:
        # 验证用户是否仍然有效
        db = SessionLocal()
        try:
            user = get_user_by_username(db, username.decode())
            if user and user.is_active:
                # 恢复会话状态
                st.session_state.user = {
                    "id": user.id,
                    "username": user.username,
                    "is_admin": user.is_admin
                }
                st.session_state.token = token
                return True
        finally:
            db.close()
    
    # 清除无效的 token
    st.experimental_set_query_params()
    return False

def check_auth():
    """检查用户认证状态"""
    # 尝试恢复会话
    if restore_session():
        return True

    # 清除无效的会话状态
    for key in ["user", "token"]:
        if key in st.session_state:
            del st.session_state[key]
    return False

def require_auth(func):
    """验证用户是否登录的装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not check_auth():
            st.error("请先登录")
            st.experimental_set_query_params()  # 清除查询参数，返回登录页
            st.rerun()
            return
        return func(*args, **kwargs)
    return wrapper 