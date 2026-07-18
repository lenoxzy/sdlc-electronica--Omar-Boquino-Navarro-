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







