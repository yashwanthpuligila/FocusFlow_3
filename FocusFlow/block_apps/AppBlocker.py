import psutil
import subprocess
import time
import os
import threading
import signal
import sys
from pathlib import Path

# Read blocklist file next to this script to avoid absolute-path issues
BLOCKLIST_FILE = Path(__file__).with_name("blocklist.txt")

class AppBlocker:
    def __init__(self):
        # use a set for fast lookups and to avoid duplicates
        self.blocked_apps = set()
        self.is_blocking = False
        self.block_thread = None

    # Read and normalize the blocklist file
    def _read_blocklist(self):
        try:
            if not BLOCKLIST_FILE.exists():
                BLOCKLIST_FILE.write_text(
                    "# Put one process name per line, e.g. chrome.exe\n"
                    "# Social Media & Entertainment\n"
                    "chrome.exe\n"
                    "firefox.exe\n"
                    "msedge.exe\n"
                    "discord.exe\n"
                    "# Games\n"
                    "steam.exe\n"
                    "# Add your specific apps here\n",
                    encoding="utf-8"
                )
                print(f"[AppBlocker] Created default blocklist at {BLOCKLIST_FILE}")
                return set()
            
            items = set()
            for line in BLOCKLIST_FILE.read_text(encoding="utf-8").splitlines():
                s = line.split("#", 1)[0].strip().lower()
                if s:
                    items.add(s)
            return items
        except Exception as e:
            print(f"[AppBlocker] Error reading blocklist: {e}")
            return set()

    # Sync in-memory list from file (called every loop)
    def sync_from_file(self):
        items = self._read_blocklist()
        if items != self.blocked_apps:
            self.blocked_apps = items
            print(f"[AppBlocker] Loaded {len(items)} apps from {BLOCKLIST_FILE.name}")
            if items:
                print(f"[AppBlocker] Blocking: {', '.join(sorted(items))}")

    def add_to_blacklist(self, app_names):
        """Add apps to blacklist - can be process names or executable names"""
        if isinstance(app_names, str):
            app_names = [app_names]
        new_apps = {a.lower().strip() for a in app_names}
        self.blocked_apps |= new_apps
        print(f"[AppBlocker] Added to blocklist: {', '.join(new_apps)}")

    def remove_from_blacklist(self, app_name):
        """Remove app from blacklist"""
        app_name = app_name.lower().strip()
        self.blocked_apps.discard(app_name)
        print(f"[AppBlocker] Removed from blocklist: {app_name}")

    def stop_blocking(self):
        """Stop the blocking loop and join the worker thread."""
        print("[AppBlocker] Stopping blocker...")
        self.is_blocking = False
        if self.block_thread and self.block_thread.is_alive():
            try:
                self.block_thread.join(timeout=3)
                print("[AppBlocker] Blocker stopped successfully")
            except Exception as e:
                print(f"[AppBlocker] Error stopping blocker thread: {e}")

    # METHOD 1: Process Termination (Most effective)
    def kill_blocked_processes(self):
        """Continuously kill blocked processes"""
        if not self.blocked_apps:
            return []

        killed_apps = []
        # System processes that should NEVER be killed
        EXEMPT = {
            "system", "idle", "services.exe", "smss.exe", "lsass.exe", "csrss.exe",
            "wininit.exe", "winlogon.exe", "svchost.exe", "fontdrvhost.exe", "registry",
            "explorer.exe", "dwm.exe", "python.exe", "pythonw.exe", "conhost.exe",
            "taskmgr.exe", "taskhost.exe", "spoolsv.exe", "audiodg.exe", "cmd.exe",
            "powershell.exe", "rundll32.exe", "dllhost.exe", "wmiprvse.exe"
        }

        try:
            for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
                try:
                    process_name = (proc.info['name'] or "").lower()
                    exe_path = (proc.info['exe'] or "").lower()
                    
                    # Skip if no process name or if it's an exempt system process
                    if not process_name or process_name in EXEMPT:
                        continue

                    # Check if this process should be blocked
                    should_block = False
                    
                    # Check direct process name match
                    if process_name in self.blocked_apps:
                        should_block = True
                    
                    # Check if any blocked app name is in the executable path
                    elif exe_path and any(blocked_app in exe_path for blocked_app in self.blocked_apps):
                        should_block = True
                    
                    # Also check command line for browser tabs/processes
                    elif proc.info.get('cmdline'):
                        cmdline_str = ' '.join(proc.info['cmdline']).lower()
                        if any(blocked_app in cmdline_str for blocked_app in self.blocked_apps):
                            should_block = True

                    if should_block:
                        try:
                            print(f"[AppBlocker] Terminating: {process_name} (PID: {proc.info['pid']})")
                            proc.terminate()
                            killed_apps.append(process_name)
                            
                            # Give process 3 seconds to terminate gracefully
                            try:
                                proc.wait(timeout=3)
                            except psutil.TimeoutExpired:
                                print(f"[AppBlocker] Force killing: {process_name} (PID: {proc.info['pid']})")
                                proc.kill()
                                proc.wait(timeout=2)
                                
                        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                            # Process already terminated or access denied
                            pass
                        except Exception as e:
                            print(f"[AppBlocker] Error terminating {process_name}: {e}")

                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    # Process disappeared or access denied - skip it
                    continue
                except Exception as e:
                    print(f"[AppBlocker] Error processing process: {e}")
                    continue

        except Exception as e:
            print(f"[AppBlocker] Error in kill_blocked_processes: {e}")
            
        return killed_apps

    # METHOD 2: File Renaming (Additional protection)
    def rename_executables(self, block=True):
        """Temporarily rename executable files to block them"""
        if not self.blocked_apps:
            return

        # Common installation paths
        common_paths = []
        
        # Windows paths
        if os.name == 'nt':
            common_paths.extend([
                "C:\\Program Files\\",
                "C:\\Program Files (x86)\\",
                os.path.expanduser("~/AppData/Local/"),
                os.path.expanduser("~/AppData/Roaming/"),
            ])
        # macOS paths
        elif sys.platform == 'darwin':
            common_paths.extend([
                "/Applications/",
                os.path.expanduser("~/Applications/"),
            ])
        # Linux paths
        else:
            common_paths.extend([
                "/usr/bin/",
                "/usr/local/bin/",
                "/opt/",
                os.path.expanduser("~/bin/"),
            ])
        
        for blocked_app in self.blocked_apps:
            for base_path in common_paths:
                if os.path.exists(base_path):
                    try:
                        for root, dirs, files in os.walk(base_path):
                            for file in files:
                                file_lower = file.lower()
                                if (blocked_app in file_lower and 
                                    (file_lower.endswith('.exe') or 
                                     file_lower.endswith('.app') or
                                     os.access(os.path.join(root, file), os.X_OK))):
                                    
                                    original_path = os.path.join(root, file)
                                    
                                    if block:
                                        blocked_path = original_path + '.blocked'
                                        try:
                                            if not os.path.exists(blocked_path):
                                                os.rename(original_path, blocked_path)
                                                print(f"[AppBlocker] Blocked executable: {file}")
                                        except (PermissionError, FileNotFoundError, OSError):
                                            pass  # Skip files we can't modify
                                    else:
                                        # Unblock by renaming back
                                        if original_path.endswith('.blocked'):
                                            try:
                                                unblocked_path = original_path[:-8]  # Remove '.blocked'
                                                if not os.path.exists(unblocked_path):
                                                    os.rename(original_path, unblocked_path)
                                                    print(f"[AppBlocker] Unblocked executable: {file}")
                                            except (PermissionError, FileNotFoundError, OSError):
                                                pass
                    except (PermissionError, OSError):
                        # Skip directories we can't access
                        continue

    # METHOD 3: Registry/Startup Blocking (Windows only)
    def block_via_registry(self, block=True):
        """Block apps from starting via registry (Windows only) - Requires admin privileges"""
        if os.name != 'nt':
            return

        try:
            import winreg
            
            # Access the Image File Execution Options registry key
            reg_path = r"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options"
            
            for blocked_app in self.blocked_apps:
                if not blocked_app.endswith('.exe'):
                    continue  # Skip non-executable entries
                    
                app_key = f"{reg_path}\\{blocked_app}"
                
                if block:
                    try:
                        key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, app_key)
                        winreg.SetValueEx(key, "Debugger", 0, winreg.REG_SZ, "nonexistent.exe")
                        winreg.CloseKey(key)
                        print(f"[AppBlocker] Registry blocked: {blocked_app}")
                    except (PermissionError, OSError):
                        print(f"[AppBlocker] Need admin privileges for registry modification of {blocked_app}")
                else:
                    try:
                        winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, app_key)
                        print(f"[AppBlocker] Registry unblocked: {blocked_app}")
                    except (FileNotFoundError, PermissionError, OSError):
                        pass  # Key doesn't exist or permission denied
                        
        except ImportError:
            print("[AppBlocker] Registry method only works on Windows")
        except Exception as e:
            print(f"[AppBlocker] Registry error: {e}")

    # METHOD 4: Continuous Monitoring and Blocking
    def start_blocking(self, duration_minutes=None, use_registry=False, use_file_rename=False):
        """Start the blocking process in a separate thread"""
        if self.is_blocking:
            print("[AppBlocker] Blocker is already running")
            return

        print(f"[AppBlocker] Starting blocker (reading from {BLOCKLIST_FILE})")
        self.is_blocking = True

        # Apply additional blocking methods if requested
        if use_registry:
            print("[AppBlocker] Applying registry blocks...")
            self.block_via_registry(block=True)
            
        if use_file_rename:
            print("[AppBlocker] Renaming executables...")
            self.rename_executables(block=True)

        def blocking_loop():
            start_time = time.time()
            last_sync = 0
            
            while self.is_blocking:
                try:
                    current_time = time.time()
                    
                    # Reload blocklist from file every 10 seconds
                    if current_time - last_sync > 10:
                        self.sync_from_file()
                        last_sync = current_time
                    
                    # Kill blocked processes
                    killed = self.kill_blocked_processes()
                    
                    # Check if duration limit reached
                    if duration_minutes and (current_time - start_time) > (duration_minutes * 60):
                        print(f"[AppBlocker] Duration limit ({duration_minutes} minutes) reached")
                        self.stop_blocking()
                        break
                    
                    # Sleep for 1 second before next check
                    time.sleep(1)
                    
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"[AppBlocker] Error in blocking loop: {e}")
                    time.sleep(5)  # Wait longer on error

            # Cleanup when stopping
            try:
                if use_registry:
                    print("[AppBlocker] Removing registry blocks...")
                    self.block_via_registry(block=False)
                    
                if use_file_rename:
                    print("[AppBlocker] Restoring renamed executables...")
                    self.rename_executables(block=False)
            except Exception as e:
                print(f"[AppBlocker] Error during cleanup: {e}")

        self.block_thread = threading.Thread(target=blocking_loop, daemon=True)
        self.block_thread.start()
        print("[AppBlocker] Blocking thread started")

