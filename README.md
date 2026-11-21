# Sistema Integral de Gestión de Clientes, Servicios y Reservas — Software FJ

Proyecto desarrollado en **Python** para la **Fase 4 (Anexo 3)** del sistema **Software FJ**, orientado a objetos y diseñado para operar **en memoria sin bases de datos**, utilizando archivos de registro (`logs`) para auditar eventos y errores controlados.

---

## Características principales

* **Arquitectura orientada a objetos sin base de datos:** Gestión en memoria de clientes, servicios y reservas mediante listas y entidades del dominio.
* **Estructura modular (`software_fj`):** Organización del código en módulos especializados (`entidades.py`, `cliente.py`, `servicios.py`, `reserva.py`, `gestor.py`, `registro.py`, `excepciones.py` y `simulacion.py`)
* **Manejo avanzado de excepciones:** Uso de bloques `try / except / else / finally`, excepciones personalizadas del dominio y encadenamiento explícito de excepciones (`from exc`).
* **Registro automático de eventos y errores:** Escritura continua de eventos y errores controlados en `logs/software_fj.log` manteniendo la ejecución estable ante fallos
* **Simulación secuencial resiliente:** Ejecución de **42 operaciones** (combinando casos válidos e inválidos) verificando que el sistema continúe operando sin interrupciones.

---

## Estructura del paquete

* `software_fj/entidades.py`: Base común de entidades y utilidades del dominio (como formato de moneda)
* `software_fj/cliente.py`: Gestión y validación de clientes
* `software_fj/servicios.py`: Clase base de servicios y subclases especializadas (como reserva de salas, alquiler de equipos y asesoría especializada) con cálculo de costos
* `software_fj/reserva.py`: Gestión del ciclo de vida y estados de las reservas (`Procesada`, `Cancelada`, `Pendiente`)
* `software_fj/gestor.py`: Administración en memoria de clientes, servicios y reservas
* `software_fj/excepciones.py`: Excepciones personalizadas del sistema.
* `software_fj/registro.py`: Configuración del logger y ruta del archivo de logs (`logs/software_fj.log`)
* `software_fj/simulacion.py`: Secuencia de simulación de 42 operaciones y resumen final

---

## Verificación y ejecución

Desde la carpeta raíz del proyecto (`Software_FJ`), puedes compilar y ejecutar la simulación como módulo:

```powershell
py -m py_compile software_fj\*.py
py -c "from software_fj.simulacion import ejecutar_simulacion; print(ejecutar_simulacion())"
