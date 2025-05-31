import importlib
from config import settings

class ModeManager:
    def __init__(self):
        self.current_mode = None
        self.mode_module = None

    def switch_mode(self, mode_name):
        if mode_name not in settings.MODES:
            print(f"Mode '{mode_name}' not found.")
            return
        if self.current_mode == mode_name:
            print(f"Already in mode: {mode_name}")
            return

        module_name = f"modes.{settings.MODES[mode_name]}"
        try:
            # Dynamically import mode module
            self.mode_module = importlib.import_module(module_name)
            self.current_mode = mode_name
            print(f"Switched to mode: {mode_name}")
            self.mode_module.run()
        except Exception as e:
            print(f"Failed to load mode '{mode_name}': {e}")

    def run_current_mode(self):
        if self.mode_module and hasattr(self.mode_module, "run"):
            self.mode_module.run()
