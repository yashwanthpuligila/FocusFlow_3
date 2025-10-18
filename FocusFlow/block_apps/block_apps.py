import sys
import time
from pathlib import Path

# Import the AppBlocker implementation from the sibling module
from AppBlocker import AppBlocker, BLOCKLIST_FILE
from mongodb_logger import MongoDBLogger

logger = MongoDBLogger()
session_id = logger.log_session_start(25, 5)

# Flag file to enable/disable blocking
FLAG_FILE = Path(__file__).with_name("block_enabled.txt")

def is_blocking_enabled():
    try:
        return FLAG_FILE.exists() and FLAG_FILE.read_text(encoding="utf-8").strip() == "1"
    except Exception:
        return False

def main():
    """Main wrapper: watch FLAG_FILE and start/stop the AppBlocker accordingly.

    Supports CLI flags:
      --duration=MINUTES   start blocker with a duration when started
      --registry           apply registry-based blocking (Windows only)
      --rename             use executable renaming as an additional block method
      --once               start blocking immediately once (ignore flag file)
    """
    use_registry = '--registry' in sys.argv
    use_file_rename = '--rename' in sys.argv
    run_once = '--once' in sys.argv
    duration = None
    for arg in sys.argv:
        if arg.startswith('--duration='):
            try:
                duration = int(arg.split('=', 1)[1])
            except ValueError:
                print("Invalid duration, ignoring")

    blocker = AppBlocker()

    try:
        if run_once:
            print(f"[block_apps] Starting one-shot blocker (duration={duration})")
            blocker.start_blocking(duration_minutes=duration, use_registry=use_registry, use_file_rename=use_file_rename)
            while blocker.is_blocking:
                time.sleep(1)
            return

        print("[block_apps] Watching flag file for enable/disable (create 'block_enabled.txt' with '1' to enable)")
        print(f"[block_apps] Reading app blocklist from: {BLOCKLIST_FILE}")

        last_enabled = False
        while True:
            try:
                enabled = is_blocking_enabled()
                if enabled and not blocker.is_blocking:
                    print("[block_apps] Flag enabled: starting blocker")
                    blocker.start_blocking(duration_minutes=duration, use_registry=use_registry, use_file_rename=use_file_rename)
                elif not enabled and blocker.is_blocking:
                    print("[block_apps] Flag disabled: stopping blocker")
                    blocker.stop_blocking()
                time.sleep(1)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"[block_apps] Error in main loop: {e}")
                time.sleep(2)

    finally:
        if blocker and blocker.is_blocking:
            blocker.stop_blocking()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("[block_apps] Interrupted by user")