# Importación de librerías necesarias para manejo de archivos, tiempo, CSV y JSON
import os, time, csv, json

# Variables globales para almacenar el estado del programa
productos = {}
lista_pedidos = []
historial_busqueda = []

# Archivo que guarda el historial de búsquedas persistente
archivo_historial = 'historial.json'
try:
    
    if os.path.exists(archivo_historial) and os.path.getsize(archivo_historial) > 0:
        with open(archivo_historial, 'r', encoding='utf-8') as f:
            # Carga el historial desde JSON y valida que sea una lista
            historial_busqueda = json.load(f)
            
            if not isinstance(historial_busqueda, list):
                historial_busqueda = []
    else:
        # Si no existe el archivo, inicializa un historial vacío
        historial_busqueda = []
except (json.JSONDecodeError, FileNotFoundError):
    
    historial_busqueda = []

# Estructura de árbol para organizar productos por categorías
class NodoArbol:
    def __init__(self, nombre):
        self.nombre = nombre
        self.hijos = {}
        self.productos = []

# Nodo raíz del árbol de categorías
raiz_categorias = NodoArbol("Categorías")

# Construye el árbol de categorías desde el archivo CSV
def cargar_arbol_categorias(nombre_archivo='basedatos.csv'):
    global raiz_categorias
    raiz_categorias = NodoArbol("Categorías")
    try:
        with open(nombre_archivo, mode='r', encoding='utf-8', newline='') as f:
            # Verifica si existe la columna de categoría en el CSV
            lector = csv.DictReader(f)
            if 'categoria' not in lector.fieldnames:
                return
            
            # Procesa cada producto y lo asigna a su categoría
            for fila in lector:
                # Normaliza las categorías vacías
                ruta_categoria = fila.get('categoria', '').strip()
                if not ruta_categoria:
                    ruta_categoria = "SIN CATEGORIA"

                # Divide la ruta de categorías y crea los nodos necesarios
                partes = ruta_categoria.split('/')
                nodo_actual = raiz_categorias
                
                # Construye la rama del árbol para esta categoría
                for parte in partes:
                    if parte not in nodo_actual.hijos:
                        nodo_actual.hijos[parte] = NodoArbol(parte)
                    nodo_actual = nodo_actual.hijos[parte]
                
                # Almacena el producto en su categoría correspondiente
                nodo_actual.productos.append(fila)
                
    except FileNotFoundError:
        pass
    except Exception:
        pass

# Recolecta recursivamente todos los productos de un nodo y sus subárboles
def obtener_productos_recursivo(nodo):
    lista_productos = []
    lista_productos.extend(nodo.productos)
    for hijo in nodo.hijos.values():
        lista_productos.extend(obtener_productos_recursivo(hijo))
    return lista_productos

# Menú principal con las operaciones fundamentales del sistema
def menu():
    os.system("cls")
    print("Menu:")
    print("1. Gestión de Productos")
    print("2. Procesar pedidos")
    print("3. Historial")
    print("4. Explorar Categorías")
    print("5. Salir")
    try:
        entrada = input("Elija una opcion: ")
        respuesta = int(entrada)

    except ValueError:
        print("Entrada no valida, Ingrese unicamente un numero")
        time.sleep(1)
        os.system("cls")
        menu()

    # Chequeo de que respuesta fue la elegida por el usuario
    if respuesta == 1:
        gestion_productos()
    elif respuesta == 2:
        pedidos()
    elif respuesta == 3:
        historial()
    elif respuesta == 4:
        explorar()
    elif respuesta == 5:
        exit()
    else:
        print("Elija una opcion valida")
        time.sleep(1)
        menu()

# Gestión CRUD de productos en el inventario
def gestion_productos():
    os.system("cls")
    print("1. Agregar producto")
    print("2. Actualizar producto")
    print("3. Buscar Producto (Mediante SKU)")
    print("4. Eliminar Producto (Mediante SKU)")
    print("5. Volver")
    try:
        entrada = input("Elija una opcion: ")
        respuesta = int(entrada)

    except ValueError:
        print("Entrada no valida, Ingrese unicamente un numero")
        time.sleep(1)
        os.system("cls")
        gestion_productos()

    if respuesta == 1:
        agregar_producto()
    elif respuesta == 2:
        actualizar_producto()
    elif respuesta == 3:
        buscar_producto_con_hash()
    elif respuesta == 4:
        eliminar_producto_con_hash()
    elif respuesta == 5:
        menu()
    else:
        print("Elija una opcion valida")
        time.sleep(1)
        gestion_productos()

