from pynput.keyboard import Key, Listener
from datetime import datetime
import time

kaes = ""
tapping = []

def show_line(t, chunk):
    stamp = datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')
    line = f"{stamp} → {''.join(chunk)}"
    print(line)

def print_chunks():
    print("\n📋 הקשות לפי זמן (כל 5 שניות):\n")

    chunk = []
    chunk_time = None

    if tapping:
        last_time = tapping[0][0]
    else:
        last_time = time.time()

    for t, c in tapping:
        if t - last_time < 5:
            if chunk_time is None:
                chunk_time = t
            chunk.append(c)
        else:
            show_line(chunk_time, chunk)
            chunk = [c]
            chunk_time = t
            last_time = t

    if chunk:
        show_line(chunk_time, chunk)

    print("\n--- סוף ---\n")

def on_press(key):
    global kaes
    try:
        k = key.char
    except:
        k = str(key)

    kaes += k
    tapping.append((time.time(), k))

    print(f"[DEBUG] kaes עכשיו: '{kaes}'")  # מדפיס את התוכן של kaes בכל לחיצה

    if "show" in kaes:
        print("[DEBUG] זוהתה פקודת SHOW!")   # מודיע שזוהתה המילה show
        print_chunks()
        kaes = ""  # מאפס את kaes אחרי ההדפסה

def on_release(key):
    if key == Key.esc:
        print("[DEBUG] יציאה מהאזנה")
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()