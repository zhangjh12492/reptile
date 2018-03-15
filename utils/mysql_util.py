import pymysql
from utils.configure_read import read_property
from common.constants import ENV
from utils.PyLog import logger
from DBUtils.PersistentDB import PersistentDB
import pymysql

def get_property(attr_name):
    return read_property(ENV.MYSQL_FILE_TYPE, ENV.MYSQL_CONF_TYPE, attr_name)


def get_conn():
    # 打开数据库链接
    try:
        db = pymysql.connect(get_property('host'),
                             get_property('user'),
                             get_property('password'),
                             get_property('database'),
                             int(get_property('port')),
                             charset=ENV.MYSQL_CHARSET)
        return db
    except Exception as e:
        logger.error("--> get db failed, " + str(e))
        return None


get_conn()