# Agrega un nuevo producto al archivo CSV con validación de duplicados
def agregar_producto():
    os.system("cls")
    nuevo = []
    lista_nombres = []
    lista_sku = []
    nuevo_nombre = ""
    sku = ""
    archivo = "basedatos.csv"
    ultimo_id = 0

    try:
        # Lee el archivo CSV existente para obtener el último ID
        with open(archivo, mode='r', newline='', encoding='utf-8') as archivo_csv:
            buscar = csv.DictReader(archivo_csv)
            for fila in buscar:
                if fila.get("id"):
                    ultimo_id = int(fila["id"])
                    lista_nombres.append(fila["nombre"].upper())
                    lista_sku.append(fila["sku"].upper())
    except FileNotFoundError:
        pass
    except Exception:
        pass

    # Asignacion automatica de ID
    nuevo_id = ultimo_id + 1

    # Solicita y valida que el nombre no exista
    nuevo_nombre = input("Ingrese nombre del producto: ").upper()
    while nuevo_nombre in lista_nombres:
        nuevo_nombre = input("Ese producto ya existe, ingrese uno nuevo: ").upper()

    precio = input("Ingrese el precio del objeto: $")
    stock = input("Ingrese la cantidad de productos disponibles: ")

    sku = input("Asigne un SKU para el producto: ").upper()
    while sku in lista_sku:
        sku = input("Ese SKU ya existe, asigne uno nuevo: ").upper()
    
    categoria = input("Ingrese la categoria (ej: COMICS/MARVEL/SPIDER-MAN): ").upper()


    nuevo.append(nuevo_id)
    nuevo.append(nuevo_nombre)
    nuevo.append(stock)
    nuevo.append(precio)
    nuevo.append(sku)
    nuevo.append(categoria)
    
    archivo_existe = os.path.isfile(archivo)
    
    nombres_columnas = ["id", "nombre", "stock", "precio", "sku", "categoria"]

    with open(archivo, 'a', newline='', encoding='utf-8') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        if not archivo_existe or os.path.getsize(archivo) == 0:
             escritor_csv.writerow(nombres_columnas)
        escritor_csv.writerow(nuevo)

# Actualiza la información de un producto existente usando un archivo temporal
def actualizar_producto():
    nombre_archivo = 'basedatos.csv'
    archivo_temporal = 'temp_basedatos.csv'
    nombres_columnas = ["id", "nombre", "stock", "precio", "sku", "categoria"]

    os.system("cls")
    print("Modificar Producto por SKU")
    sku_a_buscar = input("Ingrese el SKU del producto que desea modificar: ")

    try:
        datos_actualizados = []
        producto_encontrado = False

        with open(nombre_archivo, 'r', newline='', encoding='utf-8') as archivo_lectura:
            lector = csv.reader(archivo_lectura)

            # Preserva la cabecera del CSV y añade columna de categoría si falta
            cabecera = next(lector)
            if 'categoria' not in cabecera:
                cabecera.append('categoria')
            datos_actualizados.append(cabecera)
            
            indice_sku = 4
            indice_categoria = 5

            for fila in lector:
                if len(fila) <= indice_sku:
                    datos_actualizados.append(fila)
                    continue
                
                
                while len(fila) <= indice_categoria:
                    fila.append("")

                # Inputs para que el usuario haga las modificaciones correspondientes/necesarias para el producto
                if fila[indice_sku].upper() == sku_a_buscar.upper():
                    producto_encontrado = True
                    print(f"\nProducto encontrado: ID={fila[0]}, Nombre={fila[1]}, Stock={fila[2]}, Precio={fila[3]}, SKU={fila[4]}, Categoria={fila[5]}")
                    print("Por favor, ingrese los nuevos datos.")

                    nuevo_nombre = input("Nuevo nombre: ")
                    nuevo_stock = input("Nuevo stock: ")
                    nuevo_precio = input("Nuevo precio: ")
                    nuevo_SKU = input("Nuevo SKU: ")
                    nuevo_categoria = input("Nueva Categoria (ej: COMICS/MARVEL): ")

                    fila[1] = nuevo_nombre.upper()
                    fila[2] = nuevo_stock
                    fila[3] = nuevo_precio
                    fila[4] = nuevo_SKU.upper()
                    fila[5] = nuevo_categoria.upper()
                datos_actualizados.append(fila)
                
        if producto_encontrado:
            with open(archivo_temporal, 'w', newline='', encoding='utf-8') as archivo_escritura:
                escritor = csv.writer(archivo_escritura)
                escritor.writerows(datos_actualizados)

            os.replace(archivo_temporal, nombre_archivo)
            print(f"\n¡Éxito! El producto '{sku_a_buscar}' ha sido actualizado.")
            time.sleep(2)
            gestion_productos()
        else:
            print(f"\nNo se encontró ningún producto con el SKU '{sku_a_buscar}'.")

    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no fue encontrado.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

