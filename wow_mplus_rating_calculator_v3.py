import tkinter as tk
from tkinter import ttk

# Lookup table for key levels and base scores
lookup_table = {
    0: 0, 2: 40, 3: 45, 4: 50, 5: 55, 6: 60, 7: 75, 8: 80, 9: 89, 10: 90,
    11: 97, 12: 104, 13: 111, 14: 128, 15: 135, 16: 142, 17: 149, 18: 156,
    19: 163, 20: 170, 21: 177, 22: 184, 23: 191, 24: 198, 25: 205,
    26: 212, 27: 219, 28: 226, 29: 233, 30: 240
}

# Dungeons
dungeons = [
    "EB (The Everbloom)", "TOTT (Throne of the Tides)", "AD (Atal'Dazar)",
    "WM (Waycrest Manor)", "DT (Darkheart Thicket)", "BRH (Black Rook Hold)",
    "FALL (DOTI: Galakrond's Fall)", "RISE (DOTI: Murozond's Rise)"
]

# Function to calculate rating
def calculate_rating(fortified_score, tyrannical_score):
    highest_score = max(fortified_score, tyrannical_score)
    lowest_score = min(fortified_score, tyrannical_score)
    return (highest_score * 1.5) + (lowest_score * 0.5)

# Function to estimate the average key level needed to achieve a goal rating
def estimate_average_keys_for_goal(goal_rating, is_tyrannical_week):
    average_score_needed = goal_rating / len(dungeons)
    if is_tyrannical_week:
        average_score_needed /= 1.5
    else:
        average_score_needed /= 0.5
    average_key = min(lookup_table, key=lambda k: abs(lookup_table[k] - average_score_needed))
    return average_key

# Create the main window
root = tk.Tk()
root.title("M+ Rating Calculator")

# Header Labels
tk.Label(root, text="Dungeon").grid(row=0, column=0)
tk.Label(root, text="Fortified Keys").grid(row=0, column=1)
tk.Label(root, text="Tyrannical Keys").grid(row=0, column=2)
tk.Label(root, text="Rating").grid(row=0, column=3)

# Storing variables for each dungeon's slider selections and labels
dungeon_vars = []

# Creating the grid with sliders
for i, dungeon in enumerate(dungeons):
    tk.Label(root, text=dungeon).grid(row=i+1, column=0)
    fortified_slider = tk.Scale(root, from_=0, to=30, orient="horizontal", resolution=1, state="normal")
    tyrannical_slider = tk.Scale(root, from_=0, to=30, orient="horizontal", resolution=1, state="normal")
    fortified_slider.set(15)
    tyrannical_slider.set(15)
    fortified_slider.grid(row=i+1, column=1)
    tyrannical_slider.grid(row=i+1, column=2)
    rating_label = tk.Label(root, text="0.0")
    rating_label.grid(row=i+1, column=3)
    dungeon_vars.append((dungeon, fortified_slider, tyrannical_slider, rating_label))

# Variables for checkboxes
fortified_week = tk.BooleanVar(value=False)
tyrannical_week = tk.BooleanVar(value=False)

# Function to enable/disable sliders based on checkbox selection
def update_sliders():
    for _, fortified_slider, tyrannical_slider, _ in dungeon_vars:
        if fortified_week.get():
            fortified_slider.config(state="normal")
            tyrannical_slider.config(state="disabled")
        elif tyrannical_week.get():
            fortified_slider.config(state="disabled")
            tyrannical_slider.config(state="normal")
        else:
            fortified_slider.config(state="normal")
            tyrannical_slider.config(state="normal")

# Checkboxes for Fortified and Tyrannical weeks
fortified_checkbox = tk.Checkbutton(root, text="Fortified Week", variable=fortified_week, command=lambda: [update_sliders(), tyrannical_week.set(False)])
fortified_checkbox.grid(row=len(dungeons) + 1, column=1)
tyrannical_checkbox = tk.Checkbutton(root, text="Tyrannical Week", variable=tyrannical_week, command=lambda: [update_sliders(), fortified_week.set(False)])
tyrannical_checkbox.grid(row=len(dungeons) + 1, column=2)

# Function to update the ratings and averages, and to calculate the goal difference
def update_ratings():
    total_rating = 0
    for dungeon, fortified_slider, tyrannical_slider, rating_label in dungeon_vars:
        fortified_key = fortified_slider.get()
        tyrannical_key = tyrannical_slider.get()
        fortified_score = lookup_table.get(fortified_key, 0)
        tyrannical_score = lookup_table.get(tyrannical_key, 0)
        rating = calculate_rating(fortified_score, tyrannical_score)
        total_rating += rating
        rating_label.config(text=f"{rating:.1f}")

    total_rating_label.config(text=f"{total_rating:.1f}")

    goal = float(goal_entry.get()) if goal_entry.get() else 0
    difference = goal - total_rating
    goal_difference_label.config(text=f"{difference:.1f}")

    if fortified_week.get() or tyrannical_week.get():
        is_tyrannical_week = tyrannical_week.get()
        estimated_avg_key = estimate_average_keys_for_goal(abs(difference), is_tyrannical_week)
        goal_avg_key_label.config(text=f"{estimated_avg_key}" if is_tyrannical_week else "n/a")
    else:
        goal_avg_key_label.config(text="n/a")

# Average and total labels
avg_fortified = tk.StringVar(value="0.0")
avg_tyrannical = tk.StringVar(value="0.0")
total_rating_label = tk.Label(root, text="0.0")
total_rating_label.grid(row=len(dungeons) + 2, column=1)
tk.Label(root, text="Total Rating:").grid(row=len(dungeons) + 2, column=0)

# Goal section with modified labels for avg key
goal_label = tk.Label(root, text="Goal Total Rating:")
goal_label.grid(row=len(dungeons) + 3, column=0)
goal_entry = tk.Entry(root)
goal_entry.grid(row=len(dungeons) + 3, column=1)

goal_difference_label = tk.Label(root, text="0.0")
goal_difference_label.grid(row=len(dungeons) + 4, column=1)
tk.Label(root, text="Difference:").grid(row=len(dungeons) + 4, column=0)

goal_avg_key_label = tk.Label(root, text="n/a")
goal_avg_key_label.grid(row=len(dungeons) + 5, column=1)
tk.Label(root, text="Goal Avg Key:").grid(row=len(dungeons) + 5, column=0)

# Update button
update_button = tk.Button(root, text="Update Ratings", command=update_ratings)
update_button.grid(row=len(dungeons) + 6, columnspan=4)

# Run the application
root.mainloop()
