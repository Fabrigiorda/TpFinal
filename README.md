# TP Final
El trabajo consta de realizar el backend para la gestión de inventario y pedidos de una tienda de cómics, implementado como una aplicación de consola en Python.

# Descripción del Proyecto
Este proyecto desarrolla backend para la tienda de cómics "Nadie se salva solo". El sistema gestiona el inventario de productos, procesa pedidos de clientes en orden de llegada, mantiene un historial de los últimos productos vistos y organiza el catálogo en una jerarquía de categorías navegable.

# Instrucciones de Ejecución
1.  Asegurarse de tener Python 3.x instalado
2.  Tener los archivos `basedatos.csv`, `pedidos.json` y `historial.json` en el mismo directorio
3.  Abrir una terminal en la carpeta del proyecto
4.  Ejecutar el script: python main.py
5.  Navegar por el menú y usar la aplicacion

# Diseño y Estructuras de Datos
# 1. Gestión de Productos (Hash Table)
Requerimiento: Búsqueda, actualización y eliminación de productos por SKU de forma eficiente.
Implementación: Se creó una clase `TablaHashSimple` (Tabla Hash).
Justificación: Las funciones `buscar_producto_con_hash` y `eliminar_producto_con_hash` utilizan esta tabla. Indexar por SKU permite que las búsquedas (`obtener`) tengan una complejidad promedio de O(1)

# 2. Procesamiento de Pedidos (Queue)
Requerimiento: Procesar pedidos en el estricto orden en que fueron recibidos (FIFO).
Implementación: Se utiliza un archivo `pedidos.json` que es tratado como una cola.
Justificación: `agregar_pedido` añade al final de la lista (`.append()`). `procesar_pedido` lee y elimina del inicio (`.pop(0)`).

# 3. Historial de Últimos Productos Vistos (Queue / Lista)
Requerimiento: Mantener un historial de los últimos 5 productos vistos (eliminando el más antiguo).
Implementación: Se utiliza una lista (`historial_busqueda`) y el archivo `historial.json`.
Justificación: El requerimiento de "eliminar el más antiguo" describe una cola (FIFO). Al buscar, se añade al final (`.append()`) y si `len > 5`, se elimina el primero (`.pop(0)`).

# 4. Categorización Jerárquica (Tree)
Requerimiento: Organizar productos en una jerarquía (ej. `Cómics -> DC -> Batman`).
Implementación: Se creó una clase `NodoArbol`.
Justificación: La función `cargar_arbol_categorias` construye un árbol en memoria. `obtener_productos_recursivo` permite consultar un nodo y todos sus descendientes.