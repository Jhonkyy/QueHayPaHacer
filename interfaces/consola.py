from getpass import getpass
from typing import List
from models.evento import Evento
from models.sistema import Sistema

class InterfazConsola:
    def __init__(self, sistema: Sistema):
        self.sistema = sistema

    def mostrar_menu_principal(self):
        while True:
            print("\n=== QuéHayPaHacer? ===")
            print("1. Iniciar sesión")
            print("2. Registrarse")
            print("3. Explorar eventos")
            print("4. Salir")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.iniciar_sesion()
            elif opcion == "2":
                self.registrar_usuario()
            elif opcion == "3":
                self.explorar_eventos()
            elif opcion == "4":
                print("¡Hasta luego!")
                break
            else:
                print("Opción inválida. Intente nuevamente.")

    def iniciar_sesion(self):
        print("\n--- Iniciar Sesión ---")
        email = input("Email: ")
        password = input("Contraseña: ")

        if self.sistema.iniciar_sesion(email, password):
            self.menu_usuario()

    def registrar_usuario(self):
        print("\n--- Registro de Usuario ---")
        nombre = input("Nombre completo: ")
        email = input("Email: ")
        password = input("Contraseña (mínimo 6 caracteres): ")

        self.sistema.registrar_usuario(nombre, email, password)

    def menu_usuario(self):
        while self.sistema.usuario_actual:
            self.sistema.verificar_recordatorios()

            print("\n=== Menú Principal ===")
            print(f"Bienvenido, {self.sistema.usuario_actual.nombre}!")
            print("1. Explorar eventos")
            print("2. Mis favoritos")
            print("3. Crear evento")
            print("4. Recomendaciones")
            print("5. Preferencias")
            print("6. Cerrar sesión")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.explorar_eventos()
            elif opcion == "2":
                self.mostrar_favoritos()
            elif opcion == "3":
                self.crear_evento()
            elif opcion == "4":
                self.mostrar_recomendaciones()
            elif opcion == "5":
                self.gestionar_preferencias()
            elif opcion == "6":
                self.sistema.cerrar_sesion()
                break
            else:
                print("Opción inválida. Intente nuevamente.")

    def explorar_eventos(self):
        print("\n--- Explorar Eventos ---")
        print("Filtros disponibles (deje en blanco para omitir):")

        categoria = input("Categoría: ")
        ubicacion = input("Ubicación: ")
        fecha = input("Fecha (YYYY-MM-DD): ")

        print("\nOpciones de ordenamiento:")
        print("1. Por fecha (predeterminado)")
        print("2. Por nombre")
        print("3. Por categoría")
        orden_opcion = input("Seleccione orden (1-3): ")

        orden = 'fecha'
        if orden_opcion == "2":
            orden = 'nombre'
        elif orden_opcion == "3":
            orden = 'categoria'

        eventos = self.sistema.explorar_eventos(
            categoria=categoria if categoria else None,
            ubicacion=ubicacion if ubicacion else None,
            fecha=fecha if fecha else None,
            orden=orden
        )

        if not eventos:
            print("No se encontraron eventos con los filtros seleccionados.")
            return

        self.mostrar_lista_eventos(eventos, mostrar_opciones=True)

    def mostrar_lista_eventos(self, eventos: List[Evento], mostrar_opciones: bool = False):
        for i, evento in enumerate(eventos, 1):
            print(f"\n[{i}] {evento.nombre}")
            print(f"  📍 {evento.ubicacion} | 📅 {evento.fecha} | 🏷️ {evento.categoria}")
            print(f"  🧑‍🤝‍🧑 Capacidad: {evento.capacidad}")
            print(f"  📝 {evento.descripcion}")
            print(f"  👤 Organizador: {self.sistema.obtener_organizador_nombre(evento.organizador_id)}")

            if self.sistema.usuario_actual:
                es_favorito = evento.id in self.sistema.usuario_actual.favoritos
                print(f"  ⭐ {'Ya en favoritos' if es_favorito else 'No en favoritos'}")

        if mostrar_opciones and eventos:
            print("\nOpciones:")
            if self.sistema.usuario_actual:
                print("1. Ver detalles de un evento")
                print("2. Agregar a favoritos")
                print("3. Eliminar de favoritos")
                print("4. Volver")

                opcion = input("Seleccione una opción (1-4): ")

                if opcion == "1":
                    num = input("Ingrese el número del evento a ver: ")
                    try:
                        num = int(num)
                        if 1 <= num <= len(eventos):
                            self.mostrar_detalle_evento(eventos[num - 1])
                    except ValueError:
                        print("Número inválido.")
                elif opcion == "2":
                    num = input("Ingrese el número del evento a agregar a favoritos: ")
                    try:
                        num = int(num)
                        if 1 <= num <= len(eventos):
                            self.sistema.agregar_favorito(eventos[num - 1].id)
                    except ValueError:
                        print("Número inválido.")
                elif opcion == "3":
                    num = input("Ingrese el número del evento a eliminar de favoritos: ")
                    try:
                        num = int(num)
                        if 1 <= num <= len(eventos):
                            self.sistema.eliminar_favorito(eventos[num - 1].id)
                    except ValueError:
                        print("Número inválido.")
            else:
                input("\nPresione Enter para continuar...")

    def mostrar_detalle_evento(self, evento: Evento):
        print("\n--- Detalles del Evento ---")
        print(evento)

        if self.sistema.usuario_actual:
            print("\nOpciones:")
            if evento.id in self.sistema.usuario_actual.favoritos:
                print("1. Eliminar de favoritos")
            else:
                print("1. Agregar a favoritos")
            print("2. Volver")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                if evento.id in self.sistema.usuario_actual.favoritos:
                    self.sistema.eliminar_favorito(evento.id)
                else:
                    self.sistema.agregar_favorito(evento.id)
            elif opcion == "2":
                return

    def mostrar_favoritos(self):
        if not self.sistema.usuario_actual:
            print("Debe iniciar sesión para ver favoritos.")
            return

        print("\n--- Mis Eventos Favoritos ---")
        favoritos = self.sistema.obtener_favoritos()

        if not favoritos:
            print("No tienes eventos favoritos guardados.")
            return

        self.mostrar_lista_eventos(favoritos, mostrar_opciones=True)

    def crear_evento(self):
        if not self.sistema.usuario_actual:
            print("Debe iniciar sesión para crear eventos.")
            return

        print("\n--- Crear Nuevo Evento ---")
        nombre = input("Nombre del evento: ")
        ubicacion = input("Ubicación: ")
        fecha = input("Fecha (YYYY-MM-DD): ")
        categoria = input("Categoría: ")
        capacidad = input("Capacidad: ")
        descripcion = input("Descripción: ")

        try:
            capacidad = int(capacidad)
            if capacidad <= 0:
                raise ValueError
        except ValueError:
            print("La capacidad debe ser un número positivo.")
            return

        self.sistema.crear_evento(nombre, ubicacion, fecha, categoria, capacidad, descripcion)

    def mostrar_recomendaciones(self):
        if not self.sistema.usuario_actual:
            print("Debe iniciar sesión para ver recomendaciones.")
            return

        print("\n--- Recomendaciones Para Ti ---")
        recomendaciones = self.sistema.obtener_recomendaciones()

        if not recomendaciones:
            print("No hay recomendaciones disponibles. Agrega categorías a tus preferencias.")
            return

        self.mostrar_lista_eventos(recomendaciones, mostrar_opciones=True)

    def gestionar_preferencias(self):
        if not self.sistema.usuario_actual:
            print("Debe iniciar sesión para gestionar preferencias.")
            return

        print("\n--- Mis Preferencias ---")
        print(
            f"Categorías preferidas actuales: {', '.join(self.sistema.usuario_actual.categorias_preferidas) or 'Ninguna'}")

        print("\n1. Agregar categoría")
        print("2. Eliminar categoría")
        print("3. Volver")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nueva_categoria = input("Ingrese la nueva categoría: ")
            if nueva_categoria:
                self.sistema.agregar_categoria_preferida(nueva_categoria)
                print("Categoría agregada!")
        elif opcion == "2":
            if not self.sistema.usuario_actual.categorias_preferidas:
                print("No hay categorías para eliminar.")
                return

            print("Seleccione la categoría a eliminar:")
            for i, cat in enumerate(self.sistema.usuario_actual.categorias_preferidas, 1):
                print(f"{i}. {cat}")

            try:
                num = int(input("Número: "))
                if 1 <= num <= len(self.sistema.usuario_actual.categorias_preferidas):
                    cat_eliminar = self.sistema.usuario_actual.categorias_preferidas[num - 1]
                    self.sistema.usuario_actual.categorias_preferidas.remove(cat_eliminar)

                    categorias_str = ','.join(self.sistema.usuario_actual.categorias_preferidas)
                    cursor = self.sistema.conn.cursor()
                    cursor.execute('''
                        UPDATE usuarios 
                        SET categorias_preferidas = ?
                        WHERE id = ?
                    ''', (categorias_str, self.sistema.usuario_actual.id))
                    self.sistema.conn.commit()

                    print("Categoría eliminada!")
            except ValueError:
                print("Opción inválida.")