class SensorNotFoundError(Exception):
    """Excepción lanzada cuando no se encuentra un sensor en la base de datos."""
    pass

class ReadingNotFoundError(Exception):
    """Excepción lanzada cuando no se encuentra una lectura en la base de datos."""
    pass