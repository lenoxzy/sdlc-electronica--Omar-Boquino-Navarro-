# Deteccion de Anomalias de temperatura nocturna 
## Como dueñor de un centro de viveros, deseo la implementacion de un sistema que me pueda monitorear la temperatura en los viveros en la noche entre 15 °C a 18 °C para poder garantizar un exelente desarrolo del plantio y evitar su daño.

# Criterios (Gherkin)
 Given que el horario del sistema es nocturno (18:00 a 05:59) y el umbral máximo es 18°C y minimo es 15 °C
 When ingrese una lectura de exactamente 18.1 °C
 Then el sistema debe marcar la lectura como anómala
 And debe disparar un evento tipo "Alerta temperatura superior "
 Given que el horario del sistema es nocturno (18:00 a 05:59) y el umbral máximo es 18°C y minimo es 15 °C
 When ingrese una lectura de exactamente 14.9 °C 
 Then el sistema debe marcar la lectura como anómala
 And debe disparar un evento tipo "Alerta temperatura inferior "
 Estimación: 3 Story Points
 Prioridad: Must have 

# Deteccion de Anomalias de humedad
## como dueño de un centro de viveros,quiero que el sistema monitoree y detecte si la humedad ambiental se mantenga entre (60% al 80%),
para registrar una alerta y evitar que las plantas se deshidraten o desarrollen hongos.

## Criterios (Gherkin)
 Given que el umbral de humedad del sensor está configurado con un mínimo de 60% y un máximo de 80%
 When ingrese una lectura de humedad de exactamente 80.1%
 Then el sistema debe marcar la lectura como anómala
And disparar un evento tipo "Alerta Humedad Alta"
 Given que el umbral de humedad está configurado con los mismos parámetros
 When ingrese una lectura de humedad de exactamente 59.9%# Then el sistema debe marcar la lectura como anómala
 And disparar un evento tipo "Alerta Humedad Baja"
 Estimación: 3 Story Points
 Prioridad: Must Have
