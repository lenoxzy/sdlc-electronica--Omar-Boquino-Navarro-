#importando las clases de mi archivo solid_isp_dip.py
from solid_isp_dip import InMemoryRepository, DataProcessor, SensorReading
def test_de_guardado_de_lectura():
   # base de datos simulada y se la inyectamos al procesador
    repo_falso = InMemoryRepository()
    procesador = DataProcessor(repository=repo_falso)
    
    # se crea un dato de prueba (usando una placa típica como ejemplo)
    lectura_prueba = SensorReading(sensor_id="ESP32_01", value=25.5)
    
    # 2. ACTUAR (Act)
    # Ejecutamos el método que queremos probar
    procesador.process_and_save(lectura_prueba)
    
    # 3. VERIFICAR (Assert)
    # Comprobamos directamente en nuestro repositorio falso si el dato se guardó bien
    lectura_guardada = repo_falso.get_latest("ESP32_01")
    
    # Verificamos que el dato exista
    assert lectura_guardada is not None, "El procesador no guardó la lectura"
    # Verificamos que el valor sea el correcto
    assert lectura_guardada.value == 25.5, "El valor guardado no coincide"
    assert lectura_guardada.sensor_id == "ESP32_01", "El ID del sensor no coincide"
