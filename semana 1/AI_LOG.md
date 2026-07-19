#  Bitácora de Aprendizaje

 En este repositorio documento mi progreso, los prompts utilizados y mi desarrollo durante el curso.

## Semana 1 -objetivo de la semana  Mapear conceptos, Escribir Python idiomatico, Aplicar los 5 principios de SOLID, Practicar el flujo profesional de git y Arrancar con la bitacora de IA  -

### Día 1: Lunes 
**Entrada 1**

** Prompt utilizado:**
 "5 funciones puras sobre Reading (conversión de unidades, detección de umbral, serialización) con type hints completos"

** Notas de la sesión:**
Antes de realizar el prompt para que tuviera de una referencia le mande el codigo de la activiad.
La IA me otorgo las 5 funciones puras pero de esas 5 tome 3 ya que dos de ellas ya las habia hecho con anterioridad.

** Líneas de código descartadas:**
```python
def celsius_to_fahrenheit(r: Reading) -> Reading:
    # Código descartado
    pass

def check_threshold(r: Reading, max_limit: float) -> bool:
    # Código descartado
    pass
```
## Día 2: -Martes - 
**Entrada 2**
** Prompt utilizado:**
"quiero que el estado inicial inicie con el color rojo y que lo pueda probar con pytest"
**📝 Notas de la sesión:**
Como en el caso anterior antes de realizar algun pedido a la IA, necesita una guia para poder basarse para relizar de la mejor manera el prompt.
Asi que de nuevo le mande el codigo que fue proporcionado en el curso y revisando el codigo me percate que el codigo proporcionado por la IA era correcto ya que realizaba lo solicitado por la actividad del dia MARTES.
Solo fue cuestion de cambiar algunas palabras para un mejor entendimiento del codigo y realizar algunas busquedas por internet ya que algunos conceptos del mismo codigo no llegue a entender bien. 

** Líneas de código anexadas:**
```python
def estado_inicial_rojo():
    """ la instruccion assert ayuda a validar la prueba""" 
    """Valida que si no se pasa argumento, el semáforo inicie en ROJO."""
    semaforo = TrafficLightFSM()
    assert semaforo.state == TrafficLightState.RED
    assert semaforo._cycle_count == 0

def test_transiciones_de_estado():
    """Valida que el ciclo fluya correctamente: ROJO -> VERDE -> AMARILLO -> ROJO."""
    semaforo = TrafficLightFSM()
    
    # 1. De Rojo a Verde
    cambio = semaforo.transition()
    assert cambio == TrafficLightState.GREEN
    assert semaforo.state == TrafficLightState.GREEN
    
    # 2. De Verde a Amarillo
    cambio = semaforo.transition()
    assert cambio == TrafficLightState.YELLOW
    assert semaforo.state == TrafficLightState.YELLOW
    
    # 3. De Amarillo a Rojo (Ciclo completo)
    cambio = semaforo.transition()
    assert cambio == TrafficLightState.RED
    assert semaforo.state == TrafficLightState.RED

def test_conteo_de_ciclos():
    """Valida que el contador de ciclos incremente en cada transición."""
    semaforo = TrafficLightFSM()
    
    semaforo.transition() # +1
    semaforo.transition() # +1
    
    assert semaforo._cycle_count == 2
```
## Día 3: -Miercoles - 
**Entrada 3**
** Prompt utilizado:**
Antes de realizar algun prompt realice preguntas respecto al tema SOLID (que es, para que me sirve y ejemoplos con y sin SOLID ).
Despues de eso mande el codigo proporcionado por el curso para que la IA tuviera una referencia para los prompt. 
despues le coloque este prompt "Implementa los tres primeros principios con el dominio de sensores", asi otorgandome 3 codigos separados siendo los 3 primeros principios de SOLID (S,O,L).
**📝 Notas de la sesión:**
revisando los codigos otorgados por la IA, me parecieron correctos asi que me dispuse a unirlos en un mismo codigo grande para mejor comodidad para correrlo y testearlo en mi PC.
una vez viendo que los codigos funcionaban bien, tome de referencia esos codigos y los codigos de ejemplo que me habia dado con anterioridad para realizar la version sin parametros SOLID .
Ya teniendo ambos codigos le mande los codigos a la IA para anexar el pytest otorgandome los codigos que estan anexados en la carpeta MIERCOLES.






## Día 4: -jueves - 
**Entrada 4**
** Prompt utilizado:**
> 1.
 ```python
class DataRepository(Protocol):

def save(self, reading: SensorReading) -> None: ...

def get_latest(self, sensor_id: str) -> SensorReading | None: ...


class DataProcessor:

"""Depende de la abstraccion, no de una implementacion concreta."""

def __init__(self, repository: DataRepository) -> None:

self._repo = repository # inyeccion de dependencias


# En produccion: DataProcessor(PostgreSQLRepository())

# En tests: DataProcessor(InMemoryRepository()) <- sin base de datos 
 ```
"teniedo en cuenta este codigo realiza una estructura del Principio de Inversión de Dependencias (DIP)."
> 2. "como puedo realizarle un pytest"
**📝 Notas de la sesión:**
La IA me otorgo un codigo donde contenia las partes solicitadas por la actividad del dia jueves asi que acepte el codigo no obstante realice algunos cambios pequeños al codigo para mi mejor comprencion. asi mismo a la parte de pytest.
Tambien gracias a las referencias que le otorgo antes de realizar los promts me puede resolver problemas que me surgen a lo largo de la implementacion del codigo. 


## Día 5: -Viernes - 
**Entrada 5**
** Prompt utilizado:**
```python
>     def driver_MODERNIZADO_UART() -> None:

    """ Verifica que el driver UART pueda leer una cadena de texto sin

    necesidad de hardware físico y la procese correctamente mediante parsers.py.



    se debe reimtepretar en python moderno utilizando los principios SOLID,

     como los siguientes:

     -SRP inmutabilidad

     -OCP,LSP,ISP, DIP: inyeccion de dependencias, interfaces y polimorfismo
```
> 1.  "esta correcto asi?"
> 2. "listo ya me salió todo en verde para terminar falta Extensión (alimenta la Distinción): tercer protocolo (CAN simplificado), buffer circular thread-safe con threading.Lock, logging estructurado JSON."
> 3. " me marco esto (NameError: name 'SensorReading' is not defined)"

**📝 Notas de la sesion:**
 La IA generó las implementaciones correspondientes para cumplir con la extensión: un `CANParser` (cumpliendo OCP), un `ThreadSafeCircularRecorder` usando `threading.Lock` para control de concurrencia, y un `JSONLoggingRecorderWrapper` aplicando el patrón Decorator. Posteriormente, al encontrarme con errores de ejecución, la IA me explicó la estructura física de los módulos y cómo importar correctamente las clases entre los archivos.

Acepté la estructura  sugerida por la IA, ya que respeta fielmente los protocolos (interfaces). Sin embargo, tuve que modificar y aplicar mi propio criterio en la gestión de archivos: el código de la IA asumía un entorno plano, pero al separar mis responsabilidades en `codigouni.py` y `test_driver.py`, me enfrenté a un `NameError`. Identifiqué que la responsabilidad de importar los modelos (`SensorReading`, `UARTDevice`) recae en el archivo que ensambla las pruebas, por lo que actualicé mis cabeceras con `from codigouni import ...` hasta que el ecosistema completo pasó en verde.






