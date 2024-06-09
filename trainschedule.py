import matplotlib.pyplot as plt
class TrainSchedule:
    def __init__(self):
        self.train_lines = {}
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(0, 60)
        plt.xticks(range(0, 61, 5))
        plt.grid(True)

    def add_train_line(self, line_name):
        if line_name not in self.train_lines:
            self.train_lines[line_name] = {
                "stations": {},
                "departure_times": {},
                "station_positions": {}
            }
        self.update_y_axis()

    def add_station(self, line_name, station_name, station_time):
        line = self.train_lines.get(line_name)
        if line:
            if station_name not in line["stations"]:
                position = len(line["stations"]) + 1
                line["station_positions"][station_name] = position
                line["stations"][station_name] = station_time
                line["departure_times"][station_name] = station_time
                # 自动连接前一个站点
                if position > 1:
                    prev_station = list(line["stations"].keys())[-2]
                    self.connect_stations(line_name, prev_station, station_name)
            self.update_y_axis()

    def connect_stations(self, line_name, station1, station2):
        line = self.train_lines.get(line_name)
        if line and station1 in line["departure_times"] and station2 in line["stations"]:
            y1, y2 = line["station_positions"][station1], line["station_positions"][station2]
            x1, x2 = line["departure_times"][station1], line["stations"][station2]
            self.ax.plot([x1, x2], [y1, y2], 'b-')

    def add_stop_duration(self, line_name, station, duration):
        line = self.train_lines.get(line_name)
        if line and station in line["stations"]:
            y_position = line["station_positions"][station]
            x_start = line["stations"][station]
            x_end = x_start + duration
            self.ax.plot([x_start, x_end], [y_position, y_position], 'r-')
            line["departure_times"][station] = x_end

    def update_y_axis(self):
        all_station_names = set()
        for line in self.train_lines.values():
            all_station_names.update(line["station_positions"].keys())
        sorted_station_names = sorted(all_station_names)
        station_position_mapping = {name: i + 1 for i, name in enumerate(sorted_station_names)}
        for line in self.train_lines.values():
            for station_name in line["station_positions"].keys():
                line["station_positions"][station_name] = station_position_mapping[station_name]
        if sorted_station_names:
            self.ax.set_ylim(0, len(sorted_station_names) + 1)
            plt.yticks(range(1, len(sorted_station_names) + 1), sorted_station_names)
        else:
            self.ax.set_ylim(0, 1)
            plt.yticks([])
        self.ax.invert_yaxis()

    def show(self):
        plt.show()

