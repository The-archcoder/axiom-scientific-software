"""
AXIOM Scientific Software V2
Optimized for low-end PCs.

Install:
    pip install numpy matplotlib
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import math
import time
import csv

import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class AxiomScientificV2:
    def __init__(self, root):
        self.root = root
        self.root.title("AXIOM Scientific Software V2")
        self.root.geometry("1050x700")
        self.root.minsize(850, 580)

        self.time_data = None
        self.position_data = None

        self.max_plot_points = 1600

        self.build_ui()

    def build_ui(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Title.TLabel",
            font=("Segoe UI", 18, "bold")
        )

        style.configure(
            "Section.TLabel",
            font=("Segoe UI", 11, "bold")
        )

        # Header
        header = ttk.Frame(self.root, padding=10)
        header.pack(fill="x")

        ttk.Label(
            header,
            text="AXIOM Scientific Software V2",
            style="Title.TLabel"
        ).pack(side="left")

        ttk.Label(
            header,
            text="   Lightweight Scientific Workstation"
        ).pack(side="left")

        # Tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

        self.simulation_tab = ttk.Frame(
            notebook,
            padding=10
        )

        self.calculator_tab = ttk.Frame(
            notebook,
            padding=10
        )

        self.system_tab = ttk.Frame(
            notebook,
            padding=10
        )

        notebook.add(
            self.simulation_tab,
            text="Harmonic Oscillator"
        )

        notebook.add(
            self.calculator_tab,
            text="Calculator"
        )

        notebook.add(
            self.system_tab,
            text="System"
        )

        self.build_simulation()
        self.build_calculator()
        self.build_system()

    # ---------------------------------------------------------
    # SIMULATION
    # ---------------------------------------------------------

    def build_simulation(self):

        controls = ttk.LabelFrame(
            self.simulation_tab,
            text="Simulation Parameters",
            padding=10
        )

        controls.pack(
            side="left",
            fill="y"
        )

        parameters = [
            ("Mass (kg)", "1.0"),
            ("Spring k (N/m)", "10.0"),
            ("Initial position (m)", "1.0"),
            ("Initial velocity (m/s)", "0.0"),
            ("Duration (s)", "10.0"),
            ("Time steps", "2000")
        ]

        self.entries = {}

        for row, (name, value) in enumerate(parameters):

            ttk.Label(
                controls,
                text=name
            ).grid(
                row=row,
                column=0,
                sticky="w",
                pady=5
            )

            entry = ttk.Entry(
                controls,
                width=16
            )

            entry.insert(
                0,
                value
            )

            entry.grid(
                row=row,
                column=1,
                padx=(10, 0),
                pady=5
            )

            self.entries[name] = entry

        ttk.Label(
            controls,
            text="Performance Mode",
            style="Section.TLabel"
        ).grid(
            row=6,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(20, 5)
        )

        self.performance_mode = tk.StringVar(
            value="Lite"
        )

        mode = ttk.Combobox(
            controls,
            textvariable=self.performance_mode,
            values=["Lite", "Standard"],
            state="readonly",
            width=13
        )

        mode.grid(
            row=7,
            column=0,
            columnspan=2,
            sticky="w"
        )

        ttk.Button(
            controls,
            text="Run Simulation",
            command=self.run_simulation
        ).grid(
            row=8,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(20, 5)
        )

        ttk.Button(
            controls,
            text="FFT Analysis",
            command=self.run_fft
        ).grid(
            row=9,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=5
        )

        ttk.Button(
            controls,
            text="Save CSV",
            command=self.save_csv
        ).grid(
            row=10,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=5
        )

        self.status = tk.StringVar(
            value="Ready."
        )

        ttk.Label(
            controls,
            textvariable=self.status,
            wraplength=190
        ).grid(
            row=11,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(20, 0)
        )

        # Graph area
        graph_frame = ttk.Frame(
            self.simulation_tab
        )

        graph_frame.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(10, 0)
        )

        self.figure = Figure(
            figsize=(7, 5),
            dpi=80
        )

        self.ax = self.figure.add_subplot(111)

        self.ax.set_title(
            "Position vs Time"
        )

        self.ax.set_xlabel(
            "Time (s)"
        )

        self.ax.set_ylabel(
            "Position (m)"
        )

        self.ax.grid(
            True,
            alpha=0.25
        )

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=graph_frame
        )

        self.canvas.draw()

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

        self.info = tk.Text(
            graph_frame,
            height=6,
            wrap="word"
        )

        self.info.pack(
            fill="x",
            pady=(8, 0)
        )

        self.set_info(
            "Run a simulation to display results."
        )

    def get_float(self, name):

        return float(
            self.entries[name].get()
        )

    def get_int(self, name):

        return int(
            self.entries[name].get()
        )

    def run_simulation(self):

        start_time = time.perf_counter()

        try:

            mass = self.get_float(
                "Mass (kg)"
            )

            spring_k = self.get_float(
                "Spring k (N/m)"
            )

            x0 = self.get_float(
                "Initial position (m)"
            )

            v0 = self.get_float(
                "Initial velocity (m/s)"
            )

            duration = self.get_float(
                "Duration (s)"
            )

            steps = self.get_int(
                "Time steps"
            )

            if mass <= 0:
                raise ValueError(
                    "Mass must be greater than zero."
                )

            if spring_k <= 0:
                raise ValueError(
                    "Spring k must be greater than zero."
                )

            if duration <= 0:
                raise ValueError(
                    "Duration must be greater than zero."
                )

            if steps < 50:
                raise ValueError(
                    "Use at least 50 time steps."
                )

            if steps > 200000:
                raise ValueError(
                    "Maximum is 200000 time steps."
                )

            # Low-end optimization
            if self.performance_mode.get() == "Lite":

                steps = min(
                    steps,
                    5000
                )

                render_points = 1600

            else:

                render_points = 2500

            # Time array
            t = np.linspace(
                0,
                duration,
                steps
            )

            # Angular frequency
            omega = math.sqrt(
                spring_k / mass
            )

            # Analytical harmonic oscillator
            position = (
                x0 * np.cos(omega * t)
                +
                (v0 / omega)
                *
                np.sin(omega * t)
            )

            velocity = (
                -x0
                *
                omega
                *
                np.sin(omega * t)
                +
                v0
                *
                np.cos(omega * t)
            )

            # Energy
            kinetic_energy = (
                0.5
                *
                mass
                *
                velocity
                *
                velocity
            )

            potential_energy = (
                0.5
                *
                spring_k
                *
                position
                *
                position
            )

            total_energy = (
                kinetic_energy
                +
                potential_energy
            )

            # Downsample only for drawing.
            if len(t) > render_points:

                indices = np.linspace(
                    0,
                    len(t) - 1,
                    render_points
                ).astype(np.int32)

                plot_t = t[indices]
                plot_position = position[indices]

            else:

                plot_t = t
                plot_position = position

            # Draw graph once.
            self.ax.clear()

            self.ax.plot(
                plot_t,
                plot_position,
                linewidth=1.2
            )

            self.ax.set_title(
                "Harmonic Oscillator — Position"
            )

            self.ax.set_xlabel(
                "Time (s)"
            )

            self.ax.set_ylabel(
                "Position (m)"
            )

            self.ax.grid(
                True,
                alpha=0.25
            )

            self.figure.tight_layout()

            self.canvas.draw_idle()

            # Store data
            self.time_data = t
            self.position_data = position

            # Results
            period = (
                2
                *
                math.pi
                /
                omega
            )

            initial_energy = total_energy[0]

            energy_error = (
                np.max(
                    np.abs(
                        total_energy
                        -
                        initial_energy
                    )
                )
                /
                max(
                    abs(initial_energy),
                    1e-30
                )
            )

            elapsed = (
                time.perf_counter()
                -
                start_time
            )

            self.set_info(
                f"Simulation completed in "
                f"{elapsed:.4f} seconds\n\n"

                f"Angular frequency: "
                f"{omega:.6f} rad/s\n"

                f"Period: "
                f"{period:.6f} s\n"

                f"Initial energy: "
                f"{initial_energy:.8g} J\n"

                f"Relative energy variation: "
                f"{energy_error:.3e}\n\n"

                f"Calculated points: "
                f"{len(t):,}\n"

                f"Rendered points: "
                f"{len(plot_t):,}"
            )

            self.status.set(
                "Simulation completed."
            )

        except Exception as error:

            messagebox.showerror(
                "Simulation Error",
                str(error)
            )

            self.status.set(
                "Simulation error."
            )

    # ---------------------------------------------------------
    # FFT
    # ---------------------------------------------------------

    def run_fft(self):

        if (
            self.time_data is None
            or
            self.position_data is None
        ):

            messagebox.showinfo(
                "FFT",
                "Run a simulation first."
            )

            return

        start_time = time.perf_counter()

        signal = (
            self.position_data
            -
            np.mean(
                self.position_data
            )
        )

        dt = (
            self.time_data[1]
            -
            self.time_data[0]
        )

        fft_values = np.fft.rfft(
            signal
        )

        frequencies = np.fft.rfftfreq(
            len(signal),
            d=dt
        )

        amplitudes = np.abs(
            fft_values
        )

        if len(amplitudes) > 1:

            peak_index = (
                np.argmax(
                    amplitudes[1:]
                )
                +
                1
            )

        else:

            peak_index = 0

        dominant_frequency = (
            frequencies[peak_index]
        )

        elapsed = (
            time.perf_counter()
            -
            start_time
        )

        # Limit number of displayed FFT points.
        display_limit = min(
            len(frequencies),
            1500
        )

        self.ax.clear()

        self.ax.plot(
            frequencies[:display_limit],
            amplitudes[:display_limit],
            linewidth=1.2
        )

        self.ax.set_title(
            "FFT — Frequency Spectrum"
        )

        self.ax.set_xlabel(
            "Frequency (Hz)"
        )

        self.ax.set_ylabel(
            "Amplitude"
        )

        self.ax.grid(
            True,
            alpha=0.25
        )

        self.figure.tight_layout()

        self.canvas.draw_idle()

        self.set_info(
            f"FFT completed in "
            f"{elapsed:.4f} seconds\n\n"

            f"Dominant frequency: "
            f"{dominant_frequency:.6f} Hz\n"

            f"FFT points: "
            f"{len(frequencies):,}"
        )

        self.status.set(
            "FFT analysis completed."
        )

    # ---------------------------------------------------------
    # CSV
    # ---------------------------------------------------------

    def save_csv(self):

        if (
            self.time_data is None
            or
            self.position_data is None
        ):

            messagebox.showinfo(
                "Save CSV",
                "Run a simulation first."
            )

            return

        filename = filedialog.asksaveasfilename(
            title="Save simulation data",
            defaultextension=".csv",
            filetypes=[
                ("CSV files", "*.csv")
            ]
        )

        if not filename:
            return

        try:

            with open(
                filename,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(
                    file
                )

                writer.writerow(
                    [
                        "time_s",
                        "position_m"
                    ]
                )

                for t, x in zip(
                    self.time_data,
                    self.position_data
                ):

                    writer.writerow(
                        [
                            f"{t:.12g}",
                            f"{x:.12g}"
                        ]
                    )

            self.status.set(
                "CSV saved successfully."
            )

        except Exception as error:

            messagebox.showerror(
                "Save Error",
                str(error)
            )

    # ---------------------------------------------------------
    # CALCULATOR
    # ---------------------------------------------------------

    def build_calculator(self):

        frame = ttk.Frame(
            self.calculator_tab
        )

        frame.pack(
            fill="both",
            expand=True
        )

        ttk.Label(
            frame,
            text="Scientific Calculator",
            style="Section.TLabel"
        ).pack(
            anchor="w"
        )

        ttk.Label(
            frame,
            text=(
                "Enter a mathematical expression."
            )
        ).pack(
            anchor="w",
            pady=(5, 10)
        )

        self.calculator_entry = ttk.Entry(
            frame,
            font=("Consolas", 13)
        )

        self.calculator_entry.pack(
            fill="x"
        )

        self.calculator_entry.insert(
            0,
            "sin(pi / 4) + sqrt(25)"
        )

        ttk.Button(
            frame,
            text="Calculate",
            command=self.calculate
        ).pack(
            anchor="w",
            pady=10
        )

        self.calculator_result = tk.StringVar(
            value="Result:"
        )

        ttk.Label(
            frame,
            textvariable=self.calculator_result,
            font=("Segoe UI", 14, "bold")
        ).pack(
            anchor="w",
            pady=10
        )

        ttk.Label(
            frame,
            text=(
                "Functions: "
                "sin, cos, tan, asin, acos, atan, "
                "sqrt, log, log10, exp, abs, pi, e"
            ),
            wraplength=850
        ).pack(
            anchor="w"
        )

        self.calculator_entry.bind(
            "<Return>",
            lambda event: self.calculate()
        )

    def calculate(self):

        expression = (
            self.calculator_entry
            .get()
            .strip()
        )

        functions = {

            "sin": np.sin,
            "cos": np.cos,
            "tan": np.tan,

            "asin": np.arcsin,
            "acos": np.arccos,
            "atan": np.arctan,

            "sqrt": np.sqrt,

            "log": np.log,
            "log10": np.log10,

            "exp": np.exp,

            "abs": abs,

            "pi": np.pi,
            "e": np.e
        }

        try:

            result = eval(
                expression,
                {
                    "__builtins__": {}
                },
                functions
            )

            if isinstance(
                result,
                np.ndarray
            ):

                result = np.array2string(
                    result,
                    precision=8,
                    threshold=30
                )

            self.calculator_result.set(
                f"Result: {result}"
            )

        except Exception as error:

            self.calculator_result.set(
                f"Error: {error}"
            )

    # ---------------------------------------------------------
    # SYSTEM
    # ---------------------------------------------------------

    def build_system(self):

        text = (
            "AXIOM Scientific Software V2\n\n"

            "Performance target:\n"
            "Low-power computers such as Intel Celeron systems.\n\n"

            "Optimizations:\n"
            "• No continuous animation\n"
            "• Graphs are drawn only when necessary\n"
            "• NumPy vectorized calculations\n"
            "• Graph downsampling\n"
            "• Lite performance mode\n"
            "• FFT runs only when requested\n"
            "• No unnecessary background calculations\n\n"

            "Scientific model:\n"
            "m × x'' + k × x = 0\n\n"

            "This V2 is designed as a foundation for future AXIOM\n"
            "scientific simulation and analysis tools."
        )

        ttk.Label(
            self.system_tab,
            text=text,
            justify="left",
            font=("Segoe UI", 11)
        ).pack(
            anchor="nw"
        )

    # ---------------------------------------------------------
    # INFO
    # ---------------------------------------------------------

    def set_info(self, text):

        self.info.configure(
            state="normal"
        )

        self.info.delete(
            "1.0",
            "end"
        )

        self.info.insert(
            "1.0",
            text
        )

        self.info.configure(
            state="disabled"
        )


def main():

    root = tk.Tk()

    app = AxiomScientificV2(
        root
    )

    root.mainloop()


if __name__ == "__main__":
    main()
