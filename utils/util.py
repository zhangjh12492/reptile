import os


def getRootPath():
    """获取项目的根路径"""
    root_path = os.getcwd()
    return "{}{}{}".format(root_path[0:root_path.find('repitle')], "repitle", os.sep)
