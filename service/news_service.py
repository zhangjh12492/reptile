import json
from utils.PyLog import logger
import os
from utils.configure_read import global_consts
from model.news import NewsPO, NewsTag, TagPO
from utils.date_utils import sifting_date_str_stamp
import re

from utils.convert_obj_util import class_to_dict
from store import news_mysql, tags_mysql, news_tag_mysql


def load_content_file_to_db(index):
    file = None
    try:
        file_path = global_consts["sina_bs_folder"] + "20180313{}{}.txt".format(os.sep, index)
        file = open(file_path, 'r')
        ss = file.read()
        if ss:
            json_cont = json.loads(ss)
            if json_cont.__len__() > 1:
                if isinstance(json_cont, dict):
                    for k, v in json_cont.items():
                        news_po = NewsPO(module=10000, title=v['title'], synopsis=v['synopsis'], href=v['href'],
                                         create_time=sifting_date_str_stamp(v['create_time']),
                                         comment_count=sifting_comment_count(v['comment']))
                        logger.info(class_to_dict(news_po))
                        if news_po.href:
                            get_cont = news_mysql.get_one(NewsPO(href=news_po.href))
                            if get_cont:
                                logger.warn("--> news has exist, href :{}".format(get_cont.href))
                            else:
                                result = news_mysql.insert(news_po)
                                logger.info("--> insert news result : " + str(result))
                        else:
                            result = news_mysql.insert(news_po)
                            logger.info("--> insert news result : " + str(result))

                        tags = v['tags']
                        if tags and tags.__len__() > 0:
                            tag_objs = []
                            for tk in tags:
                                if tk:
                                    tag_obj = TagPO()
                                    for tv in tk:
                                        if str(tv).startswith('http'):
                                            tag_obj.href = tv
                                        else:
                                            tag_obj.name = tv
                                    tag_objs.append(tag_obj)
                            if tag_objs.__len__() > 0:
                                for toj in tag_objs:
                                    if tags_mysql.get_one(toj):
                                        logger.warn("--> tag has exist : {}".format(toj.href))
                                    else:
                                        result = tags_mysql.insert(toj)
                                        logger.info("--> insert tag result : {}".format(result))
                                        if toj.id and news_po.id:
                                            news_tag = NewsTag(tag_id=toj.id, news_id=news_po.id)
                                            result = news_tag_mysql.insert(news_tag)
                                            logger.info("--> insert news_tag result :{}".format(result))




    except Exception as err:
        logger.error("--> load content file error : " + str(err), err)
    finally:
        if file:
            file.close()


def sifting_comment_count(comment):
    match_group = re.search(r"\d+", comment)
    if match_group:
        return int(match_group.group())
    else:
        return 0


if __name__ == '__main__':
    # newsService.load_content_file(3)
    for i in range(1,2):
        load_content_file_to_db(i)
