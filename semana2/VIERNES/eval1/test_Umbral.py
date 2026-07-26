# Test US-02: Umbral de Temperatura
def test_anomaly_detector_temp_exceeds_threshold():
    mock_alert = MockAlert()
    # Inyectamos el umbral (NO hardcodeado) y la estrategia de alerta
    detector = AnomalyDetector(alert_strategy=mock_alert, temp_threshold=35.0, hum_threshold=80.0)
    reading = SensorReading("S1", 36.0, "temperature")

    detector.check(reading)