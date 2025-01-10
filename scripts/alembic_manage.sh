
# 生成迁移文件
alembic revision --autogenerate -m "message"

# 升级
alembic upgrade head

# 降级
alembic downgrade head