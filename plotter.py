from matplotlib import pyplot as plt


__author__ = "igor.nazarov"


int_to_month_map = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec"
}


class StatPlotter:
    def __init__(self, conn, url, method):
        self.__url = url
        self.__method = str(method)
        self.__db_conn = conn

    def show(self):
        data = self.aggregate_to_plot()
        plt.plot(data['x_axis_time'], data['y_axis_count'], label=self.__method)

        plt.title(data['title'])
        plt.legend()

        plt.show()

    def aggregate_to_plot(self):
        stat_years = []

        stat = self.__db_conn.get_url_stat(self.__url, self.__method)
        if stat is not None:
            stat_years.extend([i[2] for i in stat])
            stat_years.sort()
            stat_years = list(set(stat_years))

        stats = []
        for year in stat_years:
            for i in int_to_month_map:
                count = sum(c[3] for c in stat if int(c[2]) == int(year) and int(c[1]) == i)
                stats.append(("{}:{}".format(int_to_month_map[i], int(year - 2000)), count))

        y_axis_values = [i[1] for i in stats]
        x_axis_values = [i[0] for i in stats]

        return {
            "title": "Statistics for {}".format(self.__url),
            "x_axis_time": x_axis_values,
            "years": stat_years,
            "y_axis_count": y_axis_values
        }
