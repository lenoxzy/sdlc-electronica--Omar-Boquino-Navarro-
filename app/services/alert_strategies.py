"""Estrategias de notificacion de alertas (Open/Closed Principle).

Agregar una nueva forma de notificar (email, webhook, SMS) significa
crear una clase nueva aqui. AlertService nunca se modifica para eso.
"""
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class AlertStrategy(ABC):
    """Contrato: toda estrategia sabe notificar un mensaje."""

    @abstractmethod
    def notify(self, message: str) -> None: ...


class ConsoleAlertStrategy(AlertStrategy):
    """Notifica imprimiendo en consola. Util en desarrollo local."""

    def notify(self, message: str) -> None:
        print(f"[ALERTA] {message}")


class LogAlertStrategy(AlertStrategy):
    """Notifica via el sistema de logging estandar de Python."""

    def __init__(
        self, logger_instance: logging.Logger | None = None
    ) -> None:
        self._logger = logger_instance or logger

    def notify(self, message: str) -> None:
        self._logger.warning(message)