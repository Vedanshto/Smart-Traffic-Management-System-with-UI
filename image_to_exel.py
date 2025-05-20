import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd

class TrafficDataApp:
    def __init__(self, master):
        self.master = master
        master.title("Traffic Vehicle Counter")
        master.geometry("400x450")

        self.data = []

        # Direction
        tk.Label(master, text="Select Direction:").pack(pady=5)
        self.direction_var = tk.StringVar()
        self.direction_combo = ttk.Combobox(master, textvariable=self.direction_var)
        self.direction_combo['values'] = ("Front", "Back", "Left", "Right")
        self.direction_combo.pack()

        # Vehicle types and entries
        self.vehicle_types = ["Car", "Bike", "Truck", "Bus", "Ambulance"]
        self.vehicle_entries = {}

        for v_type in self.vehicle_types:
            tk.Label(master, text=f"{v_type} Count:").pack()
            entry = tk.Entry(master)
            entry.pack()
            self.vehicle_entries[v_type] = entry

        # Buttons
        self.add_button = tk.Button(master, text="Add Entry", command=self.add_entry)
        self.add_button.pack(pady=10)

        self.save_button = tk.Button(master, text="Save to Excel", command=self.save_to_excel)
        self.save_button.pack(pady=10)

    def add_entry(self):
        direction = self.direction_var.get()
        if not direction:
            messagebox.showerror("Error", "Please select a direction.")
            return

        for v_type in self.vehicle_types:
            count_str = self.vehicle_entries[v_type].get()
            if count_str:
                if not count_str.isdigit():
                    messagebox.showerror("Error", f"Invalid count for {v_type}. Must be a number.")
                    return
                self.data.append({
                    "Direction": direction,
                    "Vehicle_Type": v_type,
                    "Count": int(count_str)
                })

        # Clear fields
        self.direction_combo.set('')
        for entry in self.vehicle_entries.values():
            entry.delete(0, tk.END)

        messagebox.showinfo("Added", "Traffic data added.")

    def save_to_excel(self):
        if not self.data:
            messagebox.showerror("Error", "No data to save.")
            return

        df = pd.DataFrame(self.data)
        save_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel files", "*.xlsx")])
        if save_path:
            df.to_excel(save_path, index=False)
            messagebox.showinfo("Success", f"Data saved to {save_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TrafficDataApp(root)
    root.mainloop()
