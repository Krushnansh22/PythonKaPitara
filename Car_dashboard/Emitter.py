import tkinter as tk
import json
import socket
from tkinter import messagebox

# Configuration for socket
HOST = 'localhost'
PORT = 65432


class StatusGenerator:
    def __init__(self, master):
        self.master = master
        master.title("Car Status Generator")
        master.geometry("400x600")

        self.status = {
            'engine_light': False,
            'temperature': 90.0,  # °C
            'coolant_level': 90.0,  # %
            'oil_pressure': 30.0,  # psi
            'battery_voltage': 12.6,  # V
            'tire_pressure': {
                'front_left': 32.0,  # psi
                'front_right': 32.0,  # psi
                'rear_left': 32.0,  # psi
                'rear_right': 32.0  # psi
            },
            'brake_status': False,
            'fuel_level': 75.0,  # %
            'abs_status': False,
            'speed': 0.0  # km/h
        }

        self.create_widgets()
        self.connect_socket()

    def create_widgets(self):
        # Engine Light
        self.engine_var = tk.BooleanVar(value=self.status['engine_light'])
        tk.Checkbutton(self.master, text="Engine Light", variable=self.engine_var, command=self.update_status).pack(
            anchor='w', padx=10, pady=5)

        # Temperature
        tk.Label(self.master, text="Temperature (°C):").pack(anchor='w', padx=10, pady=(10, 0))
        self.temp_entry = tk.Entry(self.master)
        self.temp_entry.insert(0, str(self.status['temperature']))
        self.temp_entry.pack(anchor='w', padx=10, pady=5)
        self.temp_entry.bind("<Return>", lambda event: self.update_status())

        # Coolant Level
        tk.Label(self.master, text="Coolant Level (%):").pack(anchor='w', padx=10, pady=(10, 0))
        self.coolant_entry = tk.Entry(self.master)
        self.coolant_entry.insert(0, str(self.status['coolant_level']))
        self.coolant_entry.pack(anchor='w', padx=10, pady=5)
        self.coolant_entry.bind("<Return>", lambda event: self.update_status())

        # Oil Pressure
        tk.Label(self.master, text="Oil Pressure (psi):").pack(anchor='w', padx=10, pady=(10, 0))
        self.oil_entry = tk.Entry(self.master)
        self.oil_entry.insert(0, str(self.status['oil_pressure']))
        self.oil_entry.pack(anchor='w', padx=10, pady=5)
        self.oil_entry.bind("<Return>", lambda event: self.update_status())

        # Battery Voltage
        tk.Label(self.master, text="Battery Voltage (V):").pack(anchor='w', padx=10, pady=(10, 0))
        self.battery_entry = tk.Entry(self.master)
        self.battery_entry.insert(0, str(self.status['battery_voltage']))
        self.battery_entry.pack(anchor='w', padx=10, pady=5)
        self.battery_entry.bind("<Return>", lambda event: self.update_status())

        # Tire Pressure
        tk.Label(self.master, text="Tire Pressure (psi):").pack(anchor='w', padx=10, pady=(10, 0))
        self.tire_frames = {}
        for position in ['front_left', 'front_right', 'rear_left', 'rear_right']:
            frame = tk.Frame(self.master)
            frame.pack(anchor='w', padx=20, pady=2)
            tk.Label(frame, text=position.replace('_', ' ').title() + ": ").pack(side='left')
            entry = tk.Entry(frame, width=5)
            entry.insert(0, str(self.status['tire_pressure'][position]))
            entry.pack(side='left', padx=5)
            entry.bind("<Return>", lambda event: self.update_status())
            self.tire_frames[position] = entry

        # Brake Status
        self.brake_var = tk.BooleanVar(value=self.status['brake_status'])
        tk.Checkbutton(self.master, text="Brake Status", variable=self.brake_var, command=self.update_status).pack(
            anchor='w', padx=10, pady=5)

        # Fuel Level
        tk.Label(self.master, text="Fuel Level (%):").pack(anchor='w', padx=10, pady=(10, 0))
        self.fuel_entry = tk.Entry(self.master)
        self.fuel_entry.insert(0, str(self.status['fuel_level']))
        self.fuel_entry.pack(anchor='w', padx=10, pady=5)
        self.fuel_entry.bind("<Return>", lambda event: self.update_status())

        # ABS Status
        self.abs_var = tk.BooleanVar(value=self.status['abs_status'])
        tk.Checkbutton(self.master, text="ABS Status", variable=self.abs_var, command=self.update_status).pack(
            anchor='w', padx=10, pady=5)

        # Speed
        tk.Label(self.master, text="Speed (km/h):").pack(anchor='w', padx=10, pady=(10, 0))
        self.speed_entry = tk.Entry(self.master)
        self.speed_entry.insert(0, str(self.status['speed']))
        self.speed_entry.pack(anchor='w', padx=10, pady=5)
        self.speed_entry.bind("<Return>", lambda event: self.update_status())

        # Exit Button
        tk.Button(self.master, text="Exit", command=self.master.quit).pack(pady=20)

    def update_status(self):
        try:
            self.status['engine_light'] = self.engine_var.get()
            self.status['temperature'] = float(self.temp_entry.get())
            self.status['coolant_level'] = float(self.coolant_entry.get())
            self.status['oil_pressure'] = float(self.oil_entry.get())
            self.status['battery_voltage'] = float(self.battery_entry.get())
            for position, entry in self.tire_frames.items():
                self.status['tire_pressure'][position] = float(entry.get())
            self.status['brake_status'] = self.brake_var.get()
            self.status['fuel_level'] = float(self.fuel_entry.get())
            self.status['abs_status'] = self.abs_var.get()
            self.status['speed'] = float(self.speed_entry.get())

            # Send status via socket
            self.send_status()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values.")

    def connect_socket(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((HOST, PORT))
        except ConnectionRefusedError:
            messagebox.showerror("Connection Error", f"Cannot connect to Dashboard Receiver at {HOST}:{PORT}")
            self.master.quit()

    def send_status(self):
        try:
            message = json.dumps(self.status).encode('utf-8')
            self.client_socket.sendall(message)
        except Exception as e:
            messagebox.showerror("Send Error", f"Failed to send status: {e}")


def main():
    root = tk.Tk()
    app = StatusGenerator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
