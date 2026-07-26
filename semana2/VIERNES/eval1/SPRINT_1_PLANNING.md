# Sprint 1 Planning: Sistema de Monitoreo IoT

##  Sprint Goal (meta)
Establecer el núcleo funcional (MVP) del sistema: Lograr ingestar datos de sensores autorizados de forma segura, detectar anomalías críticas de temperatura (>35°C) y humedad (>80%), y disparar alertas inmediatas.

##  Historias de Usuario Seleccionadas (Sprint Backlog)
Se seleccionaron 5 Historias de Usuario. 
Justificacion: Estas historias conforman el "Must Have". Sin registro seguro (US-05) ni ingesta (US-01), no hay datos. Sin detección (US-02, US-03) y alertas (US-04), no hay valor de negocio para la bodega.

### 1. US-05: Registro y alta de sensores (2 SP)
 **Tarea 1.1:** Definir modelo de datos `Sensor` y clase `SensorRegistry` mediante TDD. (2h)
 **Tarea 1.2:** Implementar validación de IDs permitidos y manejo de error genérico `UnknownSensorError`. (2h)

### 2. US-01: Recepción de datos base (Ingesta) (5 SP)
 **Tarea 2.1:** Crear modelo inmutable `SensorReading` usando `dataclasses`. (1h)
 **Tarea 2.2:** Programar el parser (DataParser) que convierta el JSON simulado del hardware a objetos `SensorReading` usando TDD. (3h)
 **Tarea 2.3:** Integrar el parser con la validación de `SensorRegistry`. (2h)

### 3. US-02: Detección de Anomalías de Temperatura (3 SP)
 **Tarea 3.1:** Escribir tests en rojo para cruce de umbrales (>35.0°C). (1.5h)
 **Tarea 3.2:** Implementar lógica condicional en motor de reglas `AnomalyDetector`. (2h)

### 4. US-03: Detección de Anomalías de Humedad (3 SP)
 **Tarea 3.1:** Escribir tests en rojo para límite de humedad (>80.0%). (1.5h)
 **Tarea 3.2:** Extender el `AnomalyDetector` para soportar múltiples tipos de lectura respetando el principio Abierto/Cerrado (OCP). (2.5h)

### 5. US-04: Disparo de Alertas (5 SP)
 **Tarea 4.1:** Definir la interfaz `AlertStrategy` (Inversión de Dependencias). (1h)
 **Tarea 4.2:** Escribir implementación concreta `ConsoleAlert` simulando envío. (1.5h)
 **Tarea 4.3:** Inyectar la alerta en el `AnomalyDetector` y probar flujo completo end-to-end. (3h)

*( Ninguna tarea técnica supera las 4 horas ).*

---

##  Definition of Done (DoD) del Sprint
Para que este Sprint sea considerado "Terminado" y listo para Review, todo el código debe cumplir:
1. **TDD:** Todas las pruebas pasan en verde (`pytest`).
2. **Cobertura:** Mínimo de 80% de cobertura en ramas lógicas (`pytest --cov`).
3. **Calidad de Código:** Análisis estático sin errores de estilo ni de lógica (`ruff check .`).
4. **Tipado Estricto:** Cero errores de tipos en la evaluación estática (`mypy .`).
5. **Git Flow:** Todo el código integrado mediante Pull Requests y auto-revisión, sin commits directos a `main`.
