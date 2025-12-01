import glob
import importlib
import os
from typing import TypeVar
from sqlmodel import Session
from sqlalchemy import create_engine
from sqlmodel import SQLModel, select
import config
from sql.schema.user import User

T = TypeVar("T", bound=SQLModel)


class SQLClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        [单例模式核心]
        每次实例化前，先检查是不是已经创建过实例了。
        如果创建过，直接返回旧的，不再创建新的。
        """
        if cls._instance is None:
            cls._instance = super(SQLClient, cls).__new__(cls)
        return cls._instance

    def __init__(self, schema_dir: str = "./schema"):
        if getattr(self, "_initialized", False):
            return
        db_url = getattr(config, "DATABASE_URL", "sqlite:///market.db")
        # 智能补全 sqlite 前缀
        if "sqlite" not in db_url and "://" not in db_url:
            db_url = f"sqlite:///{db_url}"
        self.engine = create_engine(db_url)
        self.schema_dir = schema_dir

    def _auto_import_schemas(self):
        if not os.path.exists(self.schema_dir):
            print("❌ schema 目录不存在，无法导入模型")
            return
        schema_files = glob.glob(os.path.join(self.schema_dir, "*.py"))
        imported_schemas = 0

        for schema_file in schema_files:
            print(f"导入模型: {schema_file}")
            if "__init__" in schema_file:
                continue
            #  提取模块名
            module_name = os.path.splitext(os.path.basename(schema_file))[0].replace(
                os.sep, "."
            )
            if module_name.startswith("."):
                module_name = module_name[1:]

            # 将文件路径转换为模块路径 (例如 schema.user)
            module_path = f"schema.{module_name}"
            try:
                importlib.import_module(module_path)
                print(f"   -> 已加载模型文件: {module_name}")
                imported_schemas += 1
            except Exception as e:
                print(f"❌ 导入模型 {module_name} 失败: {e}")
        if imported_schemas == 0:
            print("❌ 未导入任何模型，请检查 schema 目录下是否有模型文件")

    def init_db(self):
        # self._auto_import_schemas(User)
        SQLModel.metadata.create_all(self.engine)
        print("构造数据库")

    def get_session(self):
        return Session(self.engine)

    # ---------表的基本操作增删改查模版———————————
    def add(self, item: T) -> T:
        with Session(self.engine) as session:
            session.add(item)
            session.commit()
            session.refresh(item)
            return item

    def get(self, model: T, id: int) -> T:
        with Session(self.engine) as session:
            item = session.get(model, id)
            return item

    def update(self, item: T) -> T:
        with Session(self.engine) as session:
            select_item = session.get(type(item), item.id)
            if select_item is None:
                return None
            # model_dump(exclude_unset=True) 会只提取你显式设置过的字段
            item_data = item.model_dump(exclude_unset=True)

            for key, value in item_data.items():
                setattr(select_item, key, value)
            session.add(select_item)
            session.commit()
            session.refresh(select_item)
            return item

    # order_by_desc 参数传入需要降序排序的字段，如 model.created_at
    def get_list(self, model: T, limit: int | None, order_by_desc=None) -> list[T]:
        with Session(self.engine) as session:
            # 准备查询语句：SELECT * FROM table
            statement = select(model)
            if order_by_desc is not None:
                statement = statement.order_by(order_by_desc.desc())
            # 限制返回条数 (分页的基础)
            statement = statement.limit(limit)
            return session.exec(statement).all()

    def delete(self, item: T):
        with Session(self.engine) as session:
            if session.get(type(item), item.id) is None:
                return False
            session.delete(item)
            session.commit()
            return True

    def exec(self, statement):
        with Session(self.engine) as session:
            results = session.exec(statement).all()
            return results


db = SQLClient(schema_dir="./schema")
