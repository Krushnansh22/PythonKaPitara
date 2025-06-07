import tkinter as tk
import json
import socket
import threading

# Configuration for socket
HOST = 'localhost'
PORT = 65432


class DashboardReceiver:
    def __init__(self, master):
        self.master = master
        master.title("Car Dashboard")
        master.geometry("400x600")
        master.resizable(False, False)

        # Define thresholds for abnormal conditions
        self.thresholds = {
            'temperature_high': 100.0,  # °C
            'temperature_low': 70.0,  # °C
            'coolant_low': 20.0,  # %
            'oil_pressure_low': 25.0,  # psi
            'battery_low': 11.5,  # V
            'tire_pressure_low': 30.0,  # psi
            'fuel_low': 15.0,  # %
            'speed_high': 200.0,  # km/h
            'speed_low': -10.0  # km/h (reverse beyond limit)
        }

        self.abnormalities = []

        self.create_widgets()
        self.start_socket_listener()

    def create_widgets(self):
        self.frame = tk.Frame(self.master)
        self.frame.pack(fill='both', expand=True, padx=20, pady=20)

        tk.Label(self.frame, text="Abnormal Statuses", font=("Helvetica", 16, "bold")).pack(pady=10)

        self.status_text = tk.Text(self.frame, height=25, width=40, state='disabled', bg='#2e2e2e', fg='white',
                                   font=("Helvetica", 12))
        self.status_text.pack(pady=10)

    def start_socket_listener(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen()
        threading.Thread(target=self.listen_for_status, daemon=True).start()

    def listen_for_status(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            with client_socket:
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    status_data = json.loads(data.decode('utf-8'))
                    self.check_abnormalities(status_data)

    def check_abnormalities(self, status_data):
        self.abnormalities.clear()

        # Check conditions
        if status_data['engine_light']:
            self.abnormalities.append("Engine Light ON")

        if status_data['temperature'] > self.thresholds['temperature_high']:
            self.abnormalities.append("High Temperature")
        elif status_data['temperature'] < self.thresholds['temperature_low']:
            self.abnormalities.append("Low Temperature")

        if status_data['coolant_level'] < self.thresholds['coolant_low']:
            self.abnormalities.append("Low Coolant Level")

        if status_data['oil_pressure'] < self.thresholds['oil_pressure_low']:
            self.abnormalities.append("Low Oil Pressure")

        if status_data['battery_voltage'] < self.thresholds['battery_low']:
            self.abnormalities.append("Low Battery Voltage")

        for tire, pressure in status_data['tire_pressure'].items():
            if pressure < self.thresholds['tire_pressure_low']:
                self.abnormalities.append(f"Low Tire Pressure ({tire.replace('_', ' ').title()})")

        if status_data['fuel_level'] < self.thresholds['fuel_low']:
            self.abnormalities.append("Low Fuel Level")

        if status_data['brake_status']:
            self.abnormalities.append("Brakes Engaged")

        if status_data['abs_status']:
            self.abnormalities.append("ABS Engaged")

        if status_data['speed'] > self.thresholds['speed_high']:
            self.abnormalities.append("Speed Over Limit")
        elif status_data['speed'] < self.thresholds['speed_low']:
            self.abnormalities.append("Speed Below Limit")

        self.update_status_display()

    def update_status_display(self):
        self.status_text.config(state='normal')
        self.status_text.delete(1.0, tk.END)

        if not self.abnormalities:
            self.status_text.insert(tk.END, "All systems normal.\n")
        else:
            for abnormality in self.abnormalities:
                self.status_text.insert(tk.END, abnormality + "\n")

        self.status_text.config(state='disabled')


def main():
    root = tk.Tk()
    app = DashboardReceiver(root)
    root.mainloop()


if __name__ == "__main__":
    main()
