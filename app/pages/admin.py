import streamlit as st
from app.database.session import SessionLocal
from app.services.user import get_pending_approvals, approve_user, is_admin

def admin_page():
    st.title("管理员控制台")
    
    # 检查是否登录和是否是管理员
    if "user" not in st.session_state:
        st.error("请先登录")
        st.markdown("[去登录](/)")
        return
        
    if not st.session_state.user.get("is_admin"):
        st.error("无权访问此页面")
        return

    # 获取待审批用户列表
    db = SessionLocal()
    try:
        pending_approvals = get_pending_approvals(db)
        
        if not pending_approvals:
            st.info("没有待审批的用户")
            return
            
        st.subheader("待审批用户列表")
        
        for approval in pending_approvals:
            user = approval.user
            col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
            
            with col1:
                st.write(f"用户名: {user.username}")
            with col2:
                st.write(f"邮箱: {user.email}")
            with col3:
                if st.button("通过", key=f"approve_{approval.id}"):
                    approve_user(db, approval.id, st.session_state.user["id"], True)
                    st.success("已通过")
                    st.rerun()
            with col4:
                if st.button("拒绝", key=f"reject_{approval.id}"):
                    approve_user(db, approval.id, st.session_state.user["id"], False)
                    st.success("已拒绝")
                    st.rerun()
            
            st.markdown("---")
    finally:
        db.close()

if __name__ == "__main__":
    admin_page() 