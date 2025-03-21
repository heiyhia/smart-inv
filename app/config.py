import os
from datetime import timedelta
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库配置
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/smart_inv")

# Redis配置
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# JWT配置
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-for-development")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_ACCESS_TOKEN_EXPIRE = timedelta(hours=24)

# Tushare配置
TUSHARE_TOKEN = os.getenv("TUSHARE_TOKEN")

# 系统配置
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"  # 仅用于初始化，实际应该使用环境变量
ADMIN_EMAIL = "admin@example.com"

# 密码哈希配置
PWD_CONTEXT_SCHEMES = ["bcrypt"]
PWD_CONTEXT_DEPRECATED = "auto" 