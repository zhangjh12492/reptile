import utils.configure_read as configure_read


class PathConfig:
    def __init__(self):
        self.database = configure_read.getConfig('mongodb', 'database')
        self.cluster_host = configure_read.getConfig('mongodb', 'cluster_host')

    def get_database(self):
        return self.database

    def get_cluster_host(self):
        return self.cluster_host
