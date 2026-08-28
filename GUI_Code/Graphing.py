import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

GRAPH_SIZES = {1: (800, 600), 2: (800, 300), 3: (800, 200)}

class Graphing:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.figure, self.ax = plt.subplots(figsize=(4.5, 7.5))  # 450x750 in inches
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.parent_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def plot_graph(self, channel_data_dict, title="Graph", x_label="X-axis", y_label="Y-axis", labels=None):
        self.ax.clear()  # Clear previous graph

        if channel_data_dict:
            for channel_num, data_list in channel_data_dict.items():
                if data_list:  # Check if data is not empty
                    if isinstance(data_list, list):
                        if all(isinstance(item, tuple) for item in data_list):
                            x_data, y_data = zip(*data_list)
                            label = labels[channel_num] if labels else f"Channel {channel_num}"
                            self.ax.plot(x_data, y_data, marker='o', label=label)
                        else:
                            print("Not all items are tuples")
                    else:
                        print(f"Data List not a list: {data_list}")
        self.ax.set_title(title)
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)
        self.ax.grid(True)  # Add grid for better readability

        # Check if there are any labels to include in the legend
        handles, labels = self.ax.get_legend_handles_labels()
        if handles:
            self.ax.legend(handles, labels, loc="lower left")
        self.canvas.draw()

    def set_axes_limits(self, xlim=None, ylim=None):
        if xlim:
            self.ax.set_xlim(xlim)
        if ylim:
            self.ax.set_ylim(ylim)
        self.canvas.draw()

    def reset_graph(self):
        self.ax.clear()
        self.ax.grid(True)
        self.canvas.draw()

def reselect_graphs(channels, graph_frame, graph_storage, graphs_chosen, reset=False):
    if reset:
        for widget in graph_frame.winfo_children():
            widget.destroy()
        graph_storage.clear()
        plt.close("all")

    for key, chosen in enumerate(graphs_chosen):
        key += 1
        if chosen:
            if reset:
                graph_storage[key] = []
                graph_frame_instance = tk.Frame(graph_frame, width=GRAPH_SIZES[len(graphs_chosen)][0], height=GRAPH_SIZES[len(graphs_chosen)][1], bg="grey")
                graph_frame_instance.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
                graph_frame_instance.pack_propagate(False)
                graph_storage[key].append(graph_frame_instance)

                # Initialize the Graphing instance within the frame
                graph_instance = Graphing(graph_frame_instance)
                graph_storage[key].append(graph_instance)

            # Plot graphs
            if key == 1:
                labels = {i: f"Channel {i} (Voltage)" for i in channels['voltage']}
                graph_storage[key][-1].plot_graph(channels['voltage'], title="Voltages", x_label="Time", y_label="Voltage", labels=labels)
            elif key == 2:
                labels = {i: f"Channel {i} (Acceleration)" for i in channels['acceleration']}
                graph_storage[key][-1].plot_graph(channels['acceleration'], title="Acceleration", x_label="Time", y_label="Acceleration", labels=labels)
            elif key == 3:
                labels = {i: f"Channel {i} (Temperature)" for i in channels['temperature']}
                graph_storage[key][-1].plot_graph(channels['temperature'], title="Temperature", x_label="Time", y_label="Temperature (°C)", labels=labels)

