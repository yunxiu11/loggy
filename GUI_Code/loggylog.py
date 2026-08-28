import tkinter as tk
import Serial as SC
import Graphing as GRP
import Controller as GUIC
import threading
import time
import csv
# Functions that doesn't make sense going into other files.
# These functions just change the display, either colour or words displayed.
def toggle_graph_selector(button, graph, graphs_chosen):
    if button["bg"] == "green":
        if graph == "voltage":
            graphs_chosen[0] = True
        elif graph == "accel":
            graphs_chosen[1] = True
        elif graph == "temp":
            graphs_chosen[2] = True
        button.config(bg="white")
    else:
        if graph == "voltage":
            graphs_chosen[0] = False
        elif graph == "accel":
            graphs_chosen[1] = False
        elif graph == "temp":
            graphs_chosen[2] = False
        button.config(bg="green")
    GRP.reselect_graphs(channels, graph_frame, graph_storage, graphs_chosen, True)
    GUI.apply_y_axis_limits(graph_storage)

def on_closing():
    global stop_thread
    stop_thread = True
    periodic_thread.join()
    if ser.get_ser() and ser.get_ser().is_open: #Error here
        ser.get_ser().close()
        print("Closing Serial")
    root.quit() 
    exit()

def periodic_checks():
    global stop_thread
    global recording

    while not stop_thread:
        try:
            #GUI.insert_test_values() 
            update_threshold_onoff()

            GRP.reselect_graphs(channels, graph_frame, graph_storage, graphs_chosen)
            GUI.apply_y_axis_limits(graph_storage)
            update_channels()  # Update the GUI channels
        except Exception as e:
            print(f"Error in periodic checks: {e}")
            import traceback
            traceback.print_exc()
        time.sleep(0.5)

def record_data_callback(subject, data):
    #ERROR : Something wrong is happening here : cannot unpack non-iterable int object.
    global V_change_label
    global threshold_levels
    global Options
    global data_storage
    # print(f"Subject: {subject}")
    # print(f"data: {data}")
    if subject == "CHR":
        for channel_data in data:
            data_storage.append(channel_data)  # Append each data point to data_storage
    elif subject == "ALM":
        for channel_num, alarm_mode in data.items(): #Error occues here.
            if channel_num in threshold_levels and "aType" in threshold_levels[channel_num]:
                if alarm_mode[1] == 0:
                    threshold_levels[channel_num]["aType"].set(Options[0])
                elif alarm_mode[1] == 1:
                    threshold_levels[channel_num]["aType"].set(Options[1])
                else:
                    threshold_levels[channel_num]["aType"].set(Options[2])
    elif subject == "THH" or subject == "THL":
        for channel_num, high_low in data.items():
            if channel_num in threshold_levels and subject[-1:] in threshold_levels[channel_num]:
                threshold_levels[channel_num]["H"].config(text=f"{high_low[1]}")
                threshold_levels[channel_num]["L"].config(text=f"{high_low[0]}")
    elif subject == "LED":
        for channel_num, on_off in data.items():
            if on_off[0]:
                threshold_levels[channel_num]["led"].config(text="ON")
            else:
                threshold_levels[channel_num]["led"].config(text="OFF")
    elif subject == "VOR":
        V_change_label.config(text=f"±V Range Select:  {data}V")


def start_recording(button):
    global recording
    if not recording:
        recording = True  # Set recording flag to True
        button.config(text="Stop Recording")  # Update button text
        print("Recording started")  # Debugging print statement
        # Assuming GUI.record_data is a method to start recording
        GUI.record_data(recording)
    else:
        stop_recording(button)

