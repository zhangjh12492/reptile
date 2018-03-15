import os


class PropertiesLoad():
    def __init__(self, path, filename):
        self.path = path
        self.filename = filename

    def get_properties(self):
        properties = {}
        try:
            pro_file = open(self.path + self.filename, 'r')
            for line in pro_file:
                if not line.startswith("#"):
                    strs = line.replace("\n", '').split('=')
                    properties[strs[0]] = strs[1]
            pro_file.close()
        except Exception as e:
            print('--> proc file error,', self.filename, str(e))
        return properties


