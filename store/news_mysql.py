from utils.mysql_dbutils import MyPymysqlPool
from common.constants import ENV
from utils.PyLog import logger
from model.news import NewsPO, NewsTag
from utils.convert_obj_util import class_to_dict


def insert(newsPo):
    mysql = MyPymysqlPool(ENV.MYSQL_CONF_TYPE)
    insert_sql = "insert into lp_news(module, title, synopsis, href, create_time, comment_count) " \
                 "values(%d,'%s','%s','%s',%d,'%s')" % (
                     newsPo.module, str(newsPo.title), str(newsPo.synopsis), str(newsPo.href), newsPo.create_time,
                     str(newsPo.comment_count))
    # param = (str(newsPo.module), str(newsPo.title), str(newsPo.synopsis), str(newsPo.href), str(newsPo.create_time),
    #          str(newsPo.comment_count))
    try:
        result = mysql.insert(sql=insert_sql)
        print("--> insert id :{}".format(mysql.getInsertId()))
        newsPo.id = mysql.getInsertId()
        logger.info("--> insert news result : " + str(result))
        return result
    except Exception as err:
        logger.error(
            "--> insert news error, sql :{}, param :{}, \nerr :{}".format(insert_sql, class_to_dict(newsPo), str(err)))
    finally:
        mysql.dispose()
    return 0


def get_one(newsPo):
    try:
        mysql = MyPymysqlPool(ENV.MYSQL_CONF_TYPE)
        select_sql = "select id,module,title,synopsis,href,create_time,comment_count from lp_news "
        where_sql = "where "
        where_start_sql = ""
        if newsPo.id:
            where_start_sql += " and id=%d" % newsPo.id
        if newsPo.href:
            where_start_sql += " and href='%s'" % newsPo.href
        if where_start_sql and where_start_sql.__len__() > 0:
            where_start_sql = where_start_sql[4:]
            select_sql = select_sql + "where " + where_start_sql
        result = mysql.getOne(sql=select_sql)
        logger.info("--> select result " + str(result))
        if result:
            logger.info("id :{}, module:{}, title :{}, ".format(result['id'], result['module'], result['title']))
            newsObj = NewsPO()
            newsObj.__dict__.update(result)
            return newsObj
    except Exception as err:
        logger.error("--> select news error, sql :{}, err :{}".format(select_sql, str(err)))
    finally:
        mysql.dispose()
    return False
