from utils.mysql_dbutils import MyPymysqlPool
from common.constants import ENV
from utils.PyLog import logger
from model.news import NewsTag, TagPO
from utils.convert_obj_util import class_to_dict


def insert(tagPo):
    mysql = MyPymysqlPool(ENV.MYSQL_CONF_TYPE)
    insert_sql = "insert into lp_tag(`name`, href) " \
                 "values('%s','%s')" % (str(tagPo.name), str(tagPo.href))
    try:
        result = mysql.insert(sql=insert_sql)
        tagPo.id = mysql.getInsertId()
        logger.info("--> insert news result : " + str(result))
        return result
    except Exception as err:
        logger.error(
            "--> insert news error, sql :{}, param :{}, \nerr :{}".format(insert_sql, class_to_dict(tagPo), str(err)))
    finally:
        mysql.dispose()
    return 0


def get_one(tagPo):
    try:
        mysql = MyPymysqlPool(ENV.MYSQL_CONF_TYPE)
        select_sql = "select id,`name`,href  from lp_tag "
        where_sql = "where "
        where_start_sql = ""
        if tagPo.id:
            where_start_sql += " and id=%d" % tagPo.id
        if tagPo.href:
            where_start_sql += " and href='%s'" % tagPo.href
        if where_start_sql and where_start_sql.__len__() > 0:
            where_start_sql = where_start_sql[4:]
            select_sql = select_sql + "where " + where_start_sql
        result = mysql.getOne(sql=select_sql)
        logger.info("--> select result " + str(result))
        if result:
            tagPo = TagPO()
            tagPo.__dict__.update(result)
            return tagPo
    except Exception as err:
        logger.error("--> select news error, sql :{}, err :{}".format(select_sql, str(err)))
    finally:
        mysql.dispose()
    return False
