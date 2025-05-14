import sqlite3
from datetime import datetime
from typing import List, Optional, Dict, Any
from .usuario import Usuario
from .evento import Evento
import getpass
import hashlib

class Sistema:
    def __init__(self):
        self.conn = sqlite3.connect('database/quehaypahacer.db')
        self.usuario_actual: Optional[Usuario] = None
        self._crear_tablas()

    def _crear_tablas(self):
        cursor = self.conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            categorias_preferidas TEXT
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            ubicacion TEXT NOT NULL,
            fecha TEXT NOT NULL,
            categoria TEXT NOT NULL,
            capacidad INTEGER NOT NULL,
            descripcion TEXT,
            organizador_id INTEGER NOT NULL,
            FOREIGN KEY (organizador_id) REFERENCES usuarios(id)
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS favoritos (
            usuario_id INTEGER NOT NULL,
            evento_id INTEGER NOT NULL,
            PRIMARY KEY (usuario_id, evento_id),
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
            FOREIGN KEY (evento_id) REFERENCES eventos(id)
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS asistentes (
            usuario_id INTEGER NOT NULL,
            evento_id INTEGER NOT NULL,
            PRIMARY KEY (usuario_id, evento_id),
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
            FOREIGN KEY (evento_id) REFERENCES eventos(id)
        )
        ''')
        
        self.conn.commit()

    # Métodos de usuario
    def registrar_usuario(self, nombre: str, email: str, password: str) -> bool:
        email = email.strip()  # Eliminar espacios en blanco o saltos de línea
        if not nombre or not email or not password:
            print("Error: Todos los campos son obligatorios.")
            return False
            
        if len(password) < 6:
            print("Error: La contraseña debe tener al menos 6 caracteres.")
            return False
            
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO usuarios (nombre, email, password_hash)
                VALUES (?, ?, ?)
            ''', (nombre, email, password_hash))
            self.conn.commit()
            print("Usuario registrado exitosamente!")
            return True
        except sqlite3.IntegrityError:
            print("Error: El email ya está registrado.")
            return False

    def iniciar_sesion(self, email: str, password: str) -> bool:
        email = email.strip()  # Eliminar espacios en blanco o saltos de línea
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, nombre, email, password_hash FROM usuarios WHERE email = ?', (email,))
        usuario_data = cursor.fetchone()
        
        if not usuario_data:
            print("Error: Usuario no encontrado.")
            return False
            
        usuario_id, nombre, email_db, password_hash = usuario_data
        
        if hashlib.sha256(password.encode()).hexdigest() == password_hash:
            cursor.execute('SELECT evento_id FROM favoritos WHERE usuario_id = ?', (usuario_id,))
            favoritos = [row[0] for row in cursor.fetchall()]
            
            cursor.execute('SELECT categorias_preferidas FROM usuarios WHERE id = ?', (usuario_id,))
            categorias_preferidas = cursor.fetchone()[0]
            categorias = categorias_preferidas.split(',') if categorias_preferidas else []
            
            self.usuario_actual = Usuario(usuario_id, nombre, email_db, password_hash)
            self.usuario_actual.favoritos = favoritos
            self.usuario_actual.categorias_preferidas = categorias
            
            print(f"Bienvenido, {nombre}!")
            return True
        else:
            print("Error: Contraseña incorrecta.")
            return False

    def cerrar_sesion(self):
        self.usuario_actual = None
        print("Sesión cerrada exitosamente.")

    # Métodos de eventos
    def crear_evento(self, nombre: str, ubicacion: str, fecha: str, categoria: str, 
                    capacidad: int, descripcion: str) -> bool:
        if not self.usuario_actual:
            print("Error: Debes iniciar sesión para crear un evento.")
            return False
            
        if not nombre or not ubicacion or not fecha or not categoria or capacidad <= 0:
            print("Error: Todos los campos son obligatorios y la capacidad debe ser positiva.")
            return False
            
        try:
            datetime.strptime(fecha, '%Y-%m-%d')
        except ValueError:
            print("Error: Formato de fecha inválido. Use YYYY-MM-DD.")
            return False
            
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO eventos (nombre, ubicacion, fecha, categoria, capacidad, descripcion, organizador_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (nombre, ubicacion, fecha, categoria, capacidad, descripcion, self.usuario_actual.id))
        self.conn.commit()
        
        print("Evento creado exitosamente!")
        return True

    def explorar_eventos(self, categoria: str = None, ubicacion: str = None, 
                        fecha: str = None, orden: str = 'fecha') -> List[Evento]:
        query = 'SELECT * FROM eventos WHERE 1=1'
        params = []
        
        if categoria:
            query += ' AND categoria = ?'
            params.append(categoria)
            
        if ubicacion:
            query += ' AND ubicacion LIKE ?'
            params.append(f'%{ubicacion}%')
            
        if fecha:
            query += ' AND fecha = ?'
            params.append(fecha)
            
        if orden == 'fecha':
            query += ' ORDER BY fecha'
        elif orden == 'nombre':
            query += ' ORDER BY nombre'
        elif orden == 'categoria':
            query += ' ORDER BY categoria'
            
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        
        eventos = []
        for row in cursor.fetchall():
            eventos.append(Evento(
                id=row[0],
                nombre=row[1],
                ubicacion=row[2],
                fecha=row[3],
                categoria=row[4],
                capacidad=row[5],
                descripcion=row[6],
                organizador_id=row[7]
            ))
            
        return eventos

    def agregar_favorito(self, evento_id: int) -> bool:
        if not self.usuario_actual:
            print("Error: Debes iniciar sesión para agregar favoritos.")
            return False
            
        cursor = self.conn.cursor()
        cursor.execute('SELECT id FROM eventos WHERE id = ?', (evento_id,))
        if not cursor.fetchone():
            print("Error: El evento no existe.")
            return False
            
        try:
            cursor.execute('''
                INSERT INTO favoritos (usuario_id, evento_id)
                VALUES (?, ?)
            ''', (self.usuario_actual.id, evento_id))
            self.conn.commit()
            
            if evento_id not in self.usuario_actual.favoritos:
                self.usuario_actual.favoritos.append(evento_id)
                
            print("Evento agregado a favoritos!")
            return True
        except sqlite3.IntegrityError:
            print("Este evento ya está en tus favoritos.")
            return False

    def eliminar_favorito(self, evento_id: int) -> bool:
        if not self.usuario_actual:
            print("Error: Debes iniciar sesión para eliminar favoritos.")
            return False
            
        cursor = self.conn.cursor()
        cursor.execute('''
            DELETE FROM favoritos 
            WHERE usuario_id = ? AND evento_id = ?
        ''', (self.usuario_actual.id, evento_id))
        
        if cursor.rowcount > 0:
            self.conn.commit()
            if evento_id in self.usuario_actual.favoritos:
                self.usuario_actual.favoritos.remove(evento_id)
            print("Evento eliminado de favoritos.")
            return True
        else:
            print("Este evento no estaba en tus favoritos.")
            return False

    def obtener_favoritos(self) -> List[Evento]:
        if not self.usuario_actual:
            return []
            
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT e.* FROM eventos e
            JOIN favoritos f ON e.id = f.evento_id
            WHERE f.usuario_id = ?
        ''', (self.usuario_actual.id,))
        
        return [
            Evento(
                id=row[0],
                nombre=row[1],
                ubicacion=row[2],
                fecha=row[3],
                categoria=row[4],
                capacidad=row[5],
                descripcion=row[6],
                organizador_id=row[7]
            ) for row in cursor.fetchall()
        ]

    # Notificaciones y recomendaciones
    def verificar_recordatorios(self):
        if not self.usuario_actual:
            return
            
        hoy = datetime.now().strftime('%Y-%m-%d')
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT e.* FROM eventos e
            JOIN favoritos f ON e.id = f.evento_id
            WHERE f.usuario_id = ? 
            AND e.fecha BETWEEN ? AND date(?, '+3 days')
        ''', (self.usuario_actual.id, hoy, hoy))
        
        eventos_proximos = cursor.fetchall()
        
        if eventos_proximos:
            print("\n=== RECORDATORIOS ===")
            for evento in eventos_proximos:
                print(f"¡No olvides el evento '{evento[1]}' el {evento[3]}!")
            print("===================\n")

    def obtener_recomendaciones(self) -> List[Evento]:
        if not self.usuario_actual or not self.usuario_actual.categorias_preferidas:
            return []
            
        hoy = datetime.now().strftime('%Y-%m-%d')
        categorias = self.usuario_actual.categorias_preferidas
        
        cursor = self.conn.cursor()
        query = '''
            SELECT e.* FROM eventos e
            WHERE e.categoria IN ({})
            AND e.fecha >= ?
            AND e.id NOT IN (
                SELECT evento_id FROM favoritos 
                WHERE usuario_id = ?
            )
            ORDER BY e.fecha
            LIMIT 5
        '''.format(','.join(['?']*len(categorias)))
        
        params = categorias + [hoy, self.usuario_actual.id]
        cursor.execute(query, params)
        
        return [
            Evento(
                id=row[0],
                nombre=row[1],
                ubicacion=row[2],
                fecha=row[3],
                categoria=row[4],
                capacidad=row[5],
                descripcion=row[6],
                organizador_id=row[7]
            ) for row in cursor.fetchall()
        ]

    def agregar_categoria_preferida(self, categoria: str):
        if not self.usuario_actual:
            print("Error: Debes iniciar sesión para agregar categorías preferidas.")
            return False

        if categoria not in self.usuario_actual.categorias_preferidas:
            self.usuario_actual.categorias_preferidas.append(categoria)
            categorias_str = ','.join(self.usuario_actual.categorias_preferidas)
            cursor = self.conn.cursor()
            cursor.execute('''
                UPDATE usuarios 
                SET categorias_preferidas = ?
                WHERE id = ?
            ''', (categorias_str, self.usuario_actual.id))
            self.conn.commit()
            print(f"Categoría '{categoria}' agregada a tus preferencias.")
            return True
        else:
            print(f"La categoría '{categoria}' ya está en tus preferencias.")
            return False

    # Métodos auxiliares
    def obtener_evento_por_id(self, evento_id: int) -> Optional[Evento]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM eventos WHERE id = ?', (evento_id,))
        row = cursor.fetchone()
        
        if row:
            return Evento(
                id=row[0],
                nombre=row[1],
                ubicacion=row[2],
                fecha=row[3],
                categoria=row[4],
                capacidad=row[5],
                descripcion=row[6],
                organizador_id=row[7]
            )
        return None

    def obtener_organizador_nombre(self, organizador_id: int) -> str:
        cursor = self.conn.cursor()
        cursor.execute('SELECT nombre FROM usuarios WHERE id = ?', (organizador_id,))
        row = cursor.fetchone()
        return row[0] if row else "Desconocido"