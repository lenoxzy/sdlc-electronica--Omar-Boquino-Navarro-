# ADR 0002: Soft-delete de sensores y estados de alerta sin máquina de estados

## Estado
Aceptado

## Contexto
RF-1 exige que en producción los sensores no se borren, se desactiven.
RF-5 exige que las alertas tengan un estado consultable y modificable
(open / acknowledged / resolved). Para el estado de alerta existían dos
caminos: una máquina de estados con transiciones validadas (ej. no permitir
saltar de "open" a "resolved" sin pasar por "acknowledged"), o un enum
libre donde cualquier transición es válida.

## Decisión
**Soft-delete:** se agregó `Sensor.is_active: bool` (default `True`).
`DELETE /sensors/{id}` marca `is_active=False` en vez de borrar la fila.
`GET /sensors` excluye sensores inactivos por defecto.

**Estado de alerta:** se optó por un enum libre
(`Literal["open", "acknowledged", "resolved"]` en Pydantic), sin una
máquina de estados que valide secuencia de transiciones. Cualquier
estado válido del enum puede asignarse directamente vía
`PATCH /alerts/{id}/status`, sin importar el estado anterior.

## Consecuencias

### Positivas (+)
* Soft-delete preserva integridad referencial: las lecturas y alertas de
  un sensor desactivado siguen siendo consultables e íntegras.
* El enum libre para alertas se implementó en una fracción del tiempo
  que hubiera tomado una máquina de estados completa, cumpliendo RF-5
  tal como está redactado ("consulta de activas y cambio de estado"),
  sin funcionalidad no solicitada.

### Negativas (-)
* Sin máquina de estados, nada impide una transición ilógica como
  `resolved -> open` vía API, aunque en la práctica el flujo esperado
  del operador es lineal. Es una decisión consciente de simplicidad
  sobre robustez, tomada por restricción de tiempo real del proyecto,
  no por desconocimiento de la alternativa.
* `GET /sensors/{id}` individual SÍ devuelve sensores inactivos (solo
  `GET /sensors` en listado los excluye) — es una inconsistencia menor
  de diseño que no se resolvió por priorizar tiempo; documentada aquí
  para que sea decisión explícita, no descubrimiento accidental.

## Alternativa descartada
Una máquina de estados con transiciones validadas
(`open -> acknowledged -> resolved`, rechazando saltos) fue diseñada y
descartada conscientemente por tiempo disponible. Si el proyecto
escalara a producción real con múltiples operadores, sería la primera
mejora a implementar sobre RF-5.