def stop_recording(button):
    global recording, csv_file_path, data_storage
    if recording:
        recording = False  # Set recording flag to False
        GUI.record_data(recording)
        csv_file_path = tk.filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if csv_file_path:
            with recorded_data_lock:  # Ensure thread-safe access
                with open(csv_file_path, 'w', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow(['Channel', 'X', 'Y'])  # Write header
                    for data in data_storage:
                        csv_writer.writerow(data)  # Write recorded data to file
                print(f"Recording stopped and data saved to {csv_file_path}")
        else:
            print("Recording stopped but no file was saved")
        button.config(text="Record Data")  # Update button text
        print("Recording stopped")  # Debugging print statement
        
def replay_data():
    global csv_file_path
    csv_file_path = tk.filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if csv_file_path:
        GUI.clear_data(graph_storage)  # Clear existing data
        with open(csv_file_path, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  # Skip header
            for row in csv_reader:
                channel, x, y = row
                GUI.insert_real_values(float(y), int(channel), int(x))  # Update your GUI with the replayed data
        print(f"Replayed data from {csv_file_path}")
    else:
        print("Replay cancelled")

def update_voltage_range_label(label, v, ser):
    if v.get() == 0:
        v = 10
    else:
        v = 1
    label.config(text=f"±V Range Select : ±{v}V")
    if voltage_range.get() == 1:
        ser.write_to_serial("VOR=0:ONE") #00000011 Voltage Source 1V
        GUI.change_voltage(1)
    else:
        ser.write_to_serial("VOR=0:TEN") #00000010 Voltage Source 10V
        GUI.change_voltage(0)

def update_current_source_label(label, c):
    label.config(text=f"Current Current: {c.get()}uA")
    if current_chosen.get() == 10:
        GUI.change_current(10 * (10**-6))
    else:
        GUI.change_current(200 * (10**-6))

def temp_sensor_change_label(tlabel, t_sensor):
    temp_sensor = t_sensor.get()
    if temp_sensor == 1:
        label = "RTD"       
    elif temp_sensor == 2:
        label = "Thermister" 
    tlabel.config(text=f"Current Temp Sensor: {label}")
    GUI.change_sensor(label)

def high_pressed(button):
    global high_state
    high_state = not high_state
    if high_state:
        button.config(bg="darkblue")
    else:
        button.config(bg="blue")
    update_channels()

def low_pressed(button):
    global low_state
    low_state = not low_state
    if low_state:
        button.config(bg="darkblue")
    else:
        button.config(bg="blue")
    update_channels()

def channel_pressed(channel_num):
    global active_channels
    if channel_num in active_channels:
        active_channels.remove(channel_num)
        btn_list[channel_num-1].config(bg="blue")
    else:
        active_channels.append(channel_num)
        btn_list[channel_num-1].config(bg="darkblue")
    update_channels()

def update_channels():
    for channel_num in range(1, 9):
        alarm_state = GUI.channel_states[channel_num][0] #This is boolean
 
        # Update the alarm state label
        if GUI.channel_states[channel_num][1] != 0:
            if alarm_state:
                threshold_levels[channel_num]["led"].config(text="ON")
            else:
                threshold_levels[channel_num]["led"].config(text="OFF")
        else:
            threshold_levels[channel_num]["led"].config(text="OFF")
        
        if channel_num in active_channels:
            if high_state:
                if isinstance(threshold_levels[channel_num]["H"], tk.Label):
                    label_text = threshold_levels[channel_num]["H"].cget("text")
                    threshold_levels[channel_num]["H"].destroy()
                    threshold_levels[channel_num]["H"] = tk.Entry(small_frames[channel_num][1], textvariable=tk.StringVar(value=label_text), 
                                                                  font=("Arial", 8), bg="white", width=4)
                    threshold_levels[channel_num]["H"].pack(side=tk.LEFT, expand=True)
            else:
                if isinstance(threshold_levels[channel_num]["H"], tk.Entry):
                    entry_text = threshold_levels[channel_num]["H"].get()
                    try:
                        data = float(entry_text)
                        sent_data = int(data * 1000)
                        if sent_data < -32767 or sent_data > 32767:
                            raise ValueError
                    except ValueError as e:
                        print(f"The value entered as threshold isn't a number or threshold is outside acceptable range: {e}")
                        data = 32.767
                        sent_data = 32767

                    threshold_levels[channel_num]["H"].destroy()
                    threshold_levels[channel_num]["H"] = tk.Label(small_frames[channel_num][1], text=data, 
                                                                  font=("Arial", 8), bg="white", width=4, height=2)
                    threshold_levels[channel_num]["H"].pack(side=tk.LEFT, expand=True)
                    ser.write_to_serial(f"THH={channel_num}:{sent_data}")
                    GUI.change_thresholds(channel_num, True, float(data))
            if low_state:
                if isinstance(threshold_levels[channel_num]["L"], tk.Label):
                    label_text = threshold_levels[channel_num]["L"].cget("text")
                    threshold_levels[channel_num]["L"].destroy()
                    threshold_levels[channel_num]["L"] = tk.Entry(small_frames[channel_num][2], textvariable=tk.StringVar(value=label_text), 
                                                                  font=("Arial", 8), bg="white", width=4)
                    threshold_levels[channel_num]["L"].pack(side=tk.LEFT, expand=True)
            else:
                if isinstance(threshold_levels[channel_num]["L"], tk.Entry):
                    entry_text = threshold_levels[channel_num]["L"].get()
                    try:
                        data = float(entry_text)
                        sent_data = int(data * 1000)
                        if sent_data < -32767 or sent_data > 32767:
                            raise ValueError
                    except ValueError as e:
                        print(f"The value entered as threshold isn't a number or threshold is outside acceptable range.")
                        data = 32.767
                        sent_data = 32767

                    threshold_levels[channel_num]["L"].destroy()
                    threshold_levels[channel_num]["L"] = tk.Label(small_frames[channel_num][2], text=data, 
                                                                  font=("Arial", 8), bg="white", width=4, height=2)
                    threshold_levels[channel_num]["L"].pack(side=tk.LEFT, expand=True)
                    ser.write_to_serial(f"THL={channel_num}:{sent_data}")
                    GUI.change_thresholds(channel_num, False, float(data))
        else:
            if isinstance(threshold_levels[channel_num]["H"], tk.Entry):
                entry_text = threshold_levels[channel_num]["H"].get()
                try:
                    data = float(entry_text)
                    sent_data = int(data * 1000)
                    if sent_data < -32767 or sent_data > 32767:
                        raise ValueError
                except ValueError as e:
                    print(f"The value entered as threshold isn't a number or threshold is outside acceptable range.")
                    data = 32.767
                    sent_data = 32767

                threshold_levels[channel_num]["H"].destroy()
                threshold_levels[channel_num]["H"] = tk.Label(small_frames[channel_num][1], text=data, 
                                                              font=("Arial", 8), bg="white", width=4, height=2)
                threshold_levels[channel_num]["H"].pack(side=tk.LEFT, expand=True)
                ser.write_to_serial(f"THH={channel_num}:{sent_data}")
                GUI.change_thresholds(channel_num, True, float(data))

            if isinstance(threshold_levels[channel_num]["L"], tk.Entry):
                entry_text = threshold_levels[channel_num]["L"].get()
                try:
                    data = float(entry_text)
                    sent_data = int(data * 1000)
                    if sent_data < -32767 or sent_data > 32767:
                        raise ValueError
                except ValueError as e:
                    print(f"The value entered as threshold isn't a number or threshold is outside acceptable range.")
                    data = 32.767
                    sent_data = 32767
                threshold_levels[channel_num]["L"].destroy()
                threshold_levels[channel_num]["L"] = tk.Label(small_frames[channel_num][2], text=data, 
                                                              font=("Arial", 8), bg="white", width=4, height=2)
                threshold_levels[channel_num]["L"].pack(side=tk.LEFT, expand=True)
                ser.write_to_serial(f"THL={channel_num}:{sent_data}")
                GUI.change_thresholds(channel_num, False, float(data))
                
def update_threshold_onoff():
    #This should take in data from the thresholds too.
    #if the alarm is latching, then it should not turn off. 
    global threshold_levels
    channel_states = GUI.get_thresholds()
    for channel_num, channel in channel_states.items():
        label = threshold_levels[channel_num]["led"]
        if channel[0]:
            label.config(text="ON")
        else:
            label.config(text="OFF")
                    

# Constants
data_storage = []
recorded_data_lock = threading.Lock()
recording = False
csv_file_path = None
csv_writer = None
previous_actives = []
high_state = False
low_state = False
active_channels = []
btn_list = []
threshold_levels = {}
indiv_frames = {}
small_frames = {}
stop_thread = False
# Graph management
graph_storage = {}
graphs_chosen = [True, True, True]  # Voltage, Accel, Temp


empty_channels = {
'voltage': {
    1: [],
    2: [],
    3: [],
    4: [],
},
'acceleration': {
    5: [],
    6: [],
    7: [],
},
'temperature': {
    8: [],
}
}

#-------------------------------------------------------------------------------------------------------------------------------
GUI = GUIC.Entire_system(empty_channels, record_callback=record_data_callback) #Instead of full_channels, pretty sure itll just be an empty list since data begins at 0.
channels = GUI.get_displayed_channels()

root = tk.Tk()
root.title("GUI for Graphs and Tables")
root.geometry("1800x900")
root.resizable(False, False)

ser = SC.SerialC(root, callback=GUI.update_from_serial)
if ser:
    GUI.recieve_ser(ser)

main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

graph_frame = tk.Frame(main_frame, width=1000, height=750, bg="lightblue")
graph_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)
graph_frame.pack_propagate(False)
graph_label = tk.Label(graph_frame, text="Graph Display Area", font=("Arial", 14), bg="white")
graph_label.pack(pady=20)
GRP.reselect_graphs(channels, graph_frame, graph_storage, graphs_chosen, True)

info_frame = tk.Frame(main_frame, width=520, height=750, bg="lightblue")
info_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)
info_frame.pack_propagate(False)
info_label = tk.Label(info_frame, text="Information", font=("Arial", 14), bg="white")
info_label.pack()

