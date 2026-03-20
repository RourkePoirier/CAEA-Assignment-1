import tkinter as tk

class PropertiesWindow(tk.Frame):
    def __init__(self, parent, entries=None, width=700, height=50):
        super().__init__(parent)

        if entries is None:
            entries = [
                ("Young's Modulus", "GPa"),
                ("Thickness", "m"),
                ("Poisson's Ratio", "")
            ]

        self.entry_widgets = {}  # store entry widgets by key

        #########################################
        # Title
        #########################################
        title = tk.Label(self, text="System Properties:", font=("Arial", 10, "bold"))
        title.grid(row=0, column=0, columnspan=3, pady=(0, 10), sticky="w")

        #########################################
        # Create key-value-unit rows
        #########################################
        for i, (key, unit) in enumerate(entries, start=1):
            label = tk.Label(self, text=f"{key}:")
            entry = tk.Entry(self, width=10)
            unit_label = tk.Label(self, text=f"({unit})" if unit else "")

            label.grid(row=i, column=0, sticky="w")
            entry.grid(row=i, column=1)
            unit_label.grid(row=i, column=2, sticky="w")

            self.entry_widgets[key] = entry

        #########################################
        # Save button
        #########################################
        save_btn = tk.Button(self, text="Save", command=self.save_all)
        save_btn.grid(row=len(entries)+1, column=0, columnspan=3, pady=10)

    #########################################
    # Save callback
    #########################################
    def save_all(self):
        saved_values = {}
        for key, entry in self.entry_widgets.items():
            val_str = entry.get()
            try:
                value = float(val_str)
                saved_values[key] = value
            except ValueError:
                print(f"Invalid number for {key}: '{val_str}'")
        print("Saved values:", saved_values)


if __name__ == "__main__":
    root = tk.Tk()
    pw = PropertiesWindow(root)
    pw.pack(padx=20, pady=20)
    root.mainloop()