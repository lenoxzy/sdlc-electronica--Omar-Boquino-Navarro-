import pytest
from enum import Enum, auto
class TrafficLightState(Enum):
    RED = auto()
    YELLOW = auto()
    GREEN = auto()

class TrafficLightFSM:
    
    def __init__(self, initial_state: TrafficLightState = TrafficLightState.RED) -> None:
        self._state = initial_state
        self._cycle_count = 0

    @property
    def state(self) -> TrafficLightState:
        return self._state

    def transition(self) -> TrafficLightState:
        transitions = {
            TrafficLightState.RED: TrafficLightState.GREEN,
            TrafficLightState.GREEN: TrafficLightState.YELLOW,
            TrafficLightState.YELLOW: TrafficLightState.RED,
        }
        self._state = transitions[self._state]
        self._cycle_count += 1
        return self._state


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