control_frame = tk.Frame(info_frame, width=480, height=100, bg="lightblue")
control_frame.pack(side=tk.BOTTOM, padx=30, pady=10)
control_frame.pack_propagate(False)

table_frame = tk.Frame(info_frame, width=275, height=750, bg="lightblue")
table_frame.pack(side=tk.RIGHT, padx=5, pady=10, fill=tk.X)
table_frame.pack_propagate(False)
table_label = tk.Label(table_frame, text="Channels Graphs", font=("Arial", 14), bg="white")
table_label.pack()

range_frame = tk.Frame(info_frame, width=260, height=750, bg="lightblue")
range_frame.pack(side=tk.LEFT, padx=5, pady=10)
range_frame.pack_propagate(False)
#-------------------------------------------------------------------------------------------------------------------------------
separator = tk.Canvas(main_frame, width=10, height=750, bg="darkgrey")
separator.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

selection_btn_v = tk.Button(control_frame, text="Voltage", padx=20, pady=10, width=10, 
                            command=lambda: toggle_graph_selector(selection_btn_v, "voltage", graphs_chosen), bg="white", fg="blue")
selection_btn_v.pack(side=tk.LEFT, pady=10, fill=tk.Y)

selection_btn_c = tk.Button(control_frame, text="Temperature", padx=20, pady=10, width=10,
                            command=lambda: toggle_graph_selector(selection_btn_c, "temp", graphs_chosen), bg="white", fg="blue")
