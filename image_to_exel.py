import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

class TrafficCaptureApp:
    def __init__(self, master):
        self.master = master
        master.title("Traffic Capture")

        self.directions = ['Front', 'Back', 'Left', 'Right']
        self.data = []

        self.current_direction_index = 0

        self.label = tk.Label(master, text=f"Upload image for direction: {self.directions[self.current_direction_index]}")
        self.label.pack(pady=10)

        self.upload_button = tk.Button(master, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=5)

        self.vehicle_label = tk.Label(master, text="Enter vehicle types detected (comma separated, e.g. Ambulance, Car, Bike):")
        self.vehicle_label.pack(pady=5)

        self.vehicle_entry = tk.Entry(master, width=50)
        self.vehicle_entry.pack(pady=5)

        self.count_label = tk.Label(master, text="Enter vehicle counts (comma separated, e.g. 1, 3, 5):")
        self.count_label.pack(pady=5)

        self.count_entry = tk.Entry(master, width=50)
        self.count_entry.pack(pady=5)

        self.next_button = tk.Button(master, text="Next Direction", command=self.next_direction)
        self.next_button.pack(pady=10)

        self.excel_button = tk.Button(master, text="Save to Excel", command=self.save_to_excel)
        self.excel_button.pack(pady=10)
        self.excel_button.config(state=tk.DISABLED)

        self.image_path = None

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            title="Select image",
            filetypes=(("Image files", "*.jpg *.jpeg *.png *.bmp"), ("All files", "*.*"))
        )
        if file_path:
            self.image_path = file_path
            messagebox.showinfo("Image Selected", f"Image for {self.directions[self.current_direction_index]} direction selected.")

    def next_direction(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please upload an image before proceeding.")
            return

        vehicle_types = self.vehicle_entry.get().strip()
        counts = self.count_entry.get().strip()

        if not vehicle_types or not counts:
            messagebox.showerror("Error", "Please enter vehicle types and counts.")
            return

        vehicle_list = [v.strip() for v in vehicle_types.split(",")]
        count_list = [c.strip() for c in counts.split(",")]

        if len(vehicle_list) != len(count_list):
            messagebox.showerror("Error", "Number of vehicle types and counts must match.")
            return

        try:
            count_list = [int(c) for c in count_list]
        except ValueError:
            messagebox.showerror("Error", "Vehicle counts must be integers.")
            return

        # Save data for current direction
        for v, c in zip(vehicle_list, count_list):
            self.data.append({
                'Direction': self.directions[self.current_direction_index],
                'Vehicle_Type': v,
                'Count': c,
                'Image_Path': self.image_path
            })

        self.current_direction_index += 1

        if self.current_direction_index >= len(self.directions):
            messagebox.showinfo("Info", "All directions processed. You can save the data to Excel now.")
            self.label.config(text="All directions done.")
            self.upload_button.config(state=tk.DISABLED)
            self.vehicle_label.config(state=tk.DISABLED)
            self.vehicle_entry.config(state=tk.DISABLED)
            self.count_label.config(state=tk.DISABLED)
            self.count_entry.config(state=tk.DISABLED)
            self.next_button.config(state=tk.DISABLED)
            self.excel_button.config(state=tk.NORMAL)
        else:
            self.label.config(text=f"Upload image for direction: {self.directions[self.current_direction_index]}")
            self.vehicle_entry.delete(0, tk.END)
            self.count_entry.delete(0, tk.END)
            self.image_path = None

    def save_to_excel(self):
        if not self.data:
            messagebox.showerror("Error", "No data to save.")
            return
        df = pd.DataFrame(self.data)
        save_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
        if save_path:
            df.to_excel(save_path, index=False)
            messagebox.showinfo("Success", f"Data saved to {save_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TrafficCaptureApp(root)
    root.mainloop()

