import subprocess, sys
script = r"C:\PROJECTS\CHAT\marker_pdf_converter\gradio_config_ui.py"
out = open(r"C:\PROJECTS\CHAT\ui_output.txt", "w", encoding="utf-8")
DETACH = 0x00000008
proc = subprocess.Popen(
    [sys.executable, "-u", script],
    stdout=out, stderr=subprocess.STDOUT,
    creationflags=DETACH,
)
print("Launched UI, PID:", proc.pid)