selection_btn_c.pack(side=tk.RIGHT, pady=10, fill=tk.Y)

selection_btn_a = tk.Button(control_frame, text="Acceleration", padx=20, pady=10, width=10,
                            command=lambda: toggle_graph_selector(selection_btn_a, "accel", graphs_chosen), bg="white", fg="blue")
selection_btn_a.pack(side=tk.BOTTOM, pady=10, fill=tk.Y, expand=True)
#-------------------------------------------------------------------------------------------------------------------------------
y_axis_frame = tk.Frame(range_frame)
y_axis_frame.pack(side=tk.TOP, fill=tk.X)

y_max_frame = tk.Frame(y_axis_frame)
y_max_frame.pack(side=tk.LEFT, padx=5)

y_min_frame = tk.Frame(y_axis_frame)
y_min_frame.pack(side=tk.RIGHT, padx=5)

y_max_label = tk.Label(y_max_frame, text="Max Y-axis:", font=("Arial", 12), bg="white")
y_max_label.pack()
y_max_entry = tk.Entry(y_max_frame, width=10)
y_max_entry.pack()

y_min_label = tk.Label(y_min_frame, text="Min Y-axis:", font=("Arial", 12), bg="white")
y_min_label.pack()
y_min_entry = tk.Entry(y_min_frame, width=10)
y_min_entry.pack()
#-------------------------------------------------------------------------------------------------------------------------------
voltage_selected = tk.BooleanVar()
accel_selected = tk.BooleanVar()
temp_selected = tk.BooleanVar()

