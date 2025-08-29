# Weekly Schedule Builder Project

import tkinter as tk
from tkinter import messagebox, filedialog
import json
import csv
import os

# CONSTANTS
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
TIME_BLOCKS = ["Morning", "Afternoon", "Evening"]
SAVE_FILE = "weekly_schedule.json"

class ScheduleApp:
    def __init__(self, root):
        # window setup
        self.root = root
        self.root.title("Weekly Schedule Builder")
        self.entries = {}

        #build the UI
        self.create_grid()
        self.create_buttons()

    # Build the grid
    def create_grid(self):
        # top left corner cell
        tk.Label(self.root, text="Time/Day", relief="ridge", width=12).grid(row=0, column=0)

        # column headers: days
        for col, day in enumerate(DAYS, 1):
            tk.Label(self.root, text=day, relief="ridge", width=15).grid(row=0, column=col)

        # rows: time blocks; columns: days; each cell is an Entry
        for row, tbk in enumerate(TIME_BLOCKS, 1):
            # row header (time block)
            tk.Label(self.root, text=tbk, relief="ridge", width=12). grid(row=row, column=0)

            for col, day in enumerate(DAYS, 1):
                entry = tk.Entry(self.root, width=18)
                entry.grid(row=row, column=col)
                self.entries[(day, tbk)] = entry

    # Build the buttons
    def create_buttons(self):
        # a thin seperator row under the grid for spacing
        sep_row = len(TIME_BLOCKS) + 1

        tk.Button(self.root, text="New Blank", command=self.new_blank)\
            .grid(row=sep_row+1, column=0, pady=10)
        tk.Button(self.root, text="Load JSON", command=self.load)\
            .grid(row=sep_row+1, column=1, pady=10)
        tk.Button(self.root, text="Save JSON", command=self.save)\
            .grid(row=sep_row+1, column=2, pady=10)
        tk.Button(self.root, text="Export CSv", command=self.export_csv)\
            .grid(row=sep_row+1, column=3, pady=10)
        tk.Button(self.root, text="Quit", command=self.root.quit)\
            .grid(row=sep_row+1, column=4, pady=10)

    def get_schedule(self):
        """Collect all Entry values into a nested dict {day: {block: task}}."""
        return {
            day: {tbk: self.entries[(day, tbk)].get().strip()
                  for tbk in TIME_BLOCKS} for day in DAYS
        }

    def set_schedule(self, schedule):
        """Fill the grid from a nested dict schedule."""
        for day in DAYS:
            for tbk in TIME_BLOCKS:
                self.entries[(day, tbk)].delete(0, tk.END)
                self.entries[(day, tbk)].insert(0, schedule.get(day, {}).get(tbk, ""))

    # Button Action
    def new_blank(self):
        """Clear all cells,"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def save(self):
        """Save to JSON file SAVE_FILE  (or prompt for path)."""
        schedule = self.get_schedule()

        # let the user choose a path (default to SAVE_FILE)
        path = filedialog.asksaveasfilename(
            title="Save schedule JSON",
            defaultextension= ".json",
            initialfile= SAVE_FILE,
            filetypes=[("JSON files", "*.json")]
        )
        if not path:
            return

        try:
            with open(path, "w", encoding="utf-8") as file:
                json.dump(schedule, file, indent=2)
            messagebox.showinfo("Saved", f"Schedule saved to {os.path.basename(path)}")
        except Exception as err:
            messagebox.showerror("Error", f"Failed to save: {err}")

    def load(self):
        """Load Schedule from a JSON file."""
        path = filedialog.askopenfilename(
            title="Load schedule JSON",
            filetypes=[("JSON files", "*.json")]
        )
        if not path:
            return

        try:
            with open(path, "r", encoding="utf-8") as file:
                schedule = json.load(file)
            self.set_schedule(schedule)
            messagebox.showinfo("Loaded", f"Loaded {os.path.basename(path)}")
        except Exception as err:
            messagebox.showerror("Error", f"Failed to load: {err}")

    def export_csv(self):
        """Export schedule to CSV in either wide (columns per block) or
        long (row per cell) format."""
        schedule = self.get_schedule()

        #ask format
        choice = messagebox.askquestion(
            "CSV Format",
            "Export in WIDE format? (Yes = Wide columns per block, "
            "No = Long day/block rows)"
        )
        wide = (choice == "yes")

        path = filedialog.asksaveasfilename(
            title="Export CSV",
            defaultextension=".csv",
            initialfile="weekly_schedule.csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if not path:
            return

        try:
            with open(path, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)

                if wide:
                    # Header: Day + each block as a column
                    writer.writerow(["Days"] + TIME_BLOCKS)
                    for day in DAYS:
                        row = [day] + [schedule[day][tbk] for tbk in TIME_BLOCKS]
                        writer.writerow(row)

                else:
                    # Long: each row = Day, Block Task
                    writer.writerow(["Day", "Time Block", "Task"])
                    for day in DAYS:
                        for tbk in TIME_BLOCKS:
                            writer.writerow([day, tbk, schedule[day][tbk]])

            messagebox.showinfo("Exported", f"CSV exported to "
                                            f"{os.path.basename(path)}")

        except Exception as err:
            messagebox.showerror("Error", f"Failed to export CSV: {err}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ScheduleApp(root)
    root.mainloop()



































