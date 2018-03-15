from utils.mysql_dbutils import MyPymysqlPool
from common.constants import ENV
from utils.PyLog import logger
from model.news import NewsTag, TagPO
from utils.convert_obj_util import class_to_dict


def insert(newsTagPo):
    mysql = MyPymysqlPool(ENV.MYSQL_CONF_TYPE)
    insert_sql = "insert into lp_news_tag( tag_id, news_id) " \
                 "values( %d, %d)" % (newsTagPo.tag_id, newsTagPo.news_id)
    try:
        result = mysql.insert(sql=insert_sql)
        newsTagPo.id = mysql.getInsertId()
        logger.info("--> insert lp_news_tag result : " + str(result))
        return result
    except Exception as err:
        logger.error(
            "--> insert lp_news_tag error, sql :{}, param :{}, \nerr :{}"
                .format(insert_sql, class_to_dict(newsTagPo), str(err)))
    finally:
        mysql.dispose()
    return 0
