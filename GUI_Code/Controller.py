import math
import tkinter as tk
import random as rnd
import Serial as SC
from Graphing import Graphing

class Entire_system:

    def __init__(self, full_channels, record_callback=None):
        self.full_channels = full_channels
        self.selected_v_source = 10
        self.selected_c_source = 10 * (10**-6)
        self.selected_sensor = "RTD"
        self.p_limit_v = None
        self.p_limit_a = None
        self.p_limit_c = None
        self.record_callback = record_callback
        self.ser = None
        self.recording = False
        self.recorded_data = []
        self.converted_channels = {
            1 : False,
            2 : False,
            3 : False, 
            4 : False
        }
        #thresholds go [min, max]
        self.thresholds = {
            1: [1, 3], 
            2: [1, 3], 
            3: [1, 3], 
            4: [1, 3], 
            5: [1, 3], 
            6: [1, 3], 
            7: [1, 3], 
            8: [1, 3], 
            }
        #[LED State, alarm state] 0 disabled, 1 live, 2 latching.
        self.channel_states = {
            1: [False, 0], 
            2: [False, 0], 
            3: [False, 0], 
            4: [False, 0], 
            5: [False, 0], 
            6: [False, 0], 
            7: [False, 0], 
            8: [False, 0]
            }
        self.changing_channels = self.deep_copy_channels(full_channels)
        self.previous_channel_states = {}
        self.y_limits = {
            "voltage" : [0, None],
            "acceleration" : [0, None],
            "temperature" : [0, None]
        }
        self.initial_data_check = False #This is used to check through the initial given data for alarms (If there is any)

    def record_data(self, recording:bool):
        if recording:
            self.recording = True
            self.recorded_data = []
        else: 
            self.recording = False
            

    def get_thresholds(self):
        return self.channel_states

    def update_from_serial(self, subject, data, channel=None):
        #print(f"Received update for {subject} on channel {channel}: {data}")

        if subject == "CLR":
            self.clear_data()

        if subject == "VOR":
            if data == 0:
                self.selected_v_source = 10
            else:
                self.selected_v_source = 1
            self.record_callback("VOR", self.selected_v_source)

        elif subject == "LED":
            # Update LED states
            #print("Recieved LED")
            for channel_num, states in self.channel_states.items():
                if data[channel_num-1]: #Because 1s and 0s are stored within data for LED only.
                    states[0] = True
                else:
                    states[0] = False
            self.record_callback("LED", self.channel_states)
            #print(f"LEDs: {self.channel_states}. First column shows LED status, second column shows alarm mode: 0-Disabled, 1-Live, 2-Latching")
        elif subject == "THH":
            #print("Recieved THH")
            # Update high threshold
            self.thresholds[channel][1] = data
            if channel == 8:
                self.record_callback("THH", self.thresholds)
            #   print(f"Thresholds: {self.thresholds}. Left column is lower thresholds, right column is upper thresholds")

        elif subject == "THL":
            #print("Recieved THL")
            # Update low threshold
            self.thresholds[channel][0] = data
            if channel == 8:
                self.record_callback("THL", self.thresholds)
            #   print(f"Thresholds: {self.thresholds}. Left column is lower thresholds, right column is upper thresholds")

        elif subject == "ALM":
            #print("Recieved ALM")
            # Update alarm type
            self.channel_states[channel][1] = data
            if channel == 8:
                self.record_callback("ALM", self.channel_states)
            # if channel == 8:
            #     print(f"Alarms: {self.channel_states}. First column shows LED status, second column shows alarm mode: 0-Disabled, 1-Live, 2-Latching")

        elif subject == "CHR":
            #print("Recieved CHR")
            # Update channel data
            self.insert_real_values(data, channel)
        else:
            print(f"Unknown subject: {subject}")

    def recieve_ser(self, ser):
        self.ser = ser

    def get_voltage_source(self):
        return self.selected_v_source
    
    def change_thresholds(self, channel_num, upper_lim:bool, lim=None): #At least one lim will be input.
        if lim:
            if upper_lim:
                self.thresholds[channel_num][1] = lim
            else:
                self.thresholds[channel_num][0] = lim
        else:
            print("Something went wrong.")

    def get_displayed_channels(self):
        return self.changing_channels
    
    def deep_copy_channels(self, channels):
        # Create a new dictionary to store the deep copy
        new_channels = {}
        for channel_type, channel_name in channels.items():
            new_channels[channel_type] = {}
            for channel, data in channel_name.items():
                # Create a new list for each channel
                new_channels[channel_type][channel] = data[:]
        return new_channels
    
    def change_alarm_types(self, channel_states):
        self.previous_channel_states = self.channel_states
        self.channel_states = channel_states
        for channel_num, states in self.channel_states.items():
            if states not in self.previous_channel_states:
                self.change_indiv_alarm_type(channel_num)

    def change_thresholds(self, upper, lower, channel_num):
        self.thresholds[channel_num] = [lower, upper]
    
    def change_indiv_alarm_type(self, channel_num): #The alarm type is 0 1 2 for disabled, live and latched.
        alarm_type = self.channel_states[channel_num][1]
        if alarm_type == 0:
            text = "DIS"
        elif alarm_type == 1:
            text = "LIV"
        else:
            text = "LAT"
        self.ser.write_to_serial(f"ALM={channel_num}:{text}")

    def change_current(self, current):
        self.selected_c_source = current
    
    def get_selected_current(self):
        return self.selected_c_source
    
    def change_voltage(self, voltage):
        self.selected_v_source = voltage

    def get_selected_voltage(self):
        return self.selected_v_source
    
    def change_sensor(self, sensor):
        self.selected_sensor = sensor

    def change_LED_Alarm_state(self, channel_num, state=bool):
        self.channel_states[channel_num][0] = state

    def get_alarm_states(self):
        return self.channel_states
    
    def clear_data(self):
        self.full_channels = {
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
        self.changing_channels = self.deep_copy_channels(self.full_channels)
        self.maintain_point_limit()

    def limit_graph_points(self, v, a, t, p_limit=None):
        selected_channels = {
            "voltage": v, 
            "acceleration": a, 
            "temperature": t
        }
        try:
            if selected_channels["voltage"]:
                self.p_limit_v = int(p_limit)
            if selected_channels["acceleration"]:
                self.p_limit_a = int(p_limit)
            if selected_channels["temperature"]:
                self.p_limit_c = int(p_limit)
        except ValueError:
            if selected_channels["voltage"]:
                self.p_limit_v = None
            if selected_channels["acceleration"]:
                self.p_limit_a = None
            if selected_channels["temperature"]:
                self.p_limit_c = None

        for channel_type, channel_name in self.changing_channels.items():
            for channel, channel_data in channel_name.items():
                if channel_type == "voltage":
                    p_limit = self.p_limit_v
                if channel_type == "acceleration":
                    p_limit = self.p_limit_a
                if channel_type == "temperature":
                    p_limit = self.p_limit_c
                    
                if p_limit == None:
                    channel_name[channel] = channel_data
                elif len(channel_data) > p_limit:
                    # Keep only the latest 'limit' points and adjust x-axis values
                    latest_data = channel_data[-p_limit:]
                    adjusted_data = [(i, y) for i, (_, y) in enumerate(latest_data, start=len(channel_data) - p_limit)]
                    channel_name[channel] = adjusted_data
                    # If the current limit is less than the new limit, show additional points
                elif len(channel_data) < p_limit:
                    # Assuming you have a way to access the full data history
                    full_data = self.get_full_data(channel_type, channel)  # Implement this function to get full data
                    channel_name[channel] = full_data[-p_limit:]  # Update with the latest 'limit' points

    def maintain_point_limit(self):
        for channel_type, channel_collection in self.changing_channels.items():
            for channel_num, data_list in channel_collection.items():
                if channel_type == "voltage":
                    p_limit = self.p_limit_v
                elif channel_type == "acceleration":
                    p_limit = self.p_limit_a
                elif channel_type == "temperature":
                    p_limit = self.p_limit_c

                if p_limit is None:
                    # If no point limit is set, use the full data
                    full_data = self.get_full_data(channel_type, channel_num)
                    channel_collection[channel_num] = full_data[:]
                else:
                    # Apply the point limit
                    if len(data_list) > p_limit:
                        # Keep only the latest 'limit' points and adjust x-axis values
                        latest_data = data_list[-p_limit:]
                        adjusted_data = [(i, y) for i, (_, y) in enumerate(latest_data, start=len(data_list) - p_limit)]
                        channel_collection[channel_num] = adjusted_data
                    elif len(data_list) < p_limit:
                        # If the current data has fewer points than the limit, fetch more data if available
                        full_data = self.get_full_data(channel_type, channel_num)
                        channel_collection[channel_num] = full_data[-p_limit:]

    def get_full_data(self, channel_type, channel_num):
        if channel_type == "temperature" and channel_num <= 4:
            # If the channel is a converted temperature channel, return the converted data
            return self.changing_channels["temperature"].get(channel_num, [])
        else:
            # For other channels, return the original data
            return self.full_channels[channel_type].get(channel_num, [])
        
    def apply_y_axis_limits(self, graph_storage, v=False, a=False, t=False, y_min=0, y_max=None):
        selected_channels = {
            "voltage": v, 
            "acceleration": a,
            "temperature": t
        }
        try:
            if selected_channels["voltage"]:
                self.y_limits["voltage"][0] = y_min
                self.y_limits["voltage"][1] = y_max
            if selected_channels["acceleration"]:
                self.y_limits["acceleration"][0] = y_min
                self.y_limits["acceleration"][1] = y_max
            if selected_channels["temperature"]:
                self.y_limits["temperature"][0] = y_min
                self.y_limits["temperature"][1] = y_max
        except ValueError:
            if selected_channels["voltage"]:
                self.y_limits["voltage"][0] = 0
                self.y_limits["voltage"][1] = None
            if selected_channels["acceleration"]:
                self.y_limits["acceleration"][0] = 0
                self.y_limits["acceleration"][1] = None
            if selected_channels["temperature"]:
                self.y_limits["temperature"][0] = 0
                self.y_limits["temperature"][1] = None  
        
        for key in graph_storage:
            if len(graph_storage[key]) > 1 and isinstance(graph_storage[key][-1], Graphing):
                if key == 1 and v:  # Voltage graph
                    graph_storage[key][-1].set_axes_limits(ylim=(self.y_limits["voltage"][0], self.y_limits["voltage"][1]))
                elif key == 2 and a:  # Acceleration graph
                    graph_storage[key][-1].set_axes_limits(ylim=(self.y_limits["acceleration"][0], self.y_limits["acceleration"][1]))
                elif key == 3 and t:  # Temperature graph
                    graph_storage[key][-1].set_axes_limits(ylim=(self.y_limits["temperature"][0], self.y_limits["temperature"][1]))


    def Calc_temperature_RTD(self, voltage):
        voltage = abs(voltage)
        #TURN THIS INTO A LOOKUP TABLE. #a table of values, of resistance and temperatures. Shos doing this. 
        RTD_Lookup_table = {
            0: 1000.000,
            1: 1003.910,
            2: 1007.820,
            3: 1011.730,
            4: 1015.640,
            5: 1019.549,
            6: 1023.459,
            7: 1027.368,
            8: 1031.277,
            9: 1035.185,
            10: 1039.094,
            11: 1043.002,
            12: 1046.910,
            13: 1050.818,
            14: 1054.725,
            15: 1058.633,
            16: 1062.540,
            17: 1066.447,
            18: 1070.354,
            19: 1074.260,
            20: 1078.166,
            21: 1082.072,
            22: 1085.978,
            23: 1089.884,
            24: 1093.789,
            25: 1097.694,
            26: 1101.599,
            27: 1105.503,
            28: 1109.408,
            29: 1113.312,
            30: 1117.216,
            31: 1121.119,
            32: 1125.023,
            33: 1128.926,
            34: 1132.829,
            35: 1136.731,
            36: 1140.634,
            37: 1144.536,
            38: 1148.438,
            39: 1152.340,
            40: 1156.241,
            41: 1160.142,
            42: 1164.043,
            43: 1167.944,
            44: 1171.844,
            45: 1175.744,
            46: 1179.644,
            47: 1183.544,
            48: 1187.443,
            49: 1191.342,
            50: 1195.241,
            51: 1199.139,
            52: 1203.038,
            53: 1206.936,
            54: 1210.833,
            55: 1214.731,
            56: 1218.628,
            57: 1222.525,
            58: 1226.421,
            59: 1230.318,
            60: 1234.214
        }
        nearest_temp = None
        
        given_resistance = (voltage / self.selected_c_source) - 380
        # print(f"Given resistance : {given_resistance}")
        min_diff = float('inf')  # Initialize with infinity

        for temp, resistance in RTD_Lookup_table.items():
            diff = abs(resistance - given_resistance)
            if diff < min_diff:
                min_diff = diff
                nearest_temp = temp
        return nearest_temp
        
        # resistance = voltage / self.selected_c_source
        # A = 3.90802 * (10 ** -3)
        # B = -5.802 * (10 ** -7)
        # Rref = 1000
        # print(resistance)
        # return ( -(Rref * A) + math.sqrt(((Rref ** 2) * (A ** 2)) + ((-4) * Rref * B * (Rref - resistance))) / 2 * Rref * B)
    
    def Calc_temperature_Thermister(self, voltage):
        voltage = abs(voltage)
        resistance = voltage / self.selected_c_source
        A = 3.354016 * (10 **-3)
        B = 2.569850 * (10 **-4)
        C = 2.620131 * (10 **-6) 
        D = 6.383091 * (10 **-8)
        # Rref at 25 Degrees is 
        Rref = 10000
        resistance_ratio = math.log(resistance / Rref)
        temp = 1 / (A + B * resistance_ratio + C * resistance_ratio ** 2 + D * resistance_ratio ** 3)
        return temp - 273
    
    def change_v2T(self, channel_data):  # turn V to T
        if self.selected_sensor == "RTD": 

            return [(x, self.Calc_temperature_RTD(y)) for x, y in channel_data]
        else:
            return [(x, self.Calc_temperature_Thermister(y)) for x, y in channel_data]
    
    def VtoT(self, ch1, ch2, ch3, ch4):
        ch1_selected = ch1.get()  # True or False
        ch2_selected = ch2.get()
        ch3_selected = ch3.get()
        ch4_selected = ch4.get()
        channels_selected = [ch1_selected, ch2_selected, ch3_selected, ch4_selected]
        for channel_num, channels_select in enumerate(channels_selected):
            if channels_select:
                self.converted_channels[channel_num+1] = True
            else:
                self.converted_channels[channel_num+1] = False
        self.update_changing_channels()

    def update_changing_channels(self):
        for channel_type, channel_list in self.full_channels.items():
            for channel_num, channel_data in channel_list.items():
                if channel_num <= 4:
                    if self.converted_channels.get(channel_num, True):
                        if channel_type == "voltage":  # if current channel type is voltage
                            if channel_num not in self.changing_channels['temperature']:
                                self.changing_channels['voltage'].pop(channel_num, None)
                            converted_data = self.change_v2T(channel_data)
                            self.changing_channels['temperature'][channel_num] = converted_data
                        elif channel_type == "temperature":
                            if channel_num in self.changing_channels['voltage']:
                                self.changing_channels['voltage'].pop(channel_num, None)
                            self.changing_channels['temperature'][channel_num] = channel_data
                    else:
                        if channel_type == "voltage":
                            if channel_num in self.changing_channels['temperature']:
                                self.changing_channels['temperature'].pop(channel_num, None)
                            self.changing_channels['voltage'][channel_num] = channel_data
                        elif channel_type == "temperature":
                            if channel_num in self.changing_channels['voltage']:
                                self.changing_channels['voltage'].pop(channel_num, None)
                            self.changing_channels['temperature'][channel_num] = channel_data
        self.maintain_point_limit()

    def generate_channel_vals(self):
        channelValues = [0.0] * 8  # Initialize a list with 8 zeros
        for i in range(4):
            random_val = rnd.randint(0, 999)
            val = ((random_val / 1000.0) * 20.0) - 10.0
            channelValues[i] = val
        
        for i in range(4, 7):
            random_val = rnd.randint(0, 999)
            accel = ((random_val / 1000.0) * 10.0) - 5.0
            channelValues[i] = accel
        
        random_val = rnd.randint(0, 999)
        temp = 20.0 + ((random_val / 1000.0) * 10.0)
        if temp > 30.0:
            temp = 30.0
        channelValues[7] = temp
        return channelValues
    
    def insert_real_values(self, data, channel, x=None): #Does it one by one.
        if x:
            count = x
            if channel < 5:
                self.full_channels["voltage"][channel].append((count, data))
            elif channel < 8:
                self.full_channels["acceleration"][channel].append((count, data))
            elif channel == 8:
                self.full_channels["temperature"][channel].append((count, data))
        else:
            if channel < 5:
                count = len(self.full_channels["voltage"][channel])
                self.full_channels["voltage"][channel].append((count, data))
            elif channel < 8:
                count = len(self.full_channels["acceleration"][channel])
                self.full_channels["acceleration"][channel].append((count, data))
            elif channel == 8:
                count = len(self.full_channels["temperature"][channel])
                self.full_channels["temperature"][channel].append((count, data))

        if self.recording:
            self.recorded_data.append((channel, count, data))
        else:
            if self.recorded_data: #If there is anything in there at all
                if self.record_callback:
                    self.record_callback("CHR", self.recorded_data) #Contains [Channel, X, Y],[Channel, X, Y] 
                else:
                    print("Something went wrong 1")
                self.recorded_data = []
        self.update_changing_channels()

    def clear_data(self):
        for channel_num in range(1, 9):
            if channel_num < 5:
                self.full_channels["voltage"][channel_num].clear()
            elif channel_num < 8:
                self.full_channels["acceleration"][channel_num].clear()
            else:
                self.full_channels["temperature"][channel_num].clear()
        self.update_changing_channels()

    def insert_test_values(self):
        test_data = self.generate_channel_vals()
        for channel_num in range(1, 9):
            if channel_num < 5:
                count = len(self.full_channels["voltage"][channel_num])
                self.full_channels["voltage"][channel_num].append((count, test_data[channel_num-1]))
            elif channel_num < 8:
                count = len(self.full_channels["acceleration"][channel_num])
                self.full_channels["acceleration"][channel_num].append((count, test_data[channel_num-1]))
            elif channel_num == 8:
                count = len(self.full_channels["temperature"][channel_num])
                self.full_channels["temperature"][channel_num].append((count, test_data[channel_num-1]))
            if self.recording:
                self.recorded_data.append((channel_num, count, test_data[channel_num-1]))
            else:
                if self.recorded_data: #If there is anything in there at all
                    if self.record_callback:
                        self.record_callback(self.recorded_data) #Contains [Channel, X, Y],[Channel, X, Y] 
                    else:
                        print("Something went wrong 2")
                    self.recorded_data = []
        self.update_changing_channels()




