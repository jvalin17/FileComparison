import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog

from file_checker import compare_files_detailed, compare_directories


SPEED_OPTIONS = {
    "Tiny (precise, slower)": 64,
    "Small": 1024,
    "Standard": 8192,
    "Large (fast, more memory)": 65536,
}
DEFAULT_SPEED = "Standard"


class FileCompareGUI:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("FileComparison Tool")
        self.window.minsize(600, 500)
        self.window.resizable(True, True)

        self.compare_mode = tk.StringVar(value="files")
        self.selected_speed = tk.StringVar(value=DEFAULT_SPEED)

        self._build_layout()
        self._setup_keyboard_shortcuts()

    def _build_layout(self):
        spacing = {"padx": 10, "pady": 5}

        # -- Mode selector (files or directories) --
        mode_section = ttk.LabelFrame(self.window, text="Mode")
        mode_section.pack(fill="x", **spacing)

        ttk.Radiobutton(
            mode_section, text="Compare Files", variable=self.compare_mode,
            value="files", command=self._on_mode_change
        ).pack(side="left", padx=15, pady=5)
        ttk.Radiobutton(
            mode_section, text="Compare Directories", variable=self.compare_mode,
            value="dirs", command=self._on_mode_change
        ).pack(side="left", padx=15, pady=5)

        # -- Path inputs with browse buttons --
        path_section = ttk.Frame(self.window)
        path_section.pack(fill="x", **spacing)

        ttk.Label(path_section, text="Path 1:").grid(row=0, column=0, sticky="w", pady=3)
        self.path_1 = tk.StringVar()
        path_1_input = ttk.Entry(path_section, textvariable=self.path_1)
        path_1_input.grid(row=0, column=1, sticky="ew", padx=5, pady=3)
        ttk.Button(path_section, text="Browse", command=lambda: self._browse(1)).grid(row=0, column=2, pady=3)

        ttk.Label(path_section, text="Path 2:").grid(row=1, column=0, sticky="w", pady=3)
        self.path_2 = tk.StringVar()
        path_2_input = ttk.Entry(path_section, textvariable=self.path_2)
        path_2_input.grid(row=1, column=1, sticky="ew", padx=5, pady=3)
        ttk.Button(path_section, text="Browse", command=lambda: self._browse(2)).grid(row=1, column=2, pady=3)

        path_section.columnconfigure(1, weight=1)

        # -- Speed option --
        options_section = ttk.LabelFrame(self.window, text="Options")
        options_section.pack(fill="x", **spacing)

        ttk.Label(options_section, text="Speed:").pack(side="left", padx=(10, 5), pady=5)
        self.speed_dropdown = ttk.Combobox(
            options_section, textvariable=self.selected_speed,
            values=list(SPEED_OPTIONS.keys()),
            state="readonly", width=24
        )
        self.speed_dropdown.pack(side="left", pady=5)

        # -- Compare and Clear buttons --
        button_section = ttk.Frame(self.window)
        button_section.pack(fill="x", **spacing)

        self.compare_button = ttk.Button(button_section, text="Compare", command=self._on_compare)
        self.compare_button.pack(side="left", padx=5)

        self.clear_button = ttk.Button(button_section, text="Clear", command=self._clear_results)
        self.clear_button.pack(side="left", padx=5)

        # -- Loading bar (pulsing animation during comparison) --
        self.loading_bar = ttk.Progressbar(self.window, mode="indeterminate")
        self.loading_bar.pack(fill="x", padx=10, pady=(0, 5))

        # -- Results display (scrollable, read-only) --
        results_section = ttk.LabelFrame(self.window, text="Results")
        results_section.pack(fill="both", expand=True, **spacing)

        self.results_display = tk.Text(results_section, wrap="word", state="disabled", height=12)
        results_scrollbar = ttk.Scrollbar(results_section, orient="vertical", command=self.results_display.yview)
        self.results_display.configure(yscrollcommand=results_scrollbar.set)
        self.results_display.pack(side="left", fill="both", expand=True)
        results_scrollbar.pack(side="right", fill="y")

        # Color tags for results text
        self.results_display.tag_configure("match", foreground="green")
        self.results_display.tag_configure("mismatch", foreground="red")
        self.results_display.tag_configure("info", foreground="gray")
        self.results_display.tag_configure("heading", font=("TkDefaultFont", 10, "bold"))

        # -- Status bar at bottom --
        self.status_text = tk.StringVar(value="Ready")
        status_border = tk.Frame(self.window, bd=1, relief="groove")
        status_border.pack(fill="x", side="bottom", padx=10, pady=(0, 5))
        ttk.Label(status_border, textvariable=self.status_text, anchor="w").pack(fill="x", padx=4, pady=2)

    def _setup_keyboard_shortcuts(self):
        self.window.bind("<Return>", lambda event: self._on_compare())
        self.window.bind("<Control-l>", lambda event: self._clear_results())

    def _on_mode_change(self):
        self._clear_results()
        self.path_1.set("")
        self.path_2.set("")

    def _browse(self, which):
        if self.compare_mode.get() == "files":
            path = filedialog.askopenfilename(title=f"Select File {which}")
        else:
            path = filedialog.askdirectory(title=f"Select Directory {which}")

        if path:
            if which == 1:
                self.path_1.set(path)
            else:
                self.path_2.set(path)

    def _on_compare(self):
        path_1 = self.path_1.get().strip()
        path_2 = self.path_2.get().strip()

        if not path_1 or not path_2:
            self._show_message("Please select both paths.", "mismatch")
            return

        if self.compare_mode.get() == "files":
            if not os.path.isfile(path_1):
                self._show_message(f"Path 1 is not a valid file:\n{path_1}", "mismatch")
                return
            if not os.path.isfile(path_2):
                self._show_message(f"Path 2 is not a valid file:\n{path_2}", "mismatch")
                return
        else:
            if not os.path.isdir(path_1):
                self._show_message(f"Path 1 is not a valid directory:\n{path_1}", "mismatch")
                return
            if not os.path.isdir(path_2):
                self._show_message(f"Path 2 is not a valid directory:\n{path_2}", "mismatch")
                return

        chunk_size = SPEED_OPTIONS[self.selected_speed.get()]

        self.compare_button.configure(state="disabled")
        self.status_text.set("Comparing...")
        self._clear_results()
        self.loading_bar.start(15)

        background_task = threading.Thread(
            target=self._run_comparison,
            args=(path_1, path_2, chunk_size),
            daemon=True
        )
        background_task.start()

    def _run_comparison(self, path_1, path_2, chunk_size):
        try:
            if self.compare_mode.get() == "files":
                result = compare_files_detailed(path_1, path_2, chunk_size)
                self.window.after(0, self._display_file_result, path_1, path_2, result)
            else:
                result = compare_directories(path_1, path_2, chunk_size)
                self.window.after(0, self._display_directory_result, path_1, path_2, result)
        except Exception as e:
            self.window.after(0, self._show_message, f"Error: {e}", "mismatch")
        finally:
            self.window.after(0, self._on_comparison_done)

    def _on_comparison_done(self):
        self.loading_bar.stop()
        self.compare_button.configure(state="normal")
        self.status_text.set("Done")

    def _display_file_result(self, path_1, path_2, result):
        file_1_size = os.path.getsize(path_1) if os.path.exists(path_1) else "N/A"
        file_2_size = os.path.getsize(path_2) if os.path.exists(path_2) else "N/A"

        color = "match" if result["match"] else "mismatch"
        status = "IDENTICAL" if result["match"] else "DIFFERENT"

        output = []
        output.append((f"{status}\n\n", color))

        output.append(("Reason: ", "heading"))
        output.append((f"{result['reason']}\n\n", color))

        if result["first_diff_offset"] is not None:
            output.append(("First difference at byte: ", "heading"))
            output.append((f"{result['first_diff_offset']:,}\n\n", "mismatch"))

        output.append(("File 1: ", "heading"))
        output.append((f"{path_1}\n", "info"))
        if isinstance(file_1_size, int):
            output.append((f"  Size: {file_1_size:,} bytes\n\n", "info"))

        output.append(("File 2: ", "heading"))
        output.append((f"{path_2}\n", "info"))
        if isinstance(file_2_size, int):
            output.append((f"  Size: {file_2_size:,} bytes\n", "info"))

        self._display_output(output)

    def _display_directory_result(self, path_1, path_2, result):
        matching_files = result["matching"]
        differing_files = result["differing"]
        only_in_first = result["only_in_first"]
        only_in_second = result["only_in_second"]

        total_files = len(matching_files) + len(differing_files) + len(only_in_first) + len(only_in_second)

        output = []
        output.append(("Directory Comparison\n\n", "heading"))

        output.append(("Dir 1: ", "heading"))
        output.append((f"{path_1}\n", "info"))
        output.append(("Dir 2: ", "heading"))
        output.append((f"{path_2}\n\n", "info"))

        output.append((f"Total files found: {total_files}\n\n", "info"))

        output.append((f"Matching ({len(matching_files)}):\n", "match"))
        if matching_files:
            for file_name in matching_files:
                output.append((f"  {file_name}\n", "match"))
        else:
            output.append(("  (none)\n", "info"))

        output.append((f"\nDiffering ({len(differing_files)}):\n", "mismatch"))
        if differing_files:
            for file_name in differing_files:
                output.append((f"  {file_name}\n", "mismatch"))
        else:
            output.append(("  (none)\n", "info"))

        output.append((f"\nOnly in Dir 1 ({len(only_in_first)}):\n", "mismatch"))
        if only_in_first:
            for file_name in only_in_first:
                output.append((f"  {file_name}\n", "mismatch"))
        else:
            output.append(("  (none)\n", "info"))

        output.append((f"\nOnly in Dir 2 ({len(only_in_second)}):\n", "mismatch"))
        if only_in_second:
            for file_name in only_in_second:
                output.append((f"  {file_name}\n", "mismatch"))
        else:
            output.append(("  (none)\n", "info"))

        self._display_output(output)

    def _show_message(self, text, color="info"):
        self._display_output([(text, color)])

    def _display_output(self, output_lines):
        self.results_display.configure(state="normal")
        self.results_display.delete("1.0", "end")
        for text, color in output_lines:
            self.results_display.insert("end", text, color)
        self.results_display.configure(state="disabled")

    def _clear_results(self):
        self.results_display.configure(state="normal")
        self.results_display.delete("1.0", "end")
        self.results_display.configure(state="disabled")
        self.status_text.set("Ready")

    def run(self):
        self.window.mainloop()
