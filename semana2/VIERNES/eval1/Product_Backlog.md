# US-01: Recepción de datos base (Ingesta)
Como Sistema Core, quiero recibir y almacenar las lecturas de temperatura y humedad de los 10 sensores cada 30 segundos para mantener un registro histórico.

## Criterio de Aceptación (Gherkin):
Dado que los 10 sensores están activos y transmitiendo,
Cuando transcurren 30 segundos,
Entonces el sistema debe recibir, validar y guardar en la base de datos la lectura con su ID de sensor y marca de tiempo (timestamp).
Prioridad: Must have (M)
Story Points: 5

# US-02: Detección de Anomalías de Temperatura
Como Supervisor de bodega, quiero que el sistema detecte automáticamente si la temperatura supera los 35°C para prevenir daños por calor en la mercancía.

## Criterio de Aceptación (Gherkin):
Dado que el sistema recibe una nueva lectura de un sensor,
Cuando el valor de temperatura es mayor a 35.0 °C,
Entonces el sistema debe clasificar esa lectura como una "Anomalía Crítica de Temperatura".
Prioridad: Must have (M)
Story Points: 3


# US-03: Detección de Anomalías de Humedad
 Como Supervisor de bodega, quiero que el sistema detecte automáticamente si la humedad supera el 80% para evitar la formación de moho u óxido.

## Criterio de Aceptación (Gherkin):
Dado que el sistema recibe una nueva lectura de un sensor,
Cuando el valor de humedad es estrictamente mayor a 80.0%,
Entonces el sistema debe clasificar esa lectura como una "Anomalía Crítica de Humedad".
Prioridad: Must have (M)
Story Points: 3


# US-04: Disparo de Alertas
Como Operador de turno, quiero recibir una notificación inmediata cuando se detecte una anomalía para poder ir físicamente a revisar la zona afectada.

## Criterio de Aceptación (Gherkin):
Dado que el motor de reglas clasificó una lectura como anomalía,
Cuando la anomalía es guardada en el sistema,
Entonces se debe disparar una alerta por consola/log (o email simulado) indicando el ID del sensor y el valor crítico.
Prioridad: Must have (M)
Story Points: 5


# US-05: Registro y alta de sensores
 Como Administrador del sistema, quiero poder registrar los IDs únicos de los 10 sensores de la bodega para que el sistema rechace datos de sensores desconocidos.

## Criterio de Aceptación (Gherkin):
Dado que un sensor envía una trama de datos,
Cuando el ID del sensor no pertenece a la lista de los 10 sensores autorizados,
Entonces el sistema debe descartar la lectura y arrojar un error UnknownSensorError.
Prioridad: Must have (M)
Story Points: 2

# US-06: Monitoreo de salud del sensor (Watchdog)
Como Administrador de infraestructura, quiero que el sistema detecte si un sensor se apaga o desconecta para ir a repararlo o cambiarle la batería.

## Criterio de Aceptación (Gherkin):
Dado un sensor previamente registrado y activo,
Cuando el sistema no recibe datos de ese ID por más de 120 segundos (4 ciclos perdidos),
Entonces el sistema debe cambiar el estado del sensor a "OFFLINE" y emitir una advertencia técnica.
Prioridad: Should have (S)
Story Points: 5

# US-07: Panel de estado en tiempo real (Dashboard)
 Como Supervisor de bodega, quiero ver un panel visual con el último estado reportado de los 10 sensores para tener un vistazo rápido de toda la nave industrial.

## Criterio de Aceptación (Gherkin):
Dado que el supervisor consulta el estado actual,
Cuando solicita la vista del dashboard,
Entonces el sistema debe retornar la última lectura válida (temperatura y humedad) de cada uno de los 10 sensores en formato legible.
Prioridad: Should have (S)
Story Points: 8


# US-08: Historial de Anomalías
Como Analista de Calidad, quiero consultar el historial de todas las alertas generadas en el día para buscar patrones de fallas en ciertas zonas de la bodega.

## Criterio de Aceptación (Gherkin):
Dado que existen anomalías previas almacenadas,
Cuando el analista solicita el historial,
Entonces el sistema devuelve una lista ordenada por fecha y hora detallando qué sensor falló y con qué valor.
Prioridad: Should have (S)
Story Points: 3

# US-09: Exportación de datos para auditoría
Como Auditor externo, quiero descargar las lecturas del sistema en un archivo plano (CSV) para cruzar datos con mis propias herramientas.

## Criterio de Aceptación (Gherkin):
Dado un periodo de tiempo especificado,
Cuando el usuario activa la función de exportar,
Entonces el sistema genera y permite la descarga de un archivo datos_sensores.csv con los registros solicitados.
Prioridad: Could have (C)
Story Points: 3

# US-10: Predicción de sobrecalentamiento por Machine Learning
Como Gerente de Planta, quiero que el sistema use Machine Learning para predecir si una zona superará los 35°C en la próxima hora basándose en la tendencia.

## Criterio de Aceptación (Gherkin):
Dado un histórico de crecimiento de temperatura,
Cuando la pendiente de aumento proyecte superar el umbral en menos de 60 minutos,
Entonces el sistema envía una alerta preventiva "Predictive Warning".
Prioridad: Won't have (W) 
Story Points: 13
