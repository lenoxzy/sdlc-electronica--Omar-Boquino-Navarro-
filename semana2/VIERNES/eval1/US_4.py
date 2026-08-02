# --- Implementaciones Concretas de la Alerta ---
class ConsoleAlert:
    def send_alert(self, message: str) -> None:
        print(f"[CONSOLE ALERT] {message}")


class FileAlert:
    def __init__(self, filepath: str):
        self._filepath = filepath

    def send_alert(self, message: str) -> None:
        with open(self._filepath, "a", encoding="utf-8") as f:
            f.write(f"[FILE ALERT] {message}\n")
