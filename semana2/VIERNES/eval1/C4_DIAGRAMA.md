# Arquitectura del Sistema: Nivel 2 (Diagrama de Contenedores)

```mermaid
C4Container
    title Diagrama de Contenedores - Sistema Monitoreo IoT Bodega

    Person(operador, "Supervisor / Operador", "Responsable de monitorear la bodega y atender emergencias.")

    System_Boundary(iot_core, "Core del Sistema IoT") {
        Container(simulador, "Hardware Simulator", "Python", "Genera ruido térmico Gaussiano simulando sensores físicos.")
        Container(ingesta, "Data Ingestion", "Python (Modelos)", "Valida IDs y crea objetos inmutables SensorReading.")
        Container(motor, "Anomaly Detector", "Python (Reglas)", "Evalúa lecturas contra umbrales (T>35, H>80).")
        Container(alertas, "Alert Manager", "Patrón Strategy", "Despacha notificaciones abstractas (Consola, Log, Email).")
    }

    Rel(simulador, ingesta, "Envía telemetría (Poling 30s)", "Objetos instanciados")
    Rel(ingesta, motor, "Transfiere datos validados", "En Memoria")
    Rel(motor, alertas, "Invoca interface Protocol", "Inyección de Dependencias")
    Rel(alertas, operador, "Dispara notificación crítica", "Consola / Email")