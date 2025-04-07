from datetime import datetime

class Evento:
    def __init__(self, id: int, nombre: str, ubicacion: str, fecha: str, 
                 categoria: str, capacidad: int, descripcion: str, organizador_id: int):
        self.id = id
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.fecha = fecha
        self.categoria = categoria
        self.capacidad = capacidad
        self.descripcion = descripcion
        self.organizador_id = organizador_id

    def __str__(self):
        return (f"Evento: {self.nombre}\n"
                f"Ubicación: {self.ubicacion}\n"
                f"Fecha: {self.fecha}\n"
                f"Categoría: {self.categoria}\n"
                f"Capacidad: {self.capacidad}\n"
                f"Descripción: {self.descripcion[:50]}...\n"
                f"Organizador ID: {self.organizador_id}")

    def es_proximo(self) -> bool:
        """Determina si el evento está próximo (en los próximos 3 días)"""
        try:
            fecha_evento = datetime.strptime(self.fecha, '%Y-%m-%d').date()
            hoy = datetime.now().date()
            return 0 <= (fecha_evento - hoy).days <= 3
        except ValueError:
            return False