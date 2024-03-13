import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import pandas as pd
from src import lv_b, ls_c, lv_d, pv_a, sv_a, beps, bepu, lvd_summary, sva_zone

# Function to get report in CSV and save in specific folders
def get_report_and_save(report_function, name, file_suffix, folder_name, path, output_text):
    report = report_function(name, path)
    file_path = os.path.join(path, f'{folder_name}_{file_suffix}.csv')
    if os.path.isfile(file_path):
        os.remove(file_path)
    with open(file_path, 'w', newline='') as f:
        report.to_csv(f, header=True, index=False, mode='wt')
    output_text.insert(tk.END, "{} Report Generated!\n".format(file_suffix))

def open_input_gui():
    splash.withdraw()  # Hide the splash screen
    input_window = tk.Toplevel()
    input_window.title("SIM File Input")

    # Function to handle closing the input window
    def close_input_window():
        input_window.destroy()
        splash.deiconify()  # Show the splash screen again

    def browse_file():
        file_path = filedialog.askopenfilename(title="Select SIM File", filetypes=(("SIM files", "*.SIM"), ("All files", "*.*")))
        if file_path:
            entry.delete(0, tk.END)
            entry.insert(0, file_path)

    # Labels and Entry for file path
    tk.Label(input_window, text="Enter SIM file path:", font=("Calibri", 12)).pack(pady=5)
    entry = tk.Entry(input_window, width=50)
    entry.pack(pady=5)
    tk.Button(input_window, text="Browse", command=browse_file, font=("Calibri", 10)).pack(pady=5)

    output_text = tk.Text(input_window, wrap="word", height=10, width=60)
    output_text.pack(pady=10)

    # Submit button to generate reports
    def submit():
        sim_file_path = entry.get()
        if os.path.isfile(sim_file_path):
            folder_name = os.path.basename(sim_file_path).split(".")[0]
            # Extracting folder name and parent directory
            if '- Baseline Design' in sim_file_path:
                folder_name = os.path.basename(sim_file_path).split(" - ")[0]
            else:
                folder_name = os.path.basename(sim_file_path).split(".")[0]
            parent_directory = os.path.dirname(sim_file_path)

            get_report_and_save(ls_c.get_LSC_report, sim_file_path, 'lsc', folder_name, parent_directory, output_text)
            get_report_and_save(lv_d.get_LVD_report, sim_file_path, 'lvd', folder_name, parent_directory, output_text)
            get_report_and_save(lvd_summary.get_LVD_Summary_report, sim_file_path, 'lvd_Summary', folder_name, parent_directory, output_text)
            get_report_and_save(pv_a.get_PVA_report, sim_file_path, 'pva', folder_name, parent_directory, output_text)
            get_report_and_save(sv_a.get_SVA_report, sim_file_path, 'sva', folder_name, parent_directory, output_text)
            get_report_and_save(sva_zone.get_SVA_Zone_report, sim_file_path, 'sva_Zone', folder_name, parent_directory, output_text)
            get_report_and_save(beps.get_BEPS_report, sim_file_path, 'beps', folder_name, parent_directory, output_text)
            get_report_and_save(bepu.get_BEPU_report, sim_file_path, 'bepu', folder_name, parent_directory, output_text)
            get_report_and_save(lv_b.get_LVB_report, sim_file_path, 'lvb', folder_name, parent_directory, output_text)
        else:
            output_text.insert(tk.END, "Invalid SIM file path.\n")

    tk.Button(input_window, text="Submit", command=submit, font=("Calibri", 12)).pack(pady=5)

    # Set the input window size to fill the screen
    screen_width = input_window.winfo_screenwidth()
    screen_height = input_window.winfo_screenheight()
    input_window.geometry("{}x{}+0+0".format(screen_width, screen_height))

# Create a new Tkinter window
splash = tk.Tk()
splash.title("SIM Parser")

# Set window icon
# Note: Replace "SIM_Parser_logo.ico" with the path to your icon file
# splash.iconbitmap("SIM_Parser_logo.ico")

# Get the dimensions of the screen
screen_width = splash.winfo_screenwidth()
screen_height = splash.winfo_screenheight()

# Set the size and position of the splash screen window
splash_geometry = "400x200+{}+{}".format(screen_width//2 - 200, screen_height//2 - 100)
splash.geometry(splash_geometry)

a = '#249794'
frame = tk.Frame(splash, width=400, height=200, bg=a)
frame.pack(fill="both", expand=True)

tk.Label(frame, text='SIM', fg='white', bg=a, font=('Calibri (Body)', 18, 'bold')).place(x=50, y=80)
tk.Label(frame, text='Output CSV reports', fg='white', bg=a, font=('Calibri (Body)', 18)).place(x=155, y=82)
tk.Label(frame, text='Parser', fg='white', bg=a, font=('Calibri (Body)', 13, 'bold')).place(x=50, y=110)

progress = ttk.Progressbar(frame, orient='horizontal', length=300, mode='indeterminate')
progress.place(x=50, y=150)

tk.Button(frame, width=10, height=2, text='Get Started', command=open_input_gui, border=0, fg=a, bg='white').place(x=150, y=110)

# Run the splash screen
splash.mainloop()