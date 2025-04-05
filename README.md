# QueHayPaHacer
# 1. Descripción del Problema
En la actualidad, muchas personas buscan actividades y eventos en su ciudad, pero la información está dispersa en redes sociales, sitios web y grupos de mensajería. Esto dificulta la organización y el descubrimiento de planes interesantes.
"QuéHayPaHacer?" es una aplicación diseñada para centralizar y facilitar el acceso a eventos y actividades, permitiendo a los usuarios explorar opciones según sus intereses y ubicación.
# 2. Análisis del Problema
## 2.1 Requisitos Funcionales
Los requisitos funcionales del sistema incluyen:
1.	**Registro y autenticación de usuarios:** Los usuarios deben poder registrarse e iniciar sesión.
2.	**Publicación de eventos:** Los organizadores pueden crear eventos con detalles como nombre, ubicación, fecha y categoría.
3.	**Exploración de eventos:** Los usuarios pueden buscar eventos según filtros como categoría, ubicación y fecha.
4.	**Guardado de eventos:** Los usuarios pueden marcar eventos como favoritos.
5.	**Notificaciones y recordatorios:** Se pueden enviar alertas sobre eventos guardados o recomendados.
6.	**(Requisito innovador):** Usar aprendizaje automático para sugerir eventos según las preferencias del usuario.
7.	**Integración con mapas:** Mostrar ubicación de eventos mediante una API de mapas.
2.2 Modelo del Mundo del Problema
El sistema se puede modelar con las siguientes clases principales:
*	Usuario: Representa a un usuario registrado con atributos como nombre, email y eventos guardados.
*	Evento: Contiene información del evento, como nombre, ubicación, fecha y organizador.
*	Organizador: Un usuario especial que puede crear eventos.
*	Categoría: Representa diferentes tipos de eventos, como conciertos, deportes o conferencias.
* 	Sistema: Administra los eventos y usuarios registrados.
El diagrama de clases UML representará la relación entre estas clases.
# 3. Implementación del Modelo del Mundo
Se implementará una versión inicial del sistema en Python con una interfaz de consola que permita:
*	Registrar y listar eventos.
*	Buscar eventos según filtros.
*	Guardar eventos como favoritos.