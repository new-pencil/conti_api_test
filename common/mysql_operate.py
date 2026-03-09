import pymysql
from loguru import logger

from common.environment import Environment

class MysqlOperate:
    def __init__(self):
        mysql = Environment().get_mysql_config()
        try:
            self.conn = pymysql.connect(
                db=mysql['db'],
                host=mysql['host'],
                user=mysql['user'],
                password=mysql['passwd'],
                port=mysql['port'])
        except Exception as e:
            logger.error(f'数据库连接失败')
            raise e
        else:
            self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)


    def close_connection(self):
        self.cur.close()
        self.conn.close()

    def query_one(self, sql, query_params=None):
        try:
            self.cur.execute(sql, query_params)
        except Exception as e:
            logger.error(e)
        else:
            return self.cur.fetchone()

    def query_all(self, sql, query_params=None):
        try:
            self.cur.execute(sql, query_params)
        except Exception as e:
            logger.error(e)
        else:
            return self.cur.fetchall()


    def modify(self, sql, query_params=None):
        try:
            self.cur.execute(sql, query_params)
            self.conn.commit()
        except Exception as e:
            logger.error(e)
            if self.conn:
                self.conn.rollback()


