import multiprocessing
import queue
import time

def proceso_1(cola_alta_prioridad, cola_proceso_2):
    """Proceso que genera tareas de alta prioridad."""
    for i in range(5):
        cola_alta_prioridad.put((0, f"Tarea de alta prioridad {i}"))  # 0 indica alta prioridad
        time.sleep(1)
    cola_proceso_2.put("Mensaje para proceso 2 desde proceso 1")

def proceso_2(cola_proceso_2, cola_proceso_3):
    """Proceso que recibe mensajes de proceso 1 y envía a proceso 3."""
    mensaje = cola_proceso_2.get()
    print(f"Proceso 2 recibió: {mensaje}")
    cola_proceso_3.put("Mensaje para proceso 3 desde proceso 2")

def proceso_3(cola_proceso_3, cola_proceso_4):
    """Proceso que recibe mensajes de proceso 2 y envía a proceso 4."""
    mensaje = cola_proceso_3.get()
    print(f"Proceso 3 recibió: {mensaje}")
    cola_proceso_4.put("Mensaje para proceso 4 desde proceso 3")

def proceso_4(cola_proceso_4, cola_alta_prioridad):
    """Proceso que recibe mensajes de proceso 3 y maneja la cola de prioridad."""
    mensaje = cola_proceso_4.get()
    print(f"Proceso 4 recibió: {mensaje}")
    while not cola_alta_prioridad.empty():
        prioridad, tarea = cola_alta_prioridad.get()
        print(f"Proceso 4 ejecutando: {tarea}")
        time.sleep(0.5)

if __name__ == "__main__":
    cola_alta_prioridad = multiprocessing.Queue()
    cola_proceso_2 = multiprocessing.Queue()
    cola_proceso_3 = multiprocessing.Queue()
    cola_proceso_4 = multiprocessing.Queue()

    p1 = multiprocessing.Process(target=proceso_1, args=(cola_alta_prioridad, cola_proceso_2))
    p2 = multiprocessing.Process(target=proceso_2, args=(cola_proceso_2, cola_proceso_3))
    p3 = multiprocessing.Process(target=proceso_3, args=(cola_proceso_3, cola_proceso_4))
    p4 = multiprocessing.Process(target=proceso_4, args=(cola_proceso_4, cola_alta_prioridad))

    p1.start()
    p2.start()
    p3.start()
    p4.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()

    print("Todos los procesos han terminado.")