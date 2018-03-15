import configparser
import os
from utils.util import getRootPath
from common.constants import global_consts
from utils.PyLog import logger
from common.constants import ENV


def read_property(file_type, conf_type, name):
    cf = configparser.ConfigParser()
    file_path = "{}conf{}{}{}{}.conf".format(getRootPath(), os.sep, global_consts['dev'], os.sep, file_type)
    logger.info("--> read conf_file " + file_path)
    cf.read(file_path)
    return cf.get(conf_type, name)


def get_cf(file_type=ENV.MYSQL_FILE_TYPE):
    cf = configparser.ConfigParser()
    file_path = "{}conf{}{}{}{}.conf".format(getRootPath(), os.sep, global_consts['dev'], os.sep, file_type)
    logger.info("--> read conf_file " + file_path)
    cf.read(file_path)
    return cf
