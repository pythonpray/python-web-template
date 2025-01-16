import importlib
from pathlib import Path

# 获取当前目录
current_dir = Path(__file__).parent

# 自动导入所有模型文件  alembic自动生成 需要知道哪些model
for file in current_dir.glob("*.py"):
    if file.stem != "__init__":
        module_name = f"infra.models.{file.stem}"
        try:
            importlib.import_module(module_name)
        except Exception as e:
            print(f"Error importing {module_name}: {e}")
