import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog

from file_checker import compare_files, compare_files_detailed, compare_directories


CHUNK_SIZES = [64, 1024, 8192, 65536]
DEFAULT_CHUNK_INDEX = 2  # 8192


class FileCompareGUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FileComparison Tool")
        self.root.minsize(600, 500)
        self.root.resizable(True, True)

        self.mode = tk.StringVar(value="files")
        self.detailed = tk.BooleanVar(value=False)
        self.chunk_var = tk.StringVar(value=str(CHUNK_SIZES[DEFAULT_CHUNK_INDEX]))

        self._build_ui()
        self._bind_keys()

    def _build_ui(self):
        pad = {"padx": 10, "pady": 5}

        # -- Mode selector --
        mode_frame = ttk.LabelFrame(self.root, text="Mode")
        mode_frame.pack(fill="x", **pad)

        ttk.Radiobutton(
            mode_frame, text="Compare Files", variable=self.mode,
            value="files", command=self._on_mode_change
        ).pack(side="left", padx=15, pady=5)
        ttk.Radiobutton(
            mode_frame, text="Compare Directories", variable=self.mode,
            value="dirs", command=self._on_mode_change
        ).pack(side="left", padx=15, pady=5)

        # -- Path inputs --
        path_frame = ttk.Frame(self.root)
        path_frame.pack(fill="x", **pad)

        ttk.Label(path_frame, text="Path 1:").grid(row=0, column=0, sticky="w", pady=3)
        self.path1_var = tk.StringVar()
        self.path1_entry = ttk.Entry(path_frame, textvariable=self.path1_var)
        self.path1_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=3)
        self.browse1_btn = ttk.Button(path_frame, text="Browse", command=lambda: self._browse(1))
        self.browse1_btn.grid(row=0, column=2, pady=3)

        ttk.Label(path_frame, text="Path 2:").grid(row=1, column=0, sticky="w", pady=3)
        self.path2_var = tk.StringVar()
        self.path2_entry = ttk.Entry(path_frame, textvariable=self.path2_var)
        self.path2_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=3)
        self.browse2_btn = ttk.Button(path_frame, text="Browse", command=lambda: self._browse(2))
        self.browse2_btn.grid(row=1, column=2, pady=3)

        path_frame.columnconfigure(1, weight=1)

        # -- Options --
        opts_frame = ttk.LabelFrame(self.root, text="Options")
        opts_frame.pack(fill="x", **pad)

        ttk.Label(opts_frame, text="Chunk Size:").pack(side="left", padx=(10, 5), pady=5)
        self.chunk_combo = ttk.Combobox(
            opts_frame, textvariable=self.chunk_var,
            values=[str(c) for c in CHUNK_SIZES],
            state="readonly", width=8
        )
        self.chunk_combo.pack(side="left", pady=5)

        self.detailed_check = ttk.Checkbutton(
            opts_frame, text="Show detailed results", variable=self.detailed
        )
        self.detailed_check.pack(side="left", padx=20, pady=5)

        # -- Compare button --
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", **pad)

        self.compare_btn = ttk.Button(btn_frame, text="Compare", command=self._on_compare)
        self.compare_btn.pack(side="left", padx=5)

        self.clear_btn = ttk.Button(btn_frame, text="Clear", command=self._clear_results)
        self.clear_btn.pack(side="left", padx=5)

        # -- Results area --
        results_frame = ttk.LabelFrame(self.root, text="Results")
        results_frame.pack(fill="both", expand=True, **pad)

        self.results_text = tk.Text(results_frame, wrap="word", state="disabled", height=12)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        self.results_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.results_text.tag_configure("match", foreground="green")
        self.results_text.tag_configure("mismatch", foreground="red")
        self.results_text.tag_configure("info", foreground="gray")
        self.results_text.tag_configure("heading", font=("TkDefaultFont", 10, "bold"))

        # -- Status bar --
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief="sunken", anchor="w")
        status_bar.pack(fill="x", side="bottom", padx=10, pady=(0, 5))

    def _bind_keys(self):
        self.root.bind("<Return>", lambda e: self._on_compare())
        self.root.bind("<Control-l>", lambda e: self._clear_results())

    def _on_mode_change(self):
        self._clear_results()
        self.path1_var.set("")
        self.path2_var.set("")
        if self.mode.get() == "dirs":
            self.detailed_check.configure(state="disabled")
            self.detailed.set(False)
        else:
            self.detailed_check.configure(state="normal")

    def _browse(self, which):
        if self.mode.get() == "files":
            path = filedialog.askopenfilename(title=f"Select File {which}")
        else:
            path = filedialog.askdirectory(title=f"Select Directory {which}")

        if path:
            if which == 1:
                self.path1_var.set(path)
            else:
                self.path2_var.set(path)

    def _on_compare(self):
        p1 = self.path1_var.get().strip()
        p2 = self.path2_var.get().strip()

        # Validate inputs
        if not p1 or not p2:
            self._show_result("Please select both paths.", "mismatch")
            return

        if self.mode.get() == "files":
            if not os.path.isfile(p1):
                self._show_result(f"Path 1 is not a valid file:\n{p1}", "mismatch")
                return
            if not os.path.isfile(p2):
                self._show_result(f"Path 2 is not a valid file:\n{p2}", "mismatch")
                return
        else:
            if not os.path.isdir(p1):
                self._show_result(f"Path 1 is not a valid directory:\n{p1}", "mismatch")
                return
            if not os.path.isdir(p2):
                self._show_result(f"Path 2 is not a valid directory:\n{p2}", "mismatch")
                return

        chunk_size = int(self.chunk_var.get())

        self.compare_btn.configure(state="disabled")
        self.status_var.set("Comparing...")
        self._clear_results()

        thread = threading.Thread(
            target=self._run_comparison,
            args=(p1, p2, chunk_size),
            daemon=True
        )
        thread.start()

    def _run_comparison(self, p1, p2, chunk_size):
        try:
            if self.mode.get() == "files":
                if self.detailed.get():
                    result = compare_files_detailed(p1, p2, chunk_size)
                    self.root.after(0, self._display_detailed_result, p1, p2, result)
                else:
                    result = compare_files(p1, p2, chunk_size)
                    self.root.after(0, self._display_simple_result, p1, p2, result)
            else:
                result = compare_directories(p1, p2, chunk_size)
                self.root.after(0, self._display_directory_result, p1, p2, result)
        except Exception as e:
            self.root.after(0, self._show_result, f"Error: {e}", "mismatch")
        finally:
            self.root.after(0, self._comparison_done)

    def _comparison_done(self):
        self.compare_btn.configure(state="normal")
        self.status_var.set("Done")

    def _display_simple_result(self, p1, p2, result):
        size1 = os.path.getsize(p1)
        size2 = os.path.getsize(p2)

        lines = []
        if result:
            lines.append(("IDENTICAL\n\n", "match"))
        else:
            lines.append(("DIFFERENT\n\n", "mismatch"))

        lines.append(("File 1: ", "heading"))
        lines.append((f"{p1}\n", "info"))
        lines.append((f"  Size: {size1:,} bytes\n\n", "info"))
        lines.append(("File 2: ", "heading"))
        lines.append((f"{p2}\n", "info"))
        lines.append((f"  Size: {size2:,} bytes\n", "info"))

        self._write_lines(lines)

    def _display_detailed_result(self, p1, p2, result):
        size1 = os.path.getsize(p1) if os.path.exists(p1) else "N/A"
        size2 = os.path.getsize(p2) if os.path.exists(p2) else "N/A"

        tag = "match" if result["match"] else "mismatch"
        status = "IDENTICAL" if result["match"] else "DIFFERENT"

        lines = []
        lines.append((f"{status}\n\n", tag))

        lines.append(("Reason: ", "heading"))
        lines.append((f"{result['reason']}\n\n", tag))

        if result["first_diff_offset"] is not None:
            lines.append(("First difference at byte: ", "heading"))
            lines.append((f"{result['first_diff_offset']:,}\n\n", "mismatch"))

        lines.append(("File 1: ", "heading"))
        lines.append((f"{p1}\n", "info"))
        if isinstance(size1, int):
            lines.append((f"  Size: {size1:,} bytes\n\n", "info"))

        lines.append(("File 2: ", "heading"))
        lines.append((f"{p2}\n", "info"))
        if isinstance(size2, int):
            lines.append((f"  Size: {size2:,} bytes\n", "info"))

        self._write_lines(lines)

    def _display_directory_result(self, p1, p2, result):
        matching = result["matching"]
        differing = result["differing"]
        only1 = result["only_in_first"]
        only2 = result["only_in_second"]

        total = len(matching) + len(differing) + len(only1) + len(only2)

        lines = []
        lines.append(("Directory Comparison\n\n", "heading"))

        lines.append(("Dir 1: ", "heading"))
        lines.append((f"{p1}\n", "info"))
        lines.append(("Dir 2: ", "heading"))
        lines.append((f"{p2}\n\n", "info"))

        lines.append((f"Total files found: {total}\n\n", "info"))

        lines.append((f"Matching ({len(matching)}):\n", "match"))
        if matching:
            for f in matching:
                lines.append((f"  {f}\n", "match"))
        else:
            lines.append(("  (none)\n", "info"))

        lines.append((f"\nDiffering ({len(differing)}):\n", "mismatch"))
        if differing:
            for f in differing:
                lines.append((f"  {f}\n", "mismatch"))
        else:
            lines.append(("  (none)\n", "info"))

        lines.append((f"\nOnly in Dir 1 ({len(only1)}):\n", "mismatch"))
        if only1:
            for f in only1:
                lines.append((f"  {f}\n", "mismatch"))
        else:
            lines.append(("  (none)\n", "info"))

        lines.append((f"\nOnly in Dir 2 ({len(only2)}):\n", "mismatch"))
        if only2:
            for f in only2:
                lines.append((f"  {f}\n", "mismatch"))
        else:
            lines.append(("  (none)\n", "info"))

        self._write_lines(lines)

    def _show_result(self, text, tag="info"):
        self._write_lines([(text, tag)])

    def _write_lines(self, lines):
        self.results_text.configure(state="normal")
        self.results_text.delete("1.0", "end")
        for text, tag in lines:
            self.results_text.insert("end", text, tag)
        self.results_text.configure(state="disabled")

    def _clear_results(self):
        self.results_text.configure(state="normal")
        self.results_text.delete("1.0", "end")
        self.results_text.configure(state="disabled")
        self.status_var.set("Ready")

    def run(self):
        self.root.mainloop()
