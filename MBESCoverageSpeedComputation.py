## GUI Program to compute for line spacing with overlap. Ping rate and survey speed.
## LT Marlon E Estropia - 26/01/2024 (GUI Version)
## Reference: Lurton, X. (2010). An introduction to underwater acoustics: Principles and applications (Second edition). Springer.
##            Lecture presentation: Johnson O. Oguntuase. (2021). HYD605 Lurton Chapter 8 Reading 6.

import math
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class MBESCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MBES Line Spacing Computation - LCDR M Estropia")
        self.root.geometry("900x650")
        self.root.minsize(800, 600)

        # --- Variables ---
        self.P_var = tk.StringVar(value="100")
        self.D_var = tk.StringVar(value="50")
        self.SA_var = tk.StringVar(value="120")
        self.c_var = tk.StringVar(value="1542")
        self.ASa_var = tk.StringVar(value="1.0")

        # --- Setup Layout ---
        self.setup_ui()

    def setup_ui(self):
        # --- Left Panel: Inputs and Results ---
        left_frame = ttk.Frame(self.root, padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False)

        # Input Frame
        input_frame = ttk.LabelFrame(left_frame, text="Input Parameters", padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(input_frame, text="Percent Overlap (%):").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(input_frame, textvariable=self.P_var, width=10).grid(row=0, column=1, sticky=tk.E, pady=2)

        ttk.Label(input_frame, text="Depth (m):").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(input_frame, textvariable=self.D_var, width=10).grid(row=1, column=1, sticky=tk.E, pady=2)

        ttk.Label(input_frame, text="Full Swath Angle (°):").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Entry(input_frame, textvariable=self.SA_var, width=10).grid(row=2, column=1, sticky=tk.E, pady=2)

        ttk.Label(input_frame, text="Avg Sound Velocity (m/s):").grid(row=3, column=0, sticky=tk.W, pady=2)
        ttk.Entry(input_frame, textvariable=self.c_var, width=10).grid(row=3, column=1, sticky=tk.E, pady=2)

        ttk.Label(input_frame, text="Along Track Swath Angle (°):").grid(row=4, column=0, sticky=tk.W, pady=2)
        ttk.Entry(input_frame, textvariable=self.ASa_var, width=10).grid(row=4, column=1, sticky=tk.E, pady=2)

        # Buttons
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        ttk.Button(btn_frame, text="Compute & Plot", command=self.compute_and_plot).pack(side=tk.LEFT, padx=5,
                                                                                         expand=True, fill=tk.X)
        ttk.Button(btn_frame, text="Exit", command=self.root.quit).pack(side=tk.RIGHT, padx=5)

        # Results Frame
        results_frame = ttk.LabelFrame(left_frame, text="Results", padding="10")
        results_frame.pack(fill=tk.X, pady=10)

        self.lbl_spacing = ttk.Label(results_frame, text="Line Spacing: -- m", font=('Helvetica', 10, 'bold'))
        self.lbl_spacing.pack(anchor=tk.W, pady=2)

        self.lbl_ping = ttk.Label(results_frame, text="Minimum Ping Rate: -- Hz")
        self.lbl_ping.pack(anchor=tk.W, pady=2)

        self.lbl_speed = ttk.Label(results_frame, text="Maximum Survey Speed: -- knts")
        self.lbl_speed.pack(anchor=tk.W, pady=2)

        # --- Right Panel: Matplotlib Plot ---
        self.right_frame = ttk.Frame(self.root, padding="10")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.fig, self.ax = plt.subplots(figsize=(6, 5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def compute_and_plot(self):
        try:
            # Get values
            P = float(self.P_var.get())
            D = float(self.D_var.get())
            SA = float(self.SA_var.get())
            c = float(self.c_var.get())
            ASa = float(self.ASa_var.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values for all parameters.")
            return

        # Computations
        SArad = math.radians(SA)

        # 1. Line Spacing
        ls_no_overlap = 2 * D * (math.tan(SArad / 2))
        ls_w_overlap = (ls_no_overlap) - ((ls_no_overlap / 2) * (P / 100))

        # 2. Ping Rate
        twtt = (1 / (math.cos(SArad / 2))) * ((2 * D) / c)
        fHz = 1 / twtt if twtt > 0 else 0

        # 3. Survey Speed
        Vmax = math.cos(SArad / 2) * (c / 2) * math.radians(ASa)
        Vmaxknts = 1.94384449 * Vmax

        # Update Result Labels
        self.lbl_spacing.config(text=f"Line Spacing: {ls_w_overlap:.2f} m")
        self.lbl_ping.config(text=f"Minimum Ping Rate: {fHz:.2f} Hz")
        self.lbl_speed.config(text=f"Maximum Survey Speed: {Vmaxknts:.2f} knts")

        # Update Plot
        self.ax.clear()

        # First Swath (Red)
        vertices1 = np.array([[0, D], [0, 0], [-1 * ls_no_overlap / 2, D]])
        vertices1 = np.vstack([vertices1, vertices1[0]])
        self.ax.plot(vertices1[:, 0], vertices1[:, 1], marker='o', color='r')

        vertices2 = np.array([[0, D], [0, 0], [ls_no_overlap / 2, D]])
        vertices2 = np.vstack([vertices2, vertices2[0]])
        self.ax.plot(vertices2[:, 0], vertices2[:, 1], marker='o', color='b')

        # Second Swath (Blue) - shifted by Line Spacing
        vertices3 = np.array([[ls_w_overlap, 0], [ls_w_overlap - (ls_no_overlap / 2), D], [ls_w_overlap, D]])
        vertices3 = np.vstack([vertices3, vertices3[0]])
        self.ax.plot(vertices3[:, 0], vertices3[:, 1], marker='x', color='r')

        vertices4 = np.array([[ls_w_overlap, 0], [ls_w_overlap + (ls_no_overlap / 2), D], [ls_w_overlap, D]])
        vertices4 = np.vstack([vertices4, vertices4[0]])
        self.ax.plot(vertices4[:, 0], vertices4[:, 1], marker='x', color='b')

        # Line Spacing Indicator
        self.ax.plot([0, ls_w_overlap], [0, 0], color='y', linestyle='--', linewidth=2, label=f"{ls_w_overlap:.2f}m")

        # Formatting Plot
        self.ax.legend(loc="upper left")
        self.ax.invert_yaxis()  # Depth goes down
        self.ax.set_xlabel('Swath Width (m)')
        self.ax.set_ylabel('Depth (m)')
        self.ax.set_title(f"Line spacing = {ls_w_overlap:.2f}m\n@ {P}% overlap; {D}m depth; {SA}° full swath angle")

        self.fig.tight_layout()
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = MBESCalculatorApp(root)
    root.mainloop()