# Menú de gestión de pedidos (crear y procesar)
def pedidos():
    
    os.system("cls")
    print("Gestión de Pedidos")
    print("1. Hacer pedido")
    print("2. Procesar pedido")
    print("3. Volver")

    try:
        entrada = input("Elija una opcion: ")
        respuesta = int(entrada)   
    except ValueError:
        print("Error. Ingrese una opcion valida")
        time.sleep(1)
        os.system("cls")
        pedidos()
    if respuesta == 1:
        agregar_pedido()
    elif respuesta == 2:
        procesar_pedido()
    elif respuesta == 3:
        menu()
    else:
        print("Elija una opcion valida")
        time.sleep(1)
        pedidos()
        
# Crea un nuevo pedido con validación de stock y cálculo de totales
def agregar_pedido():
    import json
    os.system("cls")
    nombre_cliente = input("Ingrese su nombre: ")
    if not nombre_cliente:
        print("El nombre no puede estar vacío. Volviendo...")
        time.sleep(1)
        pedidos()
        return

    pedido_actual = []
    nombre_archivo = 'basedatos.csv'

    while True:
        os.system("cls")
        print(f"Creando pedido para: {nombre_cliente}")
        
        total_pedido_actual = 0
        # Valida si hay productos en el pedido actual
        if not pedido_actual:
            print("El pedido está vacío.")
        else:
            # Muestra resumen del pedido con subtotales
            print("Productos en este pedido:")
            for i, item in enumerate(pedido_actual, 1):
                subtotal_item = item['cantidad'] * item['precio_unitario']
                total_pedido_actual += subtotal_item
                print(f"  {i}. {item['producto']} (x{item['cantidad']}) - ${item['precio_unitario']:.2f} c/u = ${subtotal_item:.2f}")
            print("-" * 30)
            print(f"Total actual: ${total_pedido_actual:.2f}")

        print("\nOpciones:")
        print("1. Agregar producto")
        print("2. Modificar pedido")
        print("3. Finalizar pedido (FIN)")
        print("4. Cancelar pedido (CANCELAR)")
        
        opcion_menu = input("Elija una opcion: ").strip().upper()

        if opcion_menu == '4' or opcion_menu == 'CANCELAR':
            print("Pedido cancelado.")
            time.sleep(1)
            pedidos()
            return
        
        if opcion_menu == '3' or opcion_menu == 'FIN':
            if not pedido_actual:
                print("No se agregaron productos. Volviendo al menú.")
                time.sleep(1)
                pedidos()
                return
            break
        
        if opcion_menu == '2':
            if not pedido_actual:
                print("No hay productos para modificar.")
                time.sleep(1)
                continue
            
            while True:
                os.system("cls")
                print("Modificar Pedido:")
                total_pedido_actual = 0
                for i, item in enumerate(pedido_actual, 1):
                    subtotal_item = item['cantidad'] * item['precio_unitario']
                    total_pedido_actual += subtotal_item
                    print(f"  {i}. {item['producto']} (x{item['cantidad']}) - ${item['precio_unitario']:.2f} c/u")
                print(f"\nTotal actual: ${total_pedido_actual:.2f}")
                print("Ingrese el número del producto a modificar, 'E' (eliminar todo) o 'V' (volver):")
                
                opcion_mod = input("Opción: ").strip().upper()

                if opcion_mod == 'V':
                    break
                
                if opcion_mod == 'E':
                    confirmar_borrado = input("¿Seguro que desea vaciar el pedido? (S/N): ").upper()
                    if confirmar_borrado == 'S':
                        pedido_actual = []
                        print("Pedido vaciado.")
                        time.sleep(1)
                        break
                    else:
                        continue

                try:
                    indice_modificar = int(opcion_mod) - 1
                    if 0 <= indice_modificar < len(pedido_actual):
                        item_a_modificar = pedido_actual[indice_modificar]
                        print(f"Modificando: {item_a_modificar['producto']}")
                        print("[1] Modificar cantidad")
                        print("[2] Eliminar producto")
                        print("[0] Volver")
                        opcion_item = input("Opción: ").strip()

                        if opcion_item == '0':
                            continue
                        
                        elif opcion_item == '2':
                            confirmar_borrado_item = input(f"¿Eliminar {item_a_modificar['producto']}? (S/N): ").upper()
                            if confirmar_borrado_item == 'S':
                                pedido_actual.pop(indice_modificar)
                                print("Producto eliminado.")
                                time.sleep(1)
                    
                        
                        elif opcion_item == '1':
                            try:
                                nueva_cantidad_texto = input(f"Ingrese nueva cantidad (actual: {item_a_modificar['cantidad']}): ")
                                nueva_cantidad = int(nueva_cantidad_texto)
                                
                                if nueva_cantidad <= 0:
                                    print("La cantidad debe ser positiva. Para eliminar, use la opción 2.")
                                    time.sleep(1.5)
                                    continue

                                stock_disponible = 0
                                try:
                                    with open(nombre_archivo, mode='r', encoding='utf-8', newline='') as f:
                                        lector = csv.DictReader(f)
                                        for fila in lector:
                                            if fila['nombre'].upper() == item_a_modificar['producto']:
                                                stock_disponible = int(fila.get('stock', 0))
                                                break
                                except Exception as e:
                                    print(f"Error al verificar stock: {e}")
                                    time.sleep(1.5)
                                    continue
                                
                                if nueva_cantidad > stock_disponible:
                                    print(f"Stock insuficiente. Disponible: {stock_disponible}")
                                    time.sleep(1.5)
                                else:
                                    item_a_modificar['cantidad'] = nueva_cantidad
                                    print("Cantidad actualizada.")
                                    time.sleep(1)

                            except ValueError:
                                print("Cantidad no válida.")
                                time.sleep(1)
                    else:
                        print("Número de producto no válido.")
                        time.sleep(1)
                except ValueError:
                    print("Opción no válida.")
                    time.sleep(1)

        elif opcion_menu == '1':
            nombre_producto_texto = input("Ingrese nombre del producto (o 'V' para volver): ").upper()

            if nombre_producto_texto == 'V':
                continue
            
            if not nombre_producto_texto:
                print("El nombre del producto no puede estar vacío.")
                time.sleep(1)
                continue

            producto_encontrado = False
            datos_producto = {}

            
            try:
                with open(nombre_archivo, mode='r', encoding='utf-8', newline='') as f:
                    lector = csv.DictReader(f)
                    for fila in lector:
                        if fila['nombre'].upper() == nombre_producto_texto:
                            datos_producto = {
                                "nombre": fila['nombre'].upper(),
                                "stock": int(fila.get('stock', 0)),
                                "precio": float(fila.get('precio', 0.0)),
                                "sku": fila['sku']
                            }
                            producto_encontrado = True
                            break
            except FileNotFoundError:
                print(f"Error: No se pudo encontrar el archivo '{nombre_archivo}'.")
                time.sleep(1.5)
                continue
            except Exception as e:
                print(f"Ocurrió un error al leer la base de datos: {e}")
                time.sleep(1.5)
                continue

            if not producto_encontrado:
                print(f"Producto '{nombre_producto_texto}' inexistente.")
                time.sleep(1.5)
                continue

            if datos_producto['stock'] <= 0:
                print(f"Producto '{datos_producto['nombre']}' sin stock.")
                time.sleep(1.5)
                continue

            os.system("cls")
            print(f"Producto: {datos_producto['nombre']}")
            print(f"Precio unitario: ${datos_producto['precio']:.2f}")
            print(f"Stock disponible: {datos_producto['stock']}")
            
            cantidad_texto = input("Ingrese la cantidad (o 'V' [Volver], 'C' [Cancelar Pedido]): ").upper()

            if cantidad_texto == 'V':
                continue
            if cantidad_texto == 'C':
                print("Pedido cancelado.")
                time.sleep(1)
                pedidos()
                return

            try:
                cantidad_deseada = int(cantidad_texto)
                if cantidad_deseada <= 0:
                    print("La cantidad debe ser un número positivo.")
                    time.sleep(1)
                    continue
            except ValueError:
                print("Cantidad no válida. Debe ingresar un número.")
                time.sleep(1)
                continue

            cantidad_en_carrito = 0
            item_existente = None
            for item in pedido_actual:
                if item['producto'] == datos_producto['nombre']:
                    cantidad_en_carrito = item['cantidad']
                    item_existente = item
                    break
            
            cantidad_total_requerida = cantidad_en_carrito + cantidad_deseada

            if cantidad_total_requerida > datos_producto['stock']:
                print(f"NO se pudo realizar la compra: Stock insuficiente.")
                print(f"Stock disponible: {datos_producto['stock']}. Total requerido: {cantidad_total_requerida}")
                time.sleep(2)
            else:
                if item_existente:
                    item_existente['cantidad'] = cantidad_total_requerida
                else:
                    pedido_actual.append({
                        "producto": datos_producto['nombre'], 
                        "sku": datos_producto['sku'],
                        "cantidad": cantidad_deseada, 
                        "precio_unitario": datos_producto['precio']
                    })
                
                print(f"Producto '{datos_producto['nombre']}' (x{cantidad_deseada}) agregado/actualizado.")
                time.sleep(1.5)
        
        else:
            print("Opción no válida.")
            time.sleep(1)


    total_compra = sum(item['cantidad'] * item['precio_unitario'] for item in pedido_actual)
    
    nuevo_pedido_completo = {
        "cliente": nombre_cliente,
        "items": pedido_actual,
        "total": total_compra
    }
    
    archivo_pedidos_json = "pedidos.json"
    lista_total_pedidos = []
    
    try:
        if os.path.exists(archivo_pedidos_json) and os.path.getsize(archivo_pedidos_json) > 0:
            with open(archivo_pedidos_json, 'r', encoding='utf-8') as f:
                lista_total_pedidos = json.load(f)
                if not isinstance(lista_total_pedidos, list):
                    lista_total_pedidos = []
        else:
            lista_total_pedidos = []
    except json.JSONDecodeError:
        lista_total_pedidos = []
    except Exception:
        lista_total_pedidos = [] 

    lista_total_pedidos.append(nuevo_pedido_completo)

    try:
        with open(archivo_pedidos_json, 'w', encoding='utf-8') as f:
            json.dump(lista_total_pedidos, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error al guardar en {archivo_pedidos_json}: {e}")
        time.sleep(2)

    os.system("cls")
    print("Pedido finalizado y guardado en el historial.")
    print("\nResumen del Pedido:")
    print(f"Cliente: {nombre_cliente}")
    for item in pedido_actual:
        subtotal_item = item['cantidad'] * item['precio_unitario']
        print(f"  - {item['producto']} (x{item['cantidad']}) @ ${item['precio_unitario']:.2f} c/u = ${subtotal_item:.2f}")
    
    print("-" * 30)
    print(f"TOTAL DE LA COMPRA: ${total_compra:.2f}")
    
    input("\nPresione Enter para volver al menú de pedidos...")
    pedidos()

# Procesa el siguiente pedido en la cola (FIFO) y actualiza el inventario
def procesar_pedido():
    os.system("cls")
    archivo_pedidos_json = 'pedidos.json'
    archivo_base_datos = 'basedatos.csv'
    
    # Cargar la lista de pedidos desde el archivo JSON
    try:
        if not os.path.exists(archivo_pedidos_json) or os.path.getsize(archivo_pedidos_json) == 0:
            print("No hay pedidos para procesar.")
            time.sleep(2)
            pedidos()
            return
    
        with open(archivo_pedidos_json, 'r', encoding='utf-8') as f:
            lista_pedidos = json.load(f)
            if not lista_pedidos:
                print("No hay pedidos para procesar.")
                time.sleep(2)
                pedidos()
                return


    except (json.JSONDecodeError, FileNotFoundError):
        print("Error al leer la cola de pedidos. El archivo puede estar corrupto.")
        time.sleep(2)
        pedidos()
        return

    
    print(f"Pedidos totales en cola: {len(lista_pedidos)}")
    
    primer_pedido = lista_pedidos[0] 
        
    print("\n--- Procesando Siguiente Pedido (FIFO) ---")
    print(f"Cliente: {primer_pedido['cliente']}")
    print(f"Total: ${primer_pedido['total']:.2f}")
    print("Items del pedido:")
    for item in primer_pedido['items']:
        print(f"  - {item['producto']} (SKU: {item['sku']}) x{item['cantidad']}")
    print("------------------------------------------")
    input("Presione Enter para confirmar el procesamiento...")

    inventario = {}
    nombres_columnas = []
    
    # Cargar el inventario desde el archivo CSV
    try:
        with open(archivo_base_datos, mode='r', encoding='utf-8', newline='') as f:
            lector = csv.DictReader(f)
            nombres_columnas = lector.fieldnames
            if not nombres_columnas:
                print(f"Error CRÍTICO: El archivo '{archivo_base_datos}' está vacío o corrupto.")
                time.sleep(3)
                pedidos()
                return
            for fila in lector:
                inventario[fila['sku']] = fila
    except FileNotFoundError:
        print(f"Error CRÍTICO: No se encontró el archivo de base de datos '{archivo_base_datos}'.")
        time.sleep(3)
        pedidos()
        return
    except Exception as e:
        print(f"Error al leer la base de datos: {e}")
        time.sleep(2)
        pedidos()
        return

    stock_suficiente = True
    items_a_procesar = primer_pedido['items']
    
    for item in items_a_procesar:
        sku = item['sku']
        cantidad_pedida = item['cantidad']
        
        if sku not in inventario:
            print(f"ERROR: Producto '{item['producto']}' (SKU: {sku}) ya no existe.")
            stock_suficiente = False
            break 
        
        try:
            # Verifica el stock antes de procesar el pedido
            stock_actual = int(inventario[sku]['stock'])
        except (ValueError, TypeError):
            print(f"ERROR: Stock inválido para SKU {sku} en basedatos.csv.")
            stock_actual = 0

        
        # Valida que haya suficiente stock para el pedido
        if cantidad_pedida > stock_actual:
            print(f"ERROR: Stock insuficiente para '{item['producto']}' (SKU: {sku}).")
            print(f"   Pedido: {cantidad_pedida} | Disponible: {stock_actual}")
            stock_suficiente = False
            break 

    # Actualiza el inventario si hay suficiente stock
    if stock_suficiente:
        print("\nStock verificado. Actualizando inventario...")
        for item in items_a_procesar:
            sku = item['sku']
            cantidad_pedida = item['cantidad']
            
            # Reduce el stock del producto
            stock_actual = int(inventario[sku]['stock'])
            nuevo_stock = stock_actual - cantidad_pedida
            inventario[sku]['stock'] = str(nuevo_stock)
        
        try:
            with open(archivo_base_datos, 'w', encoding='utf-8', newline='') as f:
                escritor = csv.DictWriter(f, fieldnames=nombres_columnas)
                escritor.writeheader()
                escritor.writerows(inventario.values())
        except Exception as e:
            print(f"Error CRÍTICO al guardar el inventario: {e}")
            time.sleep(3)
            pedidos()
            return
        
        print(f"Inventario actualizado en 'basedatos.csv'.")

    else:
        print("\nEl pedido no puede ser procesado por falta de stock.")


    pedido_procesado = lista_pedidos.pop(0) 
    
    try:
        with open(archivo_pedidos_json, 'w', encoding='utf-8') as f:
            json.dump(lista_pedidos, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error CRÍTICO al actualizar la cola de pedidos: {e}")
        time.sleep(3)
        pedidos()
        return

    if stock_suficiente:
        print(f"\nPedido de {pedido_procesado['cliente']} procesado y eliminado de la cola.")
    else:
        print(f"\nPedido de {pedido_procesado['cliente']} no procesado y eliminado de la cola.")

    print(f"Pedidos restantes: {len(lista_pedidos)}")
    input("\nPresione Enter para volver...")
    pedidos()
    







# Función para mostrar el historial de búsquedas
def historial():
    os.system("cls") 
    print("Historial de busquedas:")


    if not historial_busqueda:
        print("\nNo hay búsquedas en el historial.")
    else:
        
        for i, producto in enumerate(historial_busqueda, start=1):
            print(f"\nBusqueda {i}:")
            
            for clave, valor in producto.items():
                print(f"  {clave}: {valor}")
            print("-" * 20)
    
    input("\nPresione Enter para volver al menú...")
    menu()

# Permite navegar el árbol de categorías y ver productos
def explorar():
    cargar_arbol_categorias()
    nodo_actual = raiz_categorias
    pila_ruta = [raiz_categorias]

    while True:
        os.system("cls")
        ruta_actual_str = " / ".join(n.nombre for n in pila_ruta)
        print(f"Explorando: {ruta_actual_str}\n")

        print("--- Subcategorías ---")
        subcategorias = list(nodo_actual.hijos.keys())
        if not subcategorias:
            print("No hay subcategorías.")
        else:
            for i, nombre in enumerate(subcategorias, 1):
                print(f"{i}. {nombre}")
        
        print("\n--- Productos en esta y subcategorías ---")
        todos_los_productos = obtener_productos_recursivo(nodo_actual)
        if not todos_los_productos:
            print("No hay productos.")
        else:
            for prod in todos_los_productos:
                print(f"- {prod['nombre']} (SKU: {prod['sku']}, Stock: {prod['stock']})")

        print("\n" + "-"*30)
        print("Ingrese un NÚMERO para entrar a una subcategoría.")
        print("Ingrese '..' para subir un nivel.")
        print("Ingrese '0' para volver al menú principal.")
        
        opcion = input("Opción: ").strip().lower()

        if opcion == '0':
            menu()
            return
        elif opcion == '..':
            if len(pila_ruta) > 1:
                pila_ruta.pop()
                nodo_actual = pila_ruta[-1]
            else:
                print("Ya estás en la raíz.")
                time.sleep(1)
        else:
            try:
                indice_opcion = int(opcion) - 1
                if 0 <= indice_opcion < len(subcategorias):
                    nombre_categoria_elegida = subcategorias[indice_opcion]
                    nodo_actual = nodo_actual.hijos[nombre_categoria_elegida]
                    pila_ruta.append(nodo_actual)
                else:
                    print("Número fuera de rango.")
                    time.sleep(1)
            except ValueError:
                print("Opción no válida.")
                time.sleep(1)

# Implementación de tabla hash para búsquedas eficientes por SKU
class TablaHashSimple:

    # Inicializa la tabla hash con un tamaño predeterminado
    def __init__(self, tamano=1000):
        self.tamano = tamano
        self.cubetas = [[] for _ in range(tamano)]

    # Calcula el índice de la cubeta usando los valores ASCII de la clave
    def funcion_hash(self, clave):
        # Calcula un índice basado en la suma de valores ASCII de los caracteres
        return sum(ord(caracter) for caracter in str(clave)) % self.tamano

    # Inserta o actualiza un valor en la tabla hash
    def insertar(self, clave, valor_datos):
        # Obtiene la cubeta correspondiente a la clave
        indice = self.funcion_hash(clave)
        cubeta = self.cubetas[indice]
        
        # Actualiza el valor si la clave ya existe
        for i, (clave_existente, _) in enumerate(cubeta):
            if clave_existente == clave:
                cubeta[i] = (clave, valor_datos)
                return
        
        # Agrega nueva entrada si la clave no existe
        cubeta.append((clave, valor_datos))

    # Recupera un valor de la tabla hash por su clave
    def obtener(self, clave):
        indice = self.funcion_hash(clave)
        cubeta = self.cubetas[indice]
        
        for clave_existente, valor_datos in cubeta:
            if clave_existente == clave:
                return valor_datos 
        return None

# Busca productos por SKU usando la tabla hash y guarda en historial
def buscar_producto_con_hash(nombre_archivo='basedatos.csv', sku_columna='sku'):
    os.system("cls")
    mapa_productos = TablaHashSimple()
    
    # Cargar productos en la tabla hash
    try:
        with open(nombre_archivo, mode='r', encoding='utf-8', newline='') as f:
            lector = csv.DictReader(f)
            
            nombres_columnas = lector.fieldnames or []
            if not nombres_columnas:
                print(f"Error: El archivo '{nombre_archivo}' está vacío o no tiene cabecera.")
                time.sleep(1)
                return
            
            if sku_columna not in nombres_columnas:
                print(f"Error: La columna '{sku_columna}' no se encontró en '{nombre_archivo}'.")
                print(f"Columnas disponibles: {', '.join(nombres_columnas)}")
                return

            # Se desplaza a traves de las filas para insertar en la tabla hash    
            for fila in lector:
                clave_sku = fila.get(sku_columna, "").strip()
                if clave_sku:
                    mapa_productos.insertar(clave_sku, fila)

    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{nombre_archivo}'.")
        return
    except Exception as e:
        print(f"Ocurrió un error inesperado al leer el archivo: {e}")
        return
    
    sku_a_buscar = input("Ingrese el SKU del producto a buscar o 0 para volver al menu: ").upper()
    
    if not sku_a_buscar:
        print("No se ingresó ningún SKU.")
        return
    elif sku_a_buscar == "0":
        gestion_productos()
        return

    datos_producto = mapa_productos.obtener(sku_a_buscar.strip())

    if datos_producto:
        print("\nProducto Encontrado:")
        for clave, valor in datos_producto.items():
            print(f"{clave}: {valor}")
        
        
        historial_busqueda.append(datos_producto)
        
        if len(historial_busqueda) > 5:
            historial_busqueda.pop(0)
        

        # Guardar el historial actualizado en el archivo JSON
        try:
            with open('historial.json', 'w', encoding='utf-8') as archivo_json:
                json.dump(historial_busqueda, archivo_json, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error al guardar el historial: {e}")
    
        
    else:
        print(f"\nNo se encontró ningún producto con el SKU: {sku_a_buscar}")
        time.sleep(1)
        buscar_producto_con_hash()
        
    opcion = input("\nIngrese S para buscar un nuevo producto o cualquier tecla para volver: ")
    if opcion.upper() == "S":
        buscar_producto_con_hash()
    else:
        gestion_productos()

# Elimina productos por SKU usando la tabla hash y archivo temporal
def eliminar_producto_con_hash(nombre_archivo='basedatos.csv', sku_columna='sku'):
    
    ultimo_id = 1000
    # Determinar el último ID en el archivo CSV
    try:
        with open(nombre_archivo, mode='r', newline='', encoding='utf-8') as archivo_csv:
            buscar = csv.DictReader(archivo_csv)
            ids = [int(fila["id"]) for fila in buscar if fila.get("id")]
            if ids: 
                ultimo_id = max(ids)
    except FileNotFoundError:
        pass
    except Exception:
        pass

    # Como el ultimo id (que es agregado automaticamente), se usa para definir el tamaño de la tabla hash
    mapa_productos = TablaHashSimple(size=ultimo_id)
    
    # Cargar productos en la tabla hash
    try:
        with open(nombre_archivo, mode='r', encoding='utf-8', newline='') as f:
            lector = csv.DictReader(f)
            nombres_columnas = lector.fieldnames or []
            if not nombres_columnas:
                print(f"Error: El archivo '{nombre_archivo}' está vacío o no tiene cabecera.")
                time.sleep(1)
                gestion_productos()
                return
            
            if sku_columna not in nombres_columnas:
                print(f"Error: La columna '{sku_columna}' no se encontró en '{nombre_archivo}'.")
                print(f"Columnas disponibles: {', '.join(nombres_columnas)}")
                return
            
            for fila in lector:
                clave_sku = fila.get(sku_columna, "").strip()
                if clave_sku:
                    mapa_productos.insertar(clave_sku, fila)
                nombre = fila.get("nombre")
        
        sku_a_buscar = input("Ingrese el SKU del producto a buscar o 0 para volver al menu: ").upper()
        
        if sku_a_buscar == "0":
            gestion_productos()
            return
            
        elif not sku_a_buscar:
            print("No se ingresó ningún SKU.")
            return

        datos_producto = mapa_productos.obtener(sku_a_buscar.strip())

        # En caso de existir el producto solicitado, mostrar sus datos y pedir confirmación para eliminarlo
        if datos_producto:
            print("\nEl producto seleccionado es el siguiente: ")
            for clave, valor in datos_producto.items():
                print(f"{clave}: {valor}")
            borrar_volver = input("\n¿Seguro que desea eliminar este producto? Presione S para continuar o cualquier otra tecla para cancelar: ").strip().upper()
            if borrar_volver == "S":
                archivo_temporal = nombre_archivo + '.tmp'
                
                try:
                    with open(nombre_archivo, mode='r', encoding='utf-8', newline='') as archivo_entrada, open(archivo_temporal, mode='w', encoding='utf-8', newline='') as archivo_salida:
                        lector = csv.DictReader(archivo_entrada)
                        nombres_columnas = lector.fieldnames
                        escritor = csv.DictWriter(archivo_salida, fieldnames=nombres_columnas)
                        escritor.writeheader()
                        for fila in lector:
                            if fila.get(sku_columna, "").strip().upper() != sku_a_buscar.strip().upper():
                                escritor.writerow(fila)
                    os.replace(archivo_temporal, nombre_archivo)
                    print(f"Producto con SKU {sku_a_buscar} eliminado exitosamente.")
                except Exception as e:
                    print(f"Ocurrió un error al intentar eliminar el producto: {e}")
                    if os.path.exists(archivo_temporal):
                        os.remove(archivo_temporal)
                time.sleep(1)
                gestion_productos()
            else:
                print("Operación cancelada.")
                time.sleep(1)
                gestion_productos()
        else:
            print(f"\nNo se encontró ningún producto con el SKU: {sku_a_buscar}")
            time.sleep(1)
            eliminar_producto_con_hash()
            input("Presione cualquier tecla para volver al menu: ")
            menu()
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{nombre_archivo}'.")
        time.sleep(1)
        gestion_productos()
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return

# Inicia la aplicación mostrando el menú principal
menu()