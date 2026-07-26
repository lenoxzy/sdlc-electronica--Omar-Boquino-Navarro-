import pytest
from pathlib import Path
from US_4 import FileAlert
#Test US-04: Estrategia de Archivo (FileAlert)
def test_file_alert_writes_to_file(tmp_path: Path):
    # tmp_path es una magia de pytest que crea una carpeta temporal
    log_file = tmp_path / "alerts.log"
    alert = FileAlert(filepath=str(log_file))
    
    alert.send_alert("Prueba de alerta")
    
    content = log_file.read_text()
    assert "[FILE ALERT] Prueba de alerta" in content