import re
from tqdm import tqdm


__author__ = "igor.nazarov"


month_to_int_map = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12
}


def next_step(count):
    for _ in tqdm(range(int(count))):
        yield _


class StatParser:
    def __init__(self, connector, url):
        self.__log = connector.get_log()
        self.__file = open(self.__log[0], "r")
        self.__db_conn = connector
        self.__url = url
        self.__methods = ['GET', 'POST']
        self.matched = 0
        self.parsed = 0
        self.count = sum(1 for _ in self.__file)
        self.__progress_gen = next_step(self.count)
        self.__file.close()

        self.__regex = self.__log[1].replace("__DAY__", "(?P<DAY>\d+)")
        self.__regex = self.__regex.replace("__YEAR__", "(?P<YEAR>\d+)")
        self.__regex = self.__regex.replace("__MONTH__", "(?P<MONTH>\w+)")
        self.__regex = self.__regex.replace("__METHOD__", "(?P<METHOD>\w+)")
        self.__regex = self.__regex.replace("__URL__", "(?P<URL>{})".format(url))

    def parse(self):
        self.__file = open(self.__log[0], "r")
        for line in self.__file:
            match = re.match(self.__regex, line)
            if match:
                self.__db_conn.add_url_stat(self.__url,
                                            match.group('METHOD'),
                                            int(match.group('DAY')),
                                            month_to_int_map[match.group('MONTH')],
                                            int(match.group('YEAR'))
                                            )
                self.matched += 1
            self.parsed += 1
            next(self.__progress_gen)
        self.__file.close()
