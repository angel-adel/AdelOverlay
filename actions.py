import os
import subprocess

def run_shortcut(shortcut: dict):
    target = shortcut.get("target", "")
    t_type = shortcut.get("type", "")
    
    try:
        if t_type in ("file", "folder"):
            if os.path.exists(target):
                os.startfile(target)
        elif t_type == "command":
            subprocess.Popen(target, shell=True)
    except Exception as e:
        print(f"Ошибка запуска {target}: {e}")