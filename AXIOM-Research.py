import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import math
import csv
import json
import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class AxiomScientificV21:
    def __init__(self, root):
        self.root = root
        self.root.title("AXIOM Scientific Software V2.1")
        self.root.geometry("1100x750")
        self.root.minsize(900, 600)

        self.max_plot_points = 1600

        self.t = None
        self.x = None
        self.v = None
        self.a = None
        self.kinetic = None
        self.potential = None
        self.total_energy = None

        self.build_ui()

    # =========================================================
    # UI
    # =========================================================

    def build_ui(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True)

        self.simulation_tab = ttk.Frame(notebook)
        self.analysis_tab = ttk.Frame(notebook)
        self.calculator_tab = ttk.Frame(notebook)
        self.system_tab = ttk.Frame(notebook)

        notebook.add(self.simulation_tab, text="Simulation")
        notebook.add(self.analysis_tab, text="Analysis")
        notebook.add(self.calculator_tab, text="Calculator")
        notebook.add(self.system_tab, text="System")

        self.build_simulation()
        self.build_analysis()
        self.build_calculator()
        self.build_system()

    # =========================================================
    # SIMULATION
    # =========================================================

    def build_simulation(self):
        left = ttk.Frame(self.simulation_tab, padding=12)
        left.pack(side="left", fill="y")

        right = ttk.Frame(self.simulation_tab, padding=8)
        right.pack(side="right", fill="both", expand=True)

        ttk.Label(
            left,
            text="AXIOM Scientific Software V2.1",
            font=("Arial", 16, "bold")
        ).pack(pady=(0, 12))

        ttk.Label(left, text="Simulation Preset").pack(anchor="w")

        self.preset_var = tk.StringVar(value="Custom")

        presets = [
            "Custom",
            "Simple Oscillator",
            "Damped Oscillator",
            "Low Frequency",
            "High Frequency"
        ]

        preset_box = ttk.Combobox(
            left,
            textvariable=self.preset_var,
            values=presets,
            state="readonly",
            width=23
        )
        preset_box.pack(pady=(3, 12))
        preset_box.bind("<<ComboboxSelected>>", self.apply_preset)

        self.entries = {}

        fields = [
            ("Mass (kg)", "1.0"),
            ("Spring k (N/m)", "10.0"),
            ("Damping c", "0.0"),
            ("Initial position (m)", "1.0"),
            ("Initial velocity (m/s)", "0.0"),
            ("Duration (s)", "10.0"),
            ("Time steps", "2000")
        ]

        for label, default in fields:
            ttk.Label(left, text=label).pack(anchor="w")

            entry = ttk.Entry(left, width=25)
            entry.insert(0, default)
            entry.pack(pady=(2, 7))

            self.entries[label] = entry

        ttk.Label(left, text="Performance Mode").pack(anchor="w")

        self.performance_var = tk.StringVar(value="Lite")

        performance_box = ttk.Combobox(
            left,
            textvariable=self.performance_var,
            values=["Lite", "Standard"],
            state="readonly",
            width=23
        )
        performance_box.pack(pady=(3, 10))

        button_frame = ttk.Frame(left)
        button_frame.pack(fill="x", pady=5)

        ttk.Button(
            button_frame,
            text="Run Simulation",
            command=self.run_simulation
        ).pack(fill="x", pady=2)

        ttk.Button(
            button_frame,
            text="Reset",
            command=self.reset_simulation
        ).pack(fill="x", pady=2)

        ttk.Button(
            button_frame,
            text="Export CSV",
            command=self.export_csv
        ).pack(fill="x", pady=2)

        ttk.Button(
            button_frame,
            text="Import CSV",
            command=self.import_csv
        ).pack(fill="x", pady=2)

        ttk.Button(
            button_frame,
            text="Save Settings",
            command=self.save_settings
        ).pack(fill="x", pady=2)

        ttk.Button(
            button_frame,
            text="Load Settings",
            command=self.load_settings
        ).pack(fill="x", pady=2)

        self.status_label = ttk.Label(
            left,
            text="Ready.",
            wraplength=210
        )
        self.status_label.pack(pady=12)

        self.figure = Figure(figsize=(7, 5), dpi=90)
        self.ax = self.figure.add_subplot(111)

        self.ax.set_title("Position vs Time")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Position (m)")
        self.ax.grid(True)

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=right
        )

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # PRESETS
    # =========================================================

    def apply_preset(self, event=None):
        preset = self.preset_var.get()

        presets = {
            "Simple Oscillator": {
                "Mass (kg)": "1.0",
                "Spring k (N/m)": "10.0",
                "Damping c": "0.0",
                "Initial position (m)": "1.0",
                "Initial velocity (m/s)": "0.0",
                "Duration (s)": "10.0",
                "Time steps": "2000"
            },

            "Damped Oscillator": {
                "Mass (kg)": "1.0",
                "Spring k (N/m)": "10.0",
                "Damping c": "0.8",
                "Initial position (m)": "1.0",
                "Initial velocity (m/s)": "0.0",
                "Duration (s)": "15.0",
                "Time steps": "2500"
            },

            "Low Frequency": {
                "Mass (kg)": "2.0",
                "Spring k (N/m)": "5.0",
                "Damping c": "0.2",
                "Initial position (m)": "1.0",
                "Initial velocity (m/s)": "0.0",
                "Duration (s)": "20.0",
                "Time steps": "3000"
            },

            "High Frequency": {
                "Mass (kg)": "1.0",
                "Spring k (N/m)": "100.0",
                "Damping c": "0.5",
                "Initial position (m)": "1.0",
                "Initial velocity (m/s)": "0.0",
                "Duration (s)": "5.0",
                "Time steps": "3000"
            }
        }

        if preset not in presets:
            return

        for label, value in presets[preset].items():
            self.entries[label].delete(0, tk.END)
            self.entries[label].insert(0, value)

    # =========================================================
    # SIMULATION ENGINE
    # =========================================================

    def run_simulation(self):
        try:
            m = float(self.entries["Mass (kg)"].get())
            k = float(self.entries["Spring k (N/m)"].get())
            c = float(self.entries["Damping c"].get())
            x0 = float(self.entries["Initial position (m)"].get())
            v0 = float(self.entries["Initial velocity (m/s)"].get())
            duration = float(self.entries["Duration (s)"].get())
            steps = int(self.entries["Time steps"].get())

            if m <= 0:
                raise ValueError("Mass must be greater than zero.")

            if k <= 0:
                raise ValueError("Spring constant must be greater than zero.")

            if c < 0:
                raise ValueError("Damping cannot be negative.")

            if duration <= 0:
                raise ValueError("Duration must be greater than zero.")

            if steps < 100:
                raise ValueError("Time steps must be at least 100.")

            if self.performance_var.get() == "Lite":
                steps = min(steps, 5000)
                render_points = 1600
            else:
                steps = min(steps, 15000)
                render_points = 2500

            self.status_label.config(text="Running simulation...")
            self.root.update_idletasks()

            t = np.linspace(0, duration, steps)

            omega0 = math.sqrt(k / m)

            # Underdamped analytical solution
            if c > 0:
                gamma = c / (2 * m)

                if gamma < omega0:
                    omega_d = math.sqrt(omega0 ** 2 - gamma ** 2)

                    A = x0
                    B = (v0 + gamma * x0) / omega_d

                    envelope = np.exp(-gamma * t)

                    x = envelope * (
                        A * np.cos(omega_d * t)
                        + B * np.sin(omega_d * t)
                    )

                    v = envelope * (
                        -A * omega_d * np.sin(omega_d * t)
                        + B * omega_d * np.cos(omega_d * t)
                        - gamma * (
                            A * np.cos(omega_d * t)
                            + B * np.sin(omega_d * t)
                        )
                    )

                    a = -(c / m) * v - (k / m) * x

                elif math.isclose(gamma, omega0, rel_tol=1e-9):
                    A = x0
                    B = v0 + gamma * x0

                    x = (A + B * t) * np.exp(-gamma * t)
                    v = (
                        B * np.exp(-gamma * t)
                        - gamma * (A + B * t) * np.exp(-gamma * t)
                    )

                    a = -(c / m) * v - (k / m) * x

                else:
                    r1 = -gamma + math.sqrt(gamma ** 2 - omega0 ** 2)
                    r2 = -gamma - math.sqrt(gamma ** 2 - omega0 ** 2)

                    C1 = (v0 - r2 * x0) / (r1 - r2)
                    C2 = x0 - C1

                    x = C1 * np.exp(r1 * t) + C2 * np.exp(r2 * t)
                    v = C1 * r1 * np.exp(r1 * t) + C2 * r2 * np.exp(r2 * t)

                    a = -(c / m) * v - (k / m) * x

            else:
                x = (
                    x0 * np.cos(omega0 * t)
                    + (v0 / omega0) * np.sin(omega0 * t)
                )

                v = (
                    -x0 * omega0 * np.sin(omega0 * t)
                    + v0 * np.cos(omega0 * t)
                )

                a = -(k / m) * x

            kinetic = 0.5 * m * v ** 2
            potential = 0.5 * k * x ** 2
            total_energy = kinetic + potential

            self.t = t
            self.x = x
            self.v = v
            self.a = a
            self.kinetic = kinetic
            self.potential = potential
            self.total_energy = total_energy

            self.update_main_plot(render_points)

            initial_energy = total_energy[0]
            final_energy = total_energy[-1]

            if initial_energy != 0:
                energy_change = (
                    abs(final_energy - initial_energy)
                    / abs(initial_energy)
                ) * 100
            else:
                energy_change = 0

            period = 2 * math.pi / omega0

            self.status_label.config(
                text=(
                    f"Simulation complete.\n\n"
                    f"Natural frequency: {omega0:.4f} rad/s\n"
                    f"Period: {period:.4f} s\n"
                    f"Initial energy: {initial_energy:.6g} J\n"
                    f"Final energy: {final_energy:.6g} J\n"
                    f"Energy change: {energy_change:.4f}%\n"
                    f"Points: {steps}"
                )
            )

            self.update_analysis()

        except ValueError as e:
            messagebox.showerror(
                "Invalid Input",
                str(e)
            )

        except Exception as e:
            messagebox.showerror(
                "Simulation Error",
                f"An unexpected error occurred:\n\n{e}"
            )

    # =========================================================
    # MAIN GRAPH
    # =========================================================

    def update_main_plot(self, render_points=1600):
        if self.t is None:
            return

        if len(self.t) > render_points:
            indices = np.linspace(
                0,
                len(self.t) - 1,
                render_points
            ).astype(int)

            t = self.t[indices]
            x = self.x[indices]
        else:
            t = self.t
            x = self.x

        self.ax.clear()

        self.ax.plot(t, x)

        self.ax.set_title("Position vs Time")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Position (m)")
        self.ax.grid(True)

        self.figure.tight_layout()
        self.canvas.draw_idle()

    # =========================================================
    # ANALYSIS
    # =========================================================

    def build_analysis(self):
        top = ttk.Frame(self.analysis_tab, padding=10)
        top.pack(fill="x")

        ttk.Label(
            top,
            text="Simulation Analysis",
            font=("Arial", 16, "bold")
        ).pack(side="left")

        ttk.Button(
            top,
            text="Refresh",
            command=self.update_analysis
        ).pack(side="right")

        self.analysis_text = tk.Text(
            self.analysis_tab,
            height=10,
            wrap="word"
        )
        self.analysis_text.pack(
            fill="x",
            padx=10,
            pady=5
        )

        graph_frame = ttk.Frame(
            self.analysis_tab,
            padding=10
        )
        graph_frame.pack(
            fill="both",
            expand=True
        )

        self.analysis_figure = Figure(
            figsize=(8, 5),
            dpi=90
        )

        self.analysis_ax = self.analysis_figure.add_subplot(111)

        self.analysis_canvas = FigureCanvasTkAgg(
            self.analysis_figure,
            master=graph_frame
        )

        self.analysis_canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

        self.analysis_mode = tk.StringVar(
            value="Velocity"
        )

        control = ttk.Combobox(
            top,
            textvariable=self.analysis_mode,
            values=[
                "Velocity",
                "Acceleration",
                "Energy"
            ],
            state="readonly",
            width=15
        )

        control.pack(
            side="right",
            padx=10
        )

        control.bind(
            "<<ComboboxSelected>>",
            lambda e: self.update_analysis()
        )

    def update_analysis(self):
        if self.t is None:
            return

        self.analysis_text.delete(
            "1.0",
            tk.END
        )

        max_position = np.max(self.x)
        min_position = np.min(self.x)

        max_velocity = np.max(self.v)
        min_velocity = np.min(self.v)

        max_acceleration = np.max(self.a)
        min_acceleration = np.min(self.a)

        rms_position = math.sqrt(
            np.mean(self.x ** 2)
        )

        rms_velocity = math.sqrt(
            np.mean(self.v ** 2)
        )

        initial_energy = self.total_energy[0]
        final_energy = self.total_energy[-1]

        if initial_energy != 0:
            energy_change = (
                (final_energy - initial_energy)
                / initial_energy
            ) * 100
        else:
            energy_change = 0

        text = (
            "POSITION\n"
            f"Maximum: {max_position:.6g} m\n"
            f"Minimum: {min_position:.6g} m\n"
            f"RMS: {rms_position:.6g} m\n\n"

            "VELOCITY\n"
            f"Maximum: {max_velocity:.6g} m/s\n"
            f"Minimum: {min_velocity:.6g} m/s\n"
            f"RMS: {rms_velocity:.6g} m/s\n\n"

            "ACCELERATION\n"
            f"Maximum: {max_acceleration:.6g} m/s²\n"
            f"Minimum: {min_acceleration:.6g} m/s²\n\n"

            "ENERGY\n"
            f"Initial: {initial_energy:.6g} J\n"
            f"Final: {final_energy:.6g} J\n"
            f"Change: {energy_change:.6g}%\n"
        )

        self.analysis_text.insert(
            tk.END,
            text
        )

        mode = self.analysis_mode.get()

        self.analysis_ax.clear()

        if mode == "Velocity":
            y = self.v
            ylabel = "Velocity (m/s)"

        elif mode == "Acceleration":
            y = self.a
            ylabel = "Acceleration (m/s²)"

        else:
            self.analysis_ax.plot(
                self.t,
                self.kinetic,
                label="Kinetic"
            )

            self.analysis_ax.plot(
                self.t,
                self.potential,
                label="Potential"
            )

            self.analysis_ax.plot(
                self.t,
                self.total_energy,
                label="Total"
            )

            self.analysis_ax.set_ylabel(
                "Energy (J)"
            )

            self.analysis_ax.legend()

            self.analysis_ax.set_title(
                "Energy vs Time"
            )

            self.analysis_ax.set_xlabel(
                "Time (s)"
            )

            self.analysis_ax.grid(True)

            self.analysis_figure.tight_layout()
            self.analysis_canvas.draw_idle()

            return

        self.analysis_ax.plot(
            self.t,
            y
        )

        self.analysis_ax.set_title(
            f"{mode} vs Time"
        )

        self.analysis_ax.set_xlabel(
            "Time (s)"
        )

        self.analysis_ax.set_ylabel(
            ylabel
        )

        self.analysis_ax.grid(True)

        self.analysis_figure.tight_layout()
        self.analysis_canvas.draw_idle()

    # =========================================================
    # FFT
    # =========================================================

    def show_fft(self):
        if self.t is None:
            messagebox.showinfo(
                "FFT",
                "Run a simulation first."
            )
            return

        signal = self.x - np.mean(self.x)

        n = len(signal)

        dt = self.t[1] - self.t[0]

        frequencies = np.fft.rfftfreq(
            n,
            d=dt
        )

        amplitudes = np.abs(
            np.fft.rfft(signal)
        )

        if len(amplitudes) > 1:
            dominant_index = np.argmax(
                amplitudes[1:]
            ) + 1

            dominant_frequency = frequencies[
                dominant_index
            ]
        else:
            dominant_frequency = 0

        window = tk.Toplevel(self.root)
        window.title("AXIOM FFT Analysis")
        window.geometry("850x600")

        ttk.Label(
            window,
            text=f"Dominant Frequency: {dominant_frequency:.6g} Hz",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        fig = Figure(
            figsize=(8, 5),
            dpi=90
        )

        ax = fig.add_subplot(111)

        limit = min(
            len(frequencies),
            1500
        )

        ax.plot(
            frequencies[:limit],
            amplitudes[:limit]
        )

        ax.set_title(
            "FFT Frequency Spectrum"
        )

        ax.set_xlabel(
            "Frequency (Hz)"
        )

        ax.set_ylabel(
            "Amplitude"
        )

        ax.grid(True)

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(
            fig,
            master=window
        )

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # CALCULATOR
    # =========================================================

    def build_calculator(self):
        frame = ttk.Frame(
            self.calculator_tab,
            padding=20
        )
        frame.pack(
            fill="both",
            expand=True
        )

        ttk.Label(
            frame,
            text="Scientific Calculator",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        self.calc_entry = ttk.Entry(
            frame,
            font=("Arial", 14)
        )
        self.calc_entry.pack(
            fill="x",
            pady=10
        )

        ttk.Button(
            frame,
            text="Calculate",
            command=self.calculate
        ).pack(pady=5)

        self.calc_result = ttk.Label(
            frame,
            text="Result:",
            font=("Arial", 12)
        )
        self.calc_result.pack(
            pady=10
        )

        ttk.Label(
            frame,
            text=(
                "Available functions:\n"
                "sin, cos, tan, asin, acos, atan,\n"
                "sqrt, log, log10, exp, abs, pi, e"
            )
        ).pack(pady=10)

    def calculate(self):
        try:
            expression = self.calc_entry.get()

            allowed = {
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "asin": math.asin,
                "acos": math.acos,
                "atan": math.atan,
                "sqrt": math.sqrt,
                "log": math.log,
                "log10": math.log10,
                "exp": math.exp,
                "abs": abs,
                "pi": math.pi,
                "e": math.e
            }

            result = eval(
                expression,
                {
                    "__builtins__": {}
                },
                allowed
            )

            self.calc_result.config(
                text=f"Result: {result}"
            )

        except Exception as e:
            self.calc_result.config(
                text=f"Error: {e}"
            )

    # =========================================================
    # CSV
    # =========================================================

    def export_csv(self):
        if self.t is None:
            messagebox.showinfo(
                "Export",
                "Run a simulation first."
            )
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[
                ("CSV files", "*.csv")
            ]
        )

        if not path:
            return

        try:
            with open(
                path,
                "w",
                newline=""
            ) as file:

                writer = csv.writer(file)

                writer.writerow([
                    "time_s",
                    "position_m",
                    "velocity_m_s",
                    "acceleration_m_s2",
                    "kinetic_energy_J",
                    "potential_energy_J",
                    "total_energy_J"
                ])

                for i in range(len(self.t)):
                    writer.writerow([
                        self.t[i],
                        self.x[i],
                        self.v[i],
                        self.a[i],
                        self.kinetic[i],
                        self.potential[i],
                        self.total_energy[i]
                    ])

            messagebox.showinfo(
                "Export Complete",
                "Simulation data exported successfully."
            )

        except Exception as e:
            messagebox.showerror(
                "Export Error",
                str(e)
            )

    def import_csv(self):
        path = filedialog.askopenfilename(
            filetypes=[
                ("CSV files", "*.csv")
            ]
        )

        if not path:
            return

        try:
            data = np.genfromtxt(
                path,
                delimiter=",",
                names=True
            )

            names = data.dtype.names

            if "time_s" not in names:
                raise ValueError(
                    "CSV must contain a time_s column."
                )

            if "position_m" not in names:
                raise ValueError(
                    "CSV must contain a position_m column."
                )

            self.t = np.asarray(
                data["time_s"]
            )

            self.x = np.asarray(
                data["position_m"]
            )

            if "velocity_m_s" in names:
                self.v = np.asarray(
                    data["velocity_m_s"]
                )
            else:
                self.v = np.gradient(
                    self.x,
                    self.t
                )

            if "acceleration_m_s2" in names:
                self.a = np.asarray(
                    data["acceleration_m_s2"]
                )
            else:
                self.a = np.gradient(
                    self.v,
                    self.t
                )

            if "kinetic_energy_J" in names:
                self.kinetic = np.asarray(
                    data["kinetic_energy_J"]
                )
            else:
                self.kinetic = np.zeros_like(
                    self.t
                )

            if "potential_energy_J" in names:
                self.potential = np.asarray(
                    data["potential_energy_J"]
                )
            else:
                self.potential = np.zeros_like(
                    self.t
                )

            if "total_energy_J" in names:
                self.total_energy = np.asarray(
                    data["total_energy_J"]
                )
            else:
                self.total_energy = (
                    self.kinetic
                    + self.potential
                )

            self.update_main_plot()
            self.update_analysis()

            messagebox.showinfo(
                "Import Complete",
                "CSV data imported successfully."
            )

        except Exception as e:
            messagebox.showerror(
                "Import Error",
                str(e)
            )

    # =========================================================
    # SAVE / LOAD SETTINGS
    # =========================================================

    def save_settings(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[
                ("JSON files", "*.json")
            ]
        )

        if not path:
            return

        settings = {}

        for label, entry in self.entries.items():
            settings[label] = entry.get()

        settings["performance"] = (
            self.performance_var.get()
        )

        settings["preset"] = (
            self.preset_var.get()
        )

        try:
            with open(
                path,
                "w"
            ) as file:
                json.dump(
                    settings,
                    file,
                    indent=4
                )

            messagebox.showinfo(
                "Saved",
                "Simulation settings saved."
            )

        except Exception as e:
            messagebox.showerror(
                "Save Error",
                str(e)
            )

    def load_settings(self):
        path = filedialog.askopenfilename(
            filetypes=[
                ("JSON files", "*.json")
            ]
        )

        if not path:
            return

        try:
            with open(
                path,
                "r"
            ) as file:
                settings = json.load(file)

            for label, entry in self.entries.items():
                if label in settings:
                    entry.delete(
                        0,
                        tk.END
                    )

                    entry.insert(
                        0,
                        settings[label]
                    )

            if "performance" in settings:
                self.performance_var.set(
                    settings["performance"]
                )

            if "preset" in settings:
                self.preset_var.set(
                    settings["preset"]
                )

            messagebox.showinfo(
                "Loaded",
                "Simulation settings loaded."
            )

        except Exception as e:
            messagebox.showerror(
                "Load Error",
                str(e)
            )

    # =========================================================
    # RESET
    # =========================================================

    def reset_simulation(self):
        self.t = None
        self.x = None
        self.v = None
        self.a = None
        self.kinetic = None
        self.potential = None
        self.total_energy = None

        self.ax.clear()

        self.ax.set_title(
            "Position vs Time"
        )

        self.ax.set_xlabel(
            "Time (s)"
        )

        self.ax.set_ylabel(
            "Position (m)"
        )

        self.ax.grid(True)

        self.canvas.draw_idle()

        self.analysis_text.delete(
            "1.0",
            tk.END
        )

        self.analysis_ax.clear()

        self.analysis_ax.set_title(
            "No simulation data"
        )

        self.analysis_canvas.draw_idle()

        self.status_label.config(
            text="Ready."
        )

    # =========================================================
    # SYSTEM
    # =========================================================

    def build_system(self):
        frame = ttk.Frame(
            self.system_tab,
            padding=25
        )
        frame.pack(
            fill="both",
            expand=True
        )

        ttk.Label(
            frame,
            text="AXIOM Scientific Software V2.1",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        ttk.Label(
            frame,
            text=(
                "Development Edition\n\n"
                "V2.1 focuses on improved simulation,\n"
                "analysis, data handling and reliability.\n\n"
                "Optimized for lightweight operation."
            ),
            justify="center"
        ).pack(pady=20)

        ttk.Button(
            frame,
            text="Run FFT Analysis",
            command=self.show_fft
        ).pack(pady=10)

        ttk.Label(
            frame,
            text=(
                "AI-assisted development was used during "
                "the creation of AXIOM Scientific Software."
            ),
            wraplength=500,
            justify="center"
        ).pack(pady=20)


# =============================================================
# START PROGRAM
# =============================================================

if __name__ == "__main__":
    root = tk.Tk()

    app = AxiomScientificV21(root)

    root.mainloop()
