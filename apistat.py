import sys

from db import DbConnector
from handlers import help, set_log, make, drop, show


__author__ = "igor.nazarov"


arg_to_func_map = {
    "help": help,
    "setlog": set_log,
    "make": make,
    "drop": drop,
    "show": show
}


db_connection = DbConnector()


if len(sys.argv) <= 2:
    arg_to_func_map['help']()
else:
    arg_to_func_map[sys.argv[1]](sys.argv[2:], db_connection)


