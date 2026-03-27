import pymysql
from loguru import logger

from src.utils.environment import Environment

class MysqlOperate:
    def __init__(self):
        mysql = Environment().get_mysql_config()
        required_fields = ["host", "port", "user", "passwd", "db"]
        missing = [field for field in required_fields if not mysql.get(field)]
        if missing:
            raise ValueError(f"MySQL配置缺失: {missing}")
        try:
            self.conn = pymysql.connect(
                db=mysql['db'],
                host=mysql['host'],
                user=mysql['user'],
                password=mysql['passwd'],
                port=mysql['port'])
        except pymysql.MySQLError as e:
            logger.error(f"数据库连接失败: host={mysql.get('host')}, db={mysql.get('db')}")
            raise e
        else:
            self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def close_connection(self):
        if getattr(self, "cur", None):
            self.cur.close()
        if getattr(self, "conn", None):
            self.conn.close()

    def query_one(self, sql, query_params=None):
        try:
            self.cur.execute(sql, query_params)
        except pymysql.MySQLError as e:
            logger.error(f"MySQL query_one执行失败: sql={sql}, params={query_params}, error={e}")
            raise e
        else:
            return self.cur.fetchone()

    def query_all(self, sql, query_params=None):
        try:
            self.cur.execute(sql, query_params)
        except pymysql.MySQLError as e:
            logger.error(f"MySQL query_all执行失败: sql={sql}, params={query_params}, error={e}")
            raise e
        else:
            return self.cur.fetchall()


    def modify(self, sql, query_params=None):
        try:
            self.cur.execute(sql, query_params)
            self.conn.commit()
        except pymysql.MySQLError as e:
            logger.error(f"MySQL modify执行失败: sql={sql}, params={query_params}, error={e}")
            if self.conn:
                self.conn.rollback()
            raise e

