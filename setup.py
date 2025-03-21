from setuptools import setup, find_packages

setup(
    name="smart-inv",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.31.0",
        "pandas",
        "tushare",
        "numpy",
        "altair",
        "sqlalchemy",
        "psycopg2-binary",
        "redis",
        "python-jose[cryptography]",
        "passlib[bcrypt]",
        "bcrypt==4.0.1",
        "python-dotenv",
        "alembic",
        "python-multipart",
    ],
) 