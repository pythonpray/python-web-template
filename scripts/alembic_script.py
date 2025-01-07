#!/usr/bin/env python3
import os
import sys
import argparse
from alembic import command
from alembic.config import Config

# 获取项目根目录
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)


def get_alembic_config():
    """获取alembic配置"""
    config = Config(os.path.join(ROOT_DIR, "alembic.ini"))
    config.set_main_option("script_location", os.path.join(ROOT_DIR, "alembic"))
    return config


def create_migration(message):
    """创建新的迁移文件"""
    config = get_alembic_config()
    command.revision(config, message=message, autogenerate=True)
    print(f"Created new migration with message: {message}")


def upgrade_db(revision="head"):
    """升级数据库到指定版本"""
    config = get_alembic_config()
    command.upgrade(config, revision)
    print(f"Upgraded database to revision: {revision}")


def downgrade_db(revision="-1"):
    """降级数据库到指定版本"""
    config = get_alembic_config()
    command.downgrade(config, revision)
    print(f"Downgraded database to revision: {revision}")


def show_history():
    """显示迁移历史"""
    config = get_alembic_config()
    command.history(config)


def show_current():
    """显示当前版本"""
    config = get_alembic_config()
    command.current(config)


def main():
    parser = argparse.ArgumentParser(description="Database migration management script")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # create migration
    create_parser = subparsers.add_parser("create", help="Create a new migration")
    create_parser.add_argument("message", help="Migration message")

    # upgrade
    upgrade_parser = subparsers.add_parser("upgrade", help="Upgrade database")
    upgrade_parser.add_argument("--revision", default="head", help="Target revision (default: head)")

    # downgrade
    downgrade_parser = subparsers.add_parser("downgrade", help="Downgrade database")
    downgrade_parser.add_argument("--revision", default="-1", help="Target revision (default: -1)")

    # history
    subparsers.add_parser("history", help="Show migration history")

    # current
    subparsers.add_parser("current", help="Show current revision")

    args = parser.parse_args()

    if args.command == "create":
        create_migration(args.message)
    elif args.command == "upgrade":
        upgrade_db(args.revision)
    elif args.command == "downgrade":
        downgrade_db(args.revision)
    elif args.command == "history":
        show_history()
    elif args.command == "current":
        show_current()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
