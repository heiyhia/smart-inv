import streamlit as st
from app.database.session import SessionLocal
from app.services.user import create_user, create_user_approval, get_user_by_username, get_user_by_email

def register_page():
    st.title("注册")
    
    # 如果已经登录，重定向到主页
    if "user" in st.session_state:
        st.warning("您已登录，请先退出")
        st.query_params.clear()
        st.rerun()
        return

    # 注册表单
    with st.form("register_form"):
        username = st.text_input("用户名", help="长度3-20个字符")
        email = st.text_input("邮箱")
        password = st.text_input("密码", type="password", help="长度至少8个字符")
        password_confirm = st.text_input("确认密码", type="password")
        submitted = st.form_submit_button("注册")

        if submitted:
            # 表单验证
            if not all([username, email, password, password_confirm]):
                st.error("请填写所有字段")
                return
            
            if len(username) < 3 or len(username) > 20:
                st.error("用户名长度必须在3-20个字符之间")
                return
                
            if len(password) < 8:
                st.error("密码长度必须至少8个字符")
                return
                
            if password != password_confirm:
                st.error("两次输入的密码不一致")
                return

            # 创建用户
            db = SessionLocal()
            try:
                # 检查用户名是否已存在
                if get_user_by_username(db, username):
                    st.error("用户名已存在")
                    return
                    
                # 检查邮箱是否已存在
                if get_user_by_email(db, email):
                    st.error("邮箱已被注册")
                    return

                # 创建用户
                user = create_user(db, username, email, password)
                # 创建审批记录
                create_user_approval(db, user.id)

                st.success("注册成功！请等待管理员审批")
                st.info("审批通过后，您将收到邮件通知")
            except Exception as e:
                st.error(f"注册失败：{str(e)}")
            finally:
                db.close()

    # 登录链接
    st.markdown("已有账号？[点击登录](/)")

if __name__ == "__main__":
    register_page() 