channel_selector_frame = tk.Frame(range_frame)
channel_selector_frame.pack(side=tk.TOP, fill=tk.X, padx=10)

channel_selector_1 = tk.Checkbutton(channel_selector_frame, text="Volt", variable=voltage_selected)
channel_selector_2 = tk.Checkbutton(channel_selector_frame, text="Accel", variable=accel_selected)
channel_selector_3 = tk.Checkbutton(channel_selector_frame, text="Temp", variable=temp_selected)

channel_selector_1.pack(side=tk.LEFT)
channel_selector_3.pack(side=tk.RIGHT)
channel_selector_2.pack(side=tk.BOTTOM)

y_axies_apply_button = tk.Button(range_frame, text="Apply Axies", 
                                 command=lambda: GUI.apply_y_axis_limits(
                                     graph_storage, voltage_selected.get(), accel_selected.get(), temp_selected.get(), y_min_entry.get(), y_max_entry.get()))
y_axies_apply_button.pack()
#-------------------------------------------------------------------------------------------------------------------------------
point_limit_label = tk.Label(range_frame, text="Limit point number:", font=("Arial", 12), bg="lightgray")
point_limit_label.pack()
point_limit_entry = tk.Entry(range_frame, width=10)
point_limit_entry.pack() 

v_p_selected = tk.BooleanVar()
a_p_selected = tk.BooleanVar()
t_p_selected = tk.BooleanVar()

point_select_frame = tk.Frame(range_frame)
point_select_frame.pack(fill=tk.X, padx=10)

point_select_v = tk.Checkbutton(point_select_frame, text="Volt", variable=v_p_selected)
point_select_a = tk.Checkbutton(point_select_frame, text="Accel", variable=a_p_selected)
point_select_c = tk.Checkbutton(point_select_frame, text="Temp", variable=t_p_selected)

point_select_v.pack(side=tk.LEFT)
point_select_c.pack(side=tk.RIGHT)
point_select_a.pack(side=tk.BOTTOM)
point_limit_apply_button = tk.Button(range_frame, text="Apply Limits:", 
                                     command=lambda: 
                                     GUI.limit_graph_points(v_p_selected.get(), a_p_selected.get(), t_p_selected.get(), point_limit_entry.get()), bg="white", fg="blue")
point_limit_apply_button.pack()
#-------------------------------------------------------------------------------------------------------------------------------

#Clear button is the only thing that clears full channel
clear_button = tk.Button(range_frame, text="Clear data", command=lambda: GUI.clear_data(), bg="white", fg="blue")
clear_button.pack()
#-------------------------------------------------------------------------------------------------------------------------------
record_stop_frame = tk.Frame(range_frame)
record_stop_frame.pack()

record_btn = tk.Button(record_stop_frame, text="Record Data", command=lambda: start_recording(record_btn), bg="white", fg="blue")
stop_record_btn = tk.Button(record_stop_frame, text="Replay Data", command= replay_data, bg="white", fg="blue")
record_btn.pack(side=tk.LEFT)
stop_record_btn.pack(side=tk.RIGHT)
#-------------------------------------------------------------------------------------------------------------------------------
selected_port = tk.Label(range_frame, text="Selected Port: None")
select_port_btn = tk.Button(range_frame, text="Pick Port", command=lambda: change_label_text_value("Selected Port: ", selected_port))

selected_port.pack()
select_port_btn.pack()

def change_label_text_value(_text:str, label:tk.Label):
    value = ser.choosing_port()
    label.config(text= _text + value)

#-------------------------------------------------------------------------------------------------------------------------------

voltage_range = tk.IntVar(value=1) #NOTE This needs to be whatever the microcontroller is stored at.
V_change_label = tk.Label(range_frame, text=f"±V Range Select:  {voltage_range.get()}V", font=("Arial", 10, "bold"), bg="white")
V_change_label.pack()

voltage_frame = tk.Frame(range_frame)
voltage_frame.pack()

