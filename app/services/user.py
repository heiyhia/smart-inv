from typing import Optional
from sqlalchemy.orm import Session
from app.database.models import User, UserApproval
from app.auth.manager import get_password_hash, verify_password

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """通过用户名获取用户"""
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """通过邮箱获取用户"""
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, username: str, email: str, password: str, is_admin: bool = False) -> User:
    """创建新用户"""
    hashed_password = get_password_hash(password)
    user = User(
        username=username,
        email=email,
        password_hash=hashed_password,
        is_admin=is_admin,
        is_active=is_admin  # 管理员创建时直接激活
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_user_approval(db: Session, user_id: int) -> UserApproval:
    """创建用户审批记录"""
    approval = UserApproval(
        user_id=user_id,
        status="PENDING"
    )
    db.add(approval)
    db.commit()
    db.refresh(approval)
    return approval

def approve_user(db: Session, approval_id: int, admin_id: int, approved: bool) -> UserApproval:
    """审批用户"""
    approval = db.query(UserApproval).filter(UserApproval.id == approval_id).first()
    if approval:
        approval.status = "APPROVED" if approved else "REJECTED"
        approval.approved_by = admin_id
        if approved:
            user = approval.user
            user.is_active = True
        db.commit()
        db.refresh(approval)
    return approval

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """验证用户"""
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def get_pending_approvals(db: Session):
    """获取待审批的用户列表"""
    return db.query(UserApproval).filter(UserApproval.status == "PENDING").all()

def is_admin(user: User) -> bool:
    """检查用户是否为管理员"""
    return user.is_admin if user else False 