#!/usr/bin/env python3
"""Build standalone executable for FileComparison Tool."""
import subprocess
import sys
import platform


def main():
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("PyInstaller not found. Install it with: pip install pyinstaller")
        sys.exit(1)

    cmd = [sys.executable, "-m", "PyInstaller", "FileComparison.spec", "--noconfirm"]
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

    system = platform.system()
    if system == "Darwin":
        print("\nBuild complete! App bundle at: dist/FileComparison Tool.app")
    elif system == "Windows":
        print("\nBuild complete! Executable at: dist/FileComparison Tool.exe")
    else:
        print("\nBuild complete! Executable at: dist/FileComparison Tool")


if __name__ == "__main__":
    main()