Voltage_range10 = tk.Radiobutton(voltage_frame, text="± 10V", variable=voltage_range, value=0, font=("Arial", 10), bg="white")
Voltage_range1 = tk.Radiobutton(voltage_frame, text="± 1V", variable=voltage_range, value=1, font=("Arial", 10), bg="white")
Voltage_range1.pack(side=tk.LEFT)
Voltage_range10.pack(side=tk.RIGHT)

V_Select_button = tk.Button(range_frame, text="Choose Voltage", command=lambda: update_voltage_range_label(V_change_label, voltage_range, ser), bg="white", fg="blue")
V_Select_button.pack()
#-------------------------------------------------------------------------------------------------------------------------------
current_chosen = tk.IntVar(value=10) 

current_selector_frame = tk.Frame(range_frame, bg="white")
current_selector_frame.pack()
current_selector_label = tk.Label(current_selector_frame, text=f"Current Picker: {current_chosen.get()}uA", font=("Arial", 10, "bold"), bg="white")
current_selector_label.pack()

current_selector_10uA = tk.Radiobutton(current_selector_frame, text="10uA", variable=current_chosen, value=10, font=("Arial", 10), bg="white")
current_selector_200uA = tk.Radiobutton(current_selector_frame, text="200uA", variable=current_chosen, value=200, font=("Arial", 10), bg="white")
current_selector_btn = tk.Button(range_frame, text="Change Current:", 
                                 command=lambda: update_current_source_label(current_selector_label, current_chosen), bg="white", fg="blue")

current_selector_10uA.pack(side=tk.LEFT)
current_selector_200uA.pack(side=tk.RIGHT)
current_selector_btn.pack()
#-------------------------------------------------------------------------------------------------------------------------------
temp_chosen = tk.IntVar(value=1)

temp_sensor_frame = tk.Frame(range_frame, bg="white")
temp_sensor_frame.pack()
temp_sensor_label = tk.Label(temp_sensor_frame, text="Temp Sensor picker:", font=("Arial", 10, "bold"), bg="white")
temp_sensor_label.pack()

temp_sensor_RTD = tk.Radiobutton(temp_sensor_frame, text="RTD", variable=temp_chosen, value=1, font=("Arial", 10), bg="white")
temp_sensor_Thermister = tk.Radiobutton(temp_sensor_frame, text="Thermister", variable=temp_chosen, value=2, font=("Arial", 10), bg="white")
temp_sensor_RTD.pack(side=tk.LEFT)
temp_sensor_Thermister.pack(side=tk.RIGHT)
temp_sensor_change_btn = tk.Button(range_frame, text="Change Sensor:", 
                                   command=lambda: temp_sensor_change_label(temp_sensor_label, temp_chosen), bg="white", fg="blue")
temp_sensor_change_btn.pack()
#-------------------------------------------------------------------------------------------------------------------------------
V2Tframe = tk.Frame(range_frame, bg="white")
V2Tframe.pack()

V2Tlabel = tk.Label(V2Tframe, text="Resistive Temp Picker:", font=("Arial", 12), bg="white")
V2Tlabel.pack(side=tk.TOP)

ch1_select = tk.BooleanVar()
ch2_select = tk.BooleanVar()
ch3_select = tk.BooleanVar()
ch4_select = tk.BooleanVar()

ch1_select_btn = tk.Checkbutton(V2Tframe, text="CH1", variable=ch1_select)
ch2_select_btn = tk.Checkbutton(V2Tframe, text="CH2", variable=ch2_select)
ch3_select_btn = tk.Checkbutton(V2Tframe, text="CH3", variable=ch3_select)
ch4_select_btn = tk.Checkbutton(V2Tframe, text="CH4", variable=ch4_select)

ch1_select_btn.pack(side=tk.LEFT, expand=True)
ch2_select_btn.pack(side=tk.LEFT, expand=True)
ch3_select_btn.pack(side=tk.LEFT, expand=True)
ch4_select_btn.pack(side=tk.LEFT, expand=True)

apply_V2T_btn = tk.Button(range_frame, text="Apply Changes", 
                          command=lambda: GUI.VtoT(ch1_select, ch2_select, ch3_select, ch4_select), bg="white", fg="blue")
apply_V2T_btn.pack(side=tk.TOP)
#-------------------------------------------------------------------------------------------------------------------------------

