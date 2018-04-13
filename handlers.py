from parser import StatParser
from plotter import StatPlotter


__author__ = "igor.nazarov"


def help(*args):
    with open("./help.txt", "r") as f:
        print(f.read())


def set_log(args, conn):
    conn.set_log(args[0], args[1])


def make(args, conn):
    print("Configurating...")
    parser = StatParser(conn, args[0])
    parser.parse()

    print("Parsing done!")


def show(args, conn):
    print("Plotting...")
    plotter = StatPlotter(conn, args[0], args[1])

    plotter.show()


def drop(args, conn):
    conn.close()
