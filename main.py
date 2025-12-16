#!/usr/bin/env python3
import os
import sys

from src.chat_bot import bot

LOCK_FILE = "/tmp/promohunter_bot.lock"

def acquire_lock():
    if os.path.exists(LOCK_FILE):
        try:
            with open(LOCK_FILE, 'r') as f:
                old_pid_str = f.read().strip()
            if old_pid_str.isdigit():
                old_pid = int(old_pid_str)
                try:
                    os.kill(old_pid, 0)
                    print(f"❌ Bot already running with PID {old_pid}")
                    sys.exit(1)
                except OSError:
                    pass
        except:
            pass
    
    with open(LOCK_FILE, 'w') as f:
        f.write(str(os.getpid()))

def release_lock():
    try:
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)
    except:
        pass

if __name__ == "__main__":
    acquire_lock()
    try:
        bot.remove_webhook()
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except KeyboardInterrupt:
        pass
    finally:
        release_lock()