title_frame = tk.Frame(table_frame, width=450)
title_frame.pack(side=tk.TOP, padx=10, pady=5, fill=tk.X)
onoff_label = tk.Label(title_frame, text="ON/OFF")
onoff_label.pack(side=tk.RIGHT)
alarm_label = tk.Label(title_frame, text="Alarm States")
alarm_label.pack(side=tk.RIGHT)
channel_title = tk.Label(title_frame, text="Channels")
channel_title.pack(side=tk.LEFT)

threshold_frame = tk.Frame(title_frame, width=100, height=45)
threshold_frame.pack(side=tk.BOTTOM)

threshold_label = tk.Label(threshold_frame, text="Thresholds (V)")
threshold_label.pack()
threshold_slave_frame = tk.Frame(threshold_frame)
threshold_slave_frame.pack()
low_btn = tk.Button(threshold_slave_frame, text="HIGH", bg="blue", fg="white", command=lambda: low_pressed(low_btn))
low_btn.pack(side=tk.RIGHT)
high_btn = tk.Button(threshold_slave_frame, text="LOW", bg="blue", fg="white", command=lambda: high_pressed(high_btn))
high_btn.pack(side=tk.LEFT)

for n in range(8):
    indiv_frames[n] = []
    indiv_frames[n].append(tk.Frame(table_frame, width=410, height=60, bg="lightblue"))
    indiv_frames[n][0].pack(side=tk.TOP, padx=8)
    indiv_frames[n][0].pack_propagate(False)

    small_frames[n+1] = []
    for i in range(1, 6):
        small_frame = tk.Frame(indiv_frames[n][0], height=45, bg="lightgray")
        small_frame.pack(side=tk.LEFT, expand=True, fill=tk.X)
        small_frame.pack_propagate(True)
        small_frames[n+1].append(small_frame)
        if i == 1:
            ch_button = tk.Button(small_frame, text=f"CH{n+1}", fg="white", 
                                font=("Arial", 16), bg="blue", 
                                pady=5, relief=tk.RAISED, borderwidth=2, 
                                command=lambda channel=n+1: channel_pressed(channel))
            btn_list.append(ch_button)
            ch_button.pack(fill=tk.Y, expand=True)
        elif i == 2:
            if n + 1 not in threshold_levels:
                threshold_levels[n + 1] = {}
            threshold_levels[n + 1]["H"] = tk.Label(small_frame, text="1.022", font=("Arial", 8), bg="white", width=4, height=2)
            threshold_levels[n + 1]["H"].pack(side=tk.LEFT, expand=True, padx=1)
        elif i == 3:
            if n + 1 not in threshold_levels:
                threshold_levels[n + 1] = {}
            threshold_levels[n + 1]["L"] = tk.Label(small_frame, text="3.103", font=("Arial", 8), bg="white", width=4, height=2)
            threshold_levels[n + 1]["L"].pack(side=tk.LEFT, expand=True, padx=1)
        elif i == 5:
            if n + 1 not in threshold_levels:
                threshold_levels[n + 1] = {}
        
            Options = ["Disabled", "Live", "Latched"]
            threshold_levels[n + 1]["aType"] = tk.StringVar(value="Disabled")
            threshold_levels[n + 1]["A"] = tk.OptionMenu(small_frame, threshold_levels[n + 1]["aType"], *Options)
            threshold_levels[n + 1]["A"].pack(fill=tk.X, side=tk.LEFT, expand=True)
            threshold_levels[n + 1]["A"].pack_propagate(False)
        elif i == 4:
            if n + 1 not in threshold_levels:
                threshold_levels[n + 1] = {}
            threshold_levels[n + 1]["led"] = tk.Label(small_frame, text="OFF", font=("Arial", 8), bg="white", height=2)
            threshold_levels[n + 1]["led"].pack(fill=tk.X, side=tk.LEFT, expand=True, padx=1)
            threshold_levels[n + 1]["led"].pack_propagate(False)
update_channels()

periodic_thread = threading.Thread(target=periodic_checks)
periodic_thread.daemon = True
periodic_thread.start()

# Main loop
root.after(200, ser.check_serial_conn)  # Check the serial I/O and connection every 100ms
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()



