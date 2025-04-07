import hashlib
from typing import List

class Usuario:
    def __init__(self, id: int, nombre: str, email: str, password_hash: str):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password_hash = password_hash
        self.favoritos: List[int] = []
        self.categorias_preferidas: List[str] = []

    def verificar_password(self, password: str) -> bool:
        return hashlib.sha256(password.encode()).hexdigest() == self.password_hash

    def agregar_favorito(self, evento_id: int):
        if evento_id not in self.favoritos:
            self.favoritos.append(evento_id)

    def eliminar_favorito(self, evento_id: int):
        if evento_id in self.favoritos:
            self.favoritos.remove(evento_id)

    def agregar_categoria_preferida(self, categoria: str):
        if categoria not in self.categorias_preferidas:
            self.categorias_preferidas.append(categoria)