import streamlit as st
from app.auth.middleware import require_auth
from app.pages.stock_analysis import stock_analysis_page
from app.pages.login import logout

@require_auth
def home_page():
    st.title("数据分析系统")
    
    # 显示用户信息
    st.sidebar.success(f"当前用户：{st.session_state.user['username']}")
    
    # 确保 token 在 URL 中
    current_token = st.session_state.get("token")
    if current_token:
        if st.query_params.get("token") != current_token:
            st.query_params["token"] = current_token
            st.rerun()
    
    # 功能导航
    menu = st.sidebar.selectbox(
        "功能选择",
        ["股票数据分析", "其他功能1", "其他功能2"],
        index=0
    )
    
    # 根据选择显示不同的功能页面
    if menu == "股票数据分析":
        stock_analysis_page()
    elif menu == "其他功能1":
        st.write("功能开发中...")
    elif menu == "其他功能2":
        st.write("功能开发中...")
    
    # 退出登录按钮
    if st.sidebar.button("退出登录"):
        logout()

if __name__ == "__main__":
    home_page() 