def signal_handler(signum, frame):
    """Handle graceful shutdown on SIGINT/SIGTERM"""
    global blocker
    print(f"\n[AppBlocker] Received signal {signum}, shutting down gracefully...")
    if blocker:
        blocker.stop_blocking()
    print("[AppBlocker] Shutdown complete")
    sys.exit(0)

# Global blocker instance
blocker = None

# Main execution
if __name__ == "__main__":
    print("[AppBlocker] Starting App Blocker...")
    print(f"[AppBlocker] Python version: {sys.version}")
    print(f"[AppBlocker] Platform: {sys.platform}")
    print(f"[AppBlocker] Blocklist file: {BLOCKLIST_FILE}")
    
    blocker = AppBlocker()
    
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    if hasattr(signal, 'SIGTERM'):
        signal.signal(signal.SIGTERM, signal_handler)
    
    # Parse command line arguments for additional features
    use_registry = '--registry' in sys.argv
    use_file_rename = '--rename' in sys.argv
    duration = None
    
    for arg in sys.argv:
        if arg.startswith('--duration='):
            try:
                duration = int(arg.split('=')[1])
            except ValueError:
                print("[AppBlocker] Invalid duration format. Use --duration=MINUTES")
    
    # Start blocking with specified options
    blocker.start_blocking(
        duration_minutes=duration,
        use_registry=use_registry,
        use_file_rename=use_file_rename
    )
    
    try:
        # Keep the main thread alive
        while blocker.is_blocking:
            time.sleep(1)
        print("[AppBlocker] Blocking finished")
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)
    except Exception as e:
        print(f"[AppBlocker] Unexpected error: {e}")
        if blocker:
            blocker.stop_blocking()
    finally:
        print("[AppBlocker] Exiting...")