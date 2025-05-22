import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd

class TrafficDataApp:
    def __init__(self, master):
        self.master = master
        master.title("Traffic Vehicle Counter")
        master.geometry("400x500")
        master.resizable(False, False)

        self.data = []

        # Styles
        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 12))
        style.configure("TButton", font=("Helvetica", 12))
        style.configure("TCombobox", font=("Helvetica", 12))

        # Direction label and dropdown
        label_dir = ttk.Label(master, text="Select Direction:")
        label_dir.pack(pady=(15, 5))

        self.direction_var = tk.StringVar()
        self.direction_combo = ttk.Combobox(master, textvariable=self.direction_var, state="readonly")
        self.direction_combo['values'] = ("Front", "Back", "Left", "Right")
        self.direction_combo.pack(pady=(0, 15))

        # Vehicle types and entries
        self.vehicle_types = ["Car", "Bike", "Truck", "Bus", "Ambulance"]
        self.vehicle_entries = {}

        vehicles_frame = ttk.Frame(master)
        vehicles_frame.pack(pady=(0, 20), fill=tk.X, padx=20)

        for v_type in self.vehicle_types:
            frame = ttk.Frame(vehicles_frame)
            frame.pack(fill=tk.X, pady=5)

            label = ttk.Label(frame, text=f"{v_type} Count:")
            label.pack(side=tk.LEFT, padx=(0, 10))

            entry = ttk.Entry(frame, width=10)
            entry.pack(side=tk.LEFT)
            entry.insert(0, "0")  # default to zero for clarity
            self.vehicle_entries[v_type] = entry

        # Buttons frame
        buttons_frame = ttk.Frame(master)
        buttons_frame.pack(pady=(10, 20))

        self.add_button = ttk.Button(buttons_frame, text="Add Entry", command=self.add_entry)
        self.add_button.pack(side=tk.LEFT, padx=10)

        self.save_button = ttk.Button(buttons_frame, text="Save to Excel", command=self.save_to_excel)
        self.save_button.pack(side=tk.LEFT, padx=10)

    def add_entry(self):
        direction = self.direction_var.get()
        if not direction:
            messagebox.showerror("Input Error", "Please select a direction.")
            return

        any_count_entered = False
        for v_type in self.vehicle_types:
            count_str = self.vehicle_entries[v_type].get().strip()
            if count_str == "":
                count = 0
            else:
                if not count_str.isdigit():
                    messagebox.showerror("Input Error", f"Invalid count for {v_type}. Please enter a non-negative integer.")
                    return
                count = int(count_str)

            if count > 0:
                self.data.append({
                    "Direction": direction,
                    "Vehicle_Type": v_type,
                    "Count": count
                })
                any_count_entered = True

        if not any_count_entered:
            messagebox.showerror("Input Error", "Please enter at least one valid vehicle count greater than zero.")
            return

        # Clear inputs after adding
        self.direction_combo.set('')
        for entry in self.vehicle_entries.values():
            entry.delete(0, tk.END)
            entry.insert(0, "0")

        messagebox.showinfo("Success", "Traffic data added successfully.")

    def save_to_excel(self):
        if not self.data:
            messagebox.showerror("No Data", "No data to save. Please add some entries first.")
            return

        df = pd.DataFrame(self.data)
        save_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel Files", "*.xlsx")],
                                                 title="Save Traffic Data As")
        if save_path:
            try:
                df.to_excel(save_path, index=False)
                messagebox.showinfo("Success", f"Data saved successfully to:\n{save_path}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save file:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TrafficDataApp(root)
    root.mainloop()

