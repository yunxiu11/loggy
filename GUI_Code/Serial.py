import serial
import serial.tools.list_ports as port_list
import threading
import tkinter as tk
from tkinter import ttk

class SerialC():
    
    def __init__(self, root, callback=None):
        print("Initializing SerialC instance...")
        self.ser = None
        self.root = root
        self.callback = callback  # Store the callback function
        self.selected_port_value = None
        self.is_connected = False
        self.check_serial_conn()
    
    def choosing_port(self):
        ports = self.get_port_names()

        if not ports:
            tk.messagebox.showerror("Error", "No serial ports found!")
            return None
    
        popup = tk.Toplevel()
        popup.title("Select a serial port")

        label = ttk.Label(popup, text="Available Serial Ports:")
        label.pack(padx=10, pady=10)

        port_var = tk.StringVar()
        port_dropdown = ttk.Combobox(popup, textvariable=port_var, values=ports, state="readonly")
        port_dropdown.pack(padx=10, pady=5)

        if ports:
            port_dropdown.current(0) # Set default value to the first port if available

        def on_select():
            popup.selected_port = port_var.get()
            popup.destroy()

        popup.selected_port = None 
        select_button = ttk.Button(popup, text="Select", command=on_select)
        select_button.pack(pady=10)

        popup.wait_window(popup)

        previous_port = self.selected_port_value
        self.selected_port_value = popup.selected_port

        if self.selected_port_value != previous_port:
            if self.ser and self.ser.is_open:
                print(f"Serial port: {self.selected_port_value} closed.")
                self.ser.close()
            self.is_connected = False
            self.callback("CLR", 0)
        self.check_serial_conn()
        self.is_connected = True
        
        return popup.selected_port

    def get_ser(self):
        if self.ser:
            return self.ser
        else:
            return 

    def check_serial_conn(self):
        if self.is_connected:
            print(f"Serial connection already established with: {self.selected_port_value}.")
            return
        try:
            self.ser = serial.Serial(self.selected_port_value, 9600, timeout=1)
            if self.selected_port_value == None:
                print("No serial connection made, serial not connected.")
            else:
                print(f"Serial connection successful, Connected to {self.selected_port_value}")
                
                self.is_connected = True
                self.start_serial_thread()
                self.write_to_serial("TKINTER")
        except Exception as e:
            print(f"Serial connection failed: {e}")

    def get_port_names(self):
        port_names = [port.device for port in port_list.comports()]
        if len(port_names) > 0:
            print(f"Available ports: {port_names}")
            return port_names
        else:
            print("No available serial ports found.")
            return []

    def start_serial_thread(self):
        # Ensure the method is bound to the instance
        print("Serial reading thread started.")
        thread = threading.Thread(target=self.read_serial_data)
        thread.daemon = True
        thread.start()
        

    def read_serial_data(self):
        print("Reading serial data.")
        try:
            while True:
                if self.ser and self.ser.is_open:
                    data = self.ser.readline().decode('utf-8').strip()
                    if data:
                        #print(f"Data received: {data}")
                        self.handle_incoming_data(data)
                else:
                    print("Serial isn't open somehow")
        except serial.SerialException as e:
            print(f"Serial port disconnected: {e}")
        except Exception as e:
            print(f"Error in serial data reading: {e}")
        finally:
            if self.ser and self.ser.is_open:
                print(f"Serial port: {self.get_selected_port} closed.")
                self.ser.close()
            self.is_connected = False
            while not(self.ser.is_open):
                try:
                    self.check_serial_conn()
                except Exception as e:
                    print(f"Error checking serial connection: {e}")
                    

    def handle_incoming_data(self, data: str):
        try:
            if data:
                # Find the position of '=' and ':'
                equal_index = data.find("=")
                colon_index = data.find(":")
                
                # Extract the subject, channel, and data parts
                subject = data[:equal_index].strip()
                channel = data[equal_index + 1:colon_index].strip()
                c_data = data[colon_index + 1:].strip()
                
                # Validate the data format
                if equal_index == -1:
                    print(data)
                    print(f"Invalid data format (equal)")
                    return
                elif colon_index == -1 and (subject != "LED" and subject != "VOR"):
                    print(data)
                    print(f"Invalid data format (colon)")
                    return

                # Handle different subjects
                if subject == "VOR":  # Voltage range
                    if c_data == "TEN":
                        send = 0
                    else:
                        send = 1
                    if self.callback:
                        self.callback(subject, send)

                elif subject == "THL":  # Low Threshold
                    # print(f"Low Threshold get: {c_data} at channel {channel}")
                    formatted_data = float(c_data) / 1000
                    if self.callback:
                        self.callback(subject, float(formatted_data), int(channel))

                elif subject == "THH":  # High Threshold
                    # print(f"High Threshold get: {c_data} at channel {channel}")
                    formatted_data = float(c_data) / 1000
                    if self.callback:
                        self.callback(subject, float(formatted_data), int(channel))

                elif subject == "ALM":  # Alarm Type #Initial send
                    # print(f"Alarm Type get: {c_data} at channel {channel}")
                    if c_data == "LIV":
                        send = 1
                    elif c_data == "LAT":
                        send = 2
                    else:
                        send = 0
                    if self.callback:
                        self.callback(subject, send, int(channel))

                elif subject == "LED":
                    try:
                        # Convert c_data to an integer
                        if channel == 0:
                            led_states = int(c_data) & 0xFF  # This gives 0bXXXXXXXX, it's now in 8-bit
                            led_list = [(led_states >> i) & 1 for i in range(8)]
                            
                            if self.callback:
                                self.callback(subject, led_list)
                    except ValueError:
                        print(f"Invalid data format for LED: {c_data}")

                elif subject == "CHR":  # Channel Data
                    #print(f"Channel {channel}, {c_data}")
                    try:
                        formatted_data = float(c_data) / 1000
                        #print(f"New data at channel {channel}: {formatted_data}")
                        if self.callback:
                            self.callback(subject, formatted_data, int(channel))
                    except ValueError:
                        print(f"Invalid data format for channel {channel}: {c_data}")
                else:
                    print(f"Unknown subject: {subject}")
        except Exception as e:
            print(f"Error processing incoming data: {e}")

    def write_to_serial(self, data):
        data += "\r"
        if isinstance(data, int):
            data_bytes = data.to_bytes(1, byteorder='big')
        elif isinstance(data, str):
            data_bytes = data.encode()
            # print(data_bytes)
        else:
            data_bytes = data
        if self.ser and self.ser.is_open:
            self.ser.write(data_bytes)
            print(f"Data written to serial: {data_bytes}")
        else:
            print(f"Serial port is not open or not available. but tried to send {data_bytes}")
    
    def change_selected_port(self, port):
        self.selected_port_value = port

