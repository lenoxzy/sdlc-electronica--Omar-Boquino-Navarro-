## Semana 4 · Entrada 1
Prompt: "modifica db.py para leer DATABASE_URL del entorno, con SQLite como
default local, y normaliza postgres:// / postgresql:// a postgresql+psycopg://"

La IA propuso una función get_database_url() y agregar connect_args condicional
(check_same_thread solo aplica a SQLite). Acepté la función tal cual. Modifiqué
la sugerencia inicial de connect_args = {} sin tipo: mypy marcaba error porque
disallow_untyped_defs exige anotación explícita. Cambié a
connect_args: dict[str, bool] = {} para que pasara mypy sin desactivar la regla.

## Semana 4 · Entrada 2
Prompt: "docker compose up --build falla con connection refused en api-1
aunque db-1 ya inició"

La IA diagnosticó que depends_on: [db] solo espera a que el contenedor exista,
no a que PostgreSQL acepte conexiones, y propuso un healthcheck con pg_isready
más depends_on con condition: service_healthy. Acepté la solución completa.
Verifiqué el comportamiento reiniciando con docker compose down -v para
confirmar que el healthcheck realmente bloqueaba el arranque de api hasta que
db reportara "healthy" en los logs.

## Semana 4 · Entrada 3
Prompt: "necesito inicializar Alembic para las migraciones"

La IA propuso quitar Base.metadata.create_all() de main.py y reemplazarlo por
Alembic como único responsable del esquema, argumentando que create_all() no
modifica tablas existentes y ya me había causado un error de "no such column"
en la semana. Acepté el cambio de arquitectura. Antes de aplicarlo pregunté
por qué no podían convivir ambos mecanismos en paralelo; la respuesta (evitar
que dos sistemas compitan por la misma responsabilidad, y alinear el proyecto
con el flujo de arranque que pide la guía para producción) me convenció de
aceptarlo sin modificarlo.

## Semana 4 · Entrada 4
Prompt: "una línea autogenerada por Alembic en migrations/versions supera el
límite de ruff, ¿la reescribo?"

La IA propuso dos opciones: reformatear la línea a mano, o excluir
migrations/versions del linting vía extend-exclude en pyproject.toml. Rechacé
reformatear a mano porque cada alembic revision --autogenerate futura
regeneraría el archivo con el mismo formato, obligándome a repetir el ajuste
cada vez. Acepté la exclusión: es código generado por una herramienta, no
código que yo mantengo línea por línea, y es la práctica estándar para
carpetas de migraciones autogeneradas.

## Semana 5 · Entrada 1
Prompt (vía Aider, modelo gemini/gemini-3.6-flash): "Crea una clase
AnomalyService con un método check(reading, threshold) que use is_anomalous
internamente y registre el resultado. Sigue el patrón de inyección de
dependencias que ya uso en ReadingService."

Aider generó AnomalyService completa en dos commits automáticos separados.
Rechacé y corregí dos cosas con un commit propio posterior:
- is_anomalous usaba abs(value) > threshold sin que se lo pidiera, cambiando
  la semántica: con umbral de calor, una lectura muy fría también activaría
  la alerta. Lo definí en la Tarea 2 de prompting.md como value > threshold
  y Aider lo alteró sin avisar - lo revertí a la versión original.
- check(reading: Any, ...) usaba tipado débil pese a que el proyecto exige
  disallow_untyped_defs en mypy estricto. Lo tipé como ReadingModel, el tipo
  real que ya uso en todo el proyecto.
Acepté sin cambios: la inyección de logger, el patrón de logging
warning/info, y la estructura general de la clase.

## Semana 5 · Día 6 — Peer review humano vs. IA

1. Ver el review de la IA antes de terminar mi propia pasada humana
   contaminó mi capacidad de encontrar cosas "a ciegas" — orden correcto:
   primero pasada humana completa, IA después como segunda opinión.

2. La IA (con solo 4 archivos de código, sin contexto del PR) encontró
   violaciones de arquitectura y tipos que yo no había anotado por
   escrito: falta de AlertService, threshold_breached sin Literal,
   router retornando el modelo ORM en vez del schema.

3. Yo encontré algo que la IA NUNCA pudo haber visto: el título y la
   descripción del PR eran vagos e insuficientes. No es que yo sea mejor
   revisando código — es que la IA nunca tuvo ese contexto en el prompt.
   Un review de IA es tan completo como el contexto que le des; si no le
   compartes el PR completo (metadata incluida), tiene un punto ciego
   estructural que un humano con acceso real al repositorio no tiene.


## Semana 6 · Entrada 1
Decisión de diseño: RF-1 pedía "no borrar, desactivar" un sensor en
producción. Implementé soft-delete con Sensor.is_active en vez de mantener
el DELETE físico original de la Semana 3. Esto rompió un test existente
(test_delete_sensor_success, que esperaba 404 tras borrar) — lo actualicé
para reflejar el contrato nuevo: 204 al desactivar, el registro sigue
existiendo y consultable individualmente con is_active=False.

## Semana 6 · Entrada 2
Decisión de diseño (documentada en ADR 0002): para RF-5 (estado de
alerta), evalué una máquina de estados con transiciones validadas
(open -> acknowledged -> resolved, sin saltos) contra un enum libre sin
validación de secuencia. Elegí el enum libre por restricción real de
tiempo — cumple RF-5 tal como está redactado, sin funcionalidad no
solicitada. Documenté la alternativa descartada y la limitación conocida
(nada impide un salto ilógico de estado) en vez de ocultarla.

## Semana 6 · Entrada 3
Aprendizaje técnico: al generar la migración de Alembic para is_active y
status, el autogenerate no agregó server_default en ninguna de las dos
columnas nullable=False. Antes de aplicarla verifiqué manualmente qué
pasaría con filas ya existentes (creé un sensor y una lectura primero, y
corrí la migración después) — sin server_default, esto hubiera fallado
contra Postgres con datos reales aunque pasara sin problema en un SQLite
vacío. Agregué server_default='open' y server_default=sa.true()
explícitamente antes de aplicarla.

## Semana 6 · Entrada 4
Decisión de alcance: para RF-6 (estadísticas), calculate_stats() recibe
una lista de floats en memoria en vez de agregar MIN/MAX/AVG directamente
en SQL. Es una limitación real y consciente — no escalaría bien con
millones de lecturas por sensor — pero la versión con agregación SQL
hubiera costado más tiempo del que amerita esta entrega. Lo documenté
como respuesta honesta preparada para la presentación técnica, en vez de
ocultar la limitación. 