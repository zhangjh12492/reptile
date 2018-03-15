class NewsPO:
    """
    新闻
    """
    def __init__(self, id=None, module=None, title=None, synopsis=None, href=None, create_time=None, comment_count=0):
        """
        :param id:
        :param module: 模块
        :param title:  标题
        :param synopsis:  概要
        :param href:    链接
        :param create_time: 发布时间
        :param comment_count:  评论次数
        """
        self.id = id
        self.module = module
        self.title = title
        self.synopsis = synopsis
        self.href = href
        self.create_time = create_time
        self.comment_count = comment_count


class TagPO:
    """
    标签
    """
    def __init__(self, id=None, name=None, href=None):
        """
        :param id:
        :param name:  名称
        :param href:  链接
        """
        self.id = id
        self.name = name
        self.href = href


class NewsTag:
    """
    映射
    """
    def __init__(self, id=None, tag_id=None, news_id=None):
        """
        :param id:
        :param tag_id:  标签id
        :param news_id: 文章id
        """
        self.id = id
        self.tag_id = tag_id
        self.news_id = news_id
