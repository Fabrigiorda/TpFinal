import os, time, csv, json

productos = {}
lista_pedidos = []
historial_busqueda = []

archivo_historial = 'historial.json'
try:
    
    if os.path.exists(archivo_historial) and os.path.getsize(archivo_historial) > 0:
        with open(archivo_historial, 'r', encoding='utf-8') as f:
            historial_busqueda = json.load(f)
            
            if not isinstance(historial_busqueda, list):
                historial_busqueda = []
    else:
        
        historial_busqueda = []
except (json.JSONDecodeError, FileNotFoundError):
    
    historial_busqueda = []

class TreeNode:
    def __init__(self, name):
        self.name = name
        self.children = {}
        self.products = []

category_root = TreeNode("Categorías")

def load_category_tree(nombre_archivo='basedatos.csv'):
    global category_root
    category_root = TreeNode("Categorías")
    try:
        with open(nombre_archivo, mode='r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            if 'categoria' not in reader.fieldnames:
                return
            
            for fila in reader:
                categoria_path = fila.get('categoria', '').strip()
                if not categoria_path:
                    categoria_path = "SIN CATEGORIA"

                parts = categoria_path.split('/')
                current_node = category_root
                
                for part in parts:
                    if part not in current_node.children:
                        current_node.children[part] = TreeNode(part)
                    current_node = current_node.children[part]
                
                current_node.products.append(fila)
                
    except FileNotFoundError:
        pass
    except Exception:
        pass

def get_all_products_recursive(node):
    products = []
    products.extend(node.products)
    for child in node.children.values():
        products.extend(get_all_products_recursive(child))
    return products

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


    nuevo_id = ultimo_id + 1

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
    
    file_exists = os.path.isfile(archivo)
    
    fieldnames = ["id", "nombre", "stock", "precio", "sku", "categoria"]

    with open(archivo, 'a', newline='', encoding='utf-8') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        if not file_exists or os.path.getsize(archivo) == 0:
             escritor_csv.writerow(fieldnames)
        escritor_csv.writerow(nuevo)

def actualizar_producto():
    nombre_archivo = 'basedatos.csv'
    archivo_temporal = 'temp_basedatos.csv'
    fieldnames = ["id", "nombre", "stock", "precio", "sku", "categoria"]

    os.system("cls")
    print("Modificar Producto por SKU")
    sku_a_buscar = input("Ingrese el SKU del producto que desea modificar: ")

    try:
        datos_actualizados = []
        producto_encontrado = False

        with open(nombre_archivo, 'r', newline='', encoding='utf-8') as archivo_lectura:
            lector = csv.reader(archivo_lectura)

            cabecera = next(lector)
            # Asegurarse que la cabecera tenga 'categoria'
            if 'categoria' not in cabecera:
                cabecera.append('categoria')
                
            datos_actualizados.append(cabecera)
            
            sku_index = 4
            categoria_index = 5

            for fila in lector:
                if len(fila) <= sku_index:
                    datos_actualizados.append(fila)
                    continue
                
                # Asegurar que la fila tenga espacio para la categoria
                while len(fila) <= categoria_index:
                    fila.append("")

                if fila[sku_index].upper() == sku_a_buscar.upper():
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
        if not pedido_actual:
            print("El pedido está vacío.")
        else:
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
                    confirm_del = input("¿Seguro que desea vaciar el pedido? (S/N): ").upper()
                    if confirm_del == 'S':
                        pedido_actual = []
                        print("Pedido vaciado.")
                        time.sleep(1)
                        break
                    else:
                        continue

                try:
                    index_mod = int(opcion_mod) - 1
                    if 0 <= index_mod < len(pedido_actual):
                        item_a_modificar = pedido_actual[index_mod]
                        print(f"Modificando: {item_a_modificar['producto']}")
                        print("[1] Modificar cantidad")
                        print("[2] Eliminar producto")
                        print("[0] Volver")
                        op_item = input("Opción: ").strip()

                        if op_item == '0':
                            continue
                        
                        elif op_item == '2':
                            confirm_del_item = input(f"¿Eliminar {item_a_modificar['producto']}? (S/N): ").upper()
                            if confirm_del_item == 'S':
                                pedido_actual.pop(index_mod)
                                print("Producto eliminado.")
                                time.sleep(1)
                        
                        elif op_item == '1':
                            try:
                                nueva_cantidad_input = input(f"Ingrese nueva cantidad (actual: {item_a_modificar['cantidad']}): ")
                                nueva_cantidad = int(nueva_cantidad_input)
                                
                                if nueva_cantidad <= 0:
                                    print("La cantidad debe ser positiva. Para eliminar, use la opción 2.")
                                    time.sleep(1.5)
                                    continue

                                stock_disponible = 0
                                try:
                                    with open(nombre_archivo, mode='r', encoding='utf-8', newline='') as f:
                                        reader = csv.DictReader(f)
                                        for fila in reader:
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
            nombre_producto_input = input("Ingrese nombre del producto (o 'V' para volver): ").upper()

            if nombre_producto_input == 'V':
                continue
            
            if not nombre_producto_input:
                print("El nombre del producto no puede estar vacío.")
                time.sleep(1)
                continue

            producto_encontrado = False
            datos_producto = {}

            try:
                with open(nombre_archivo, mode='r', encoding='utf-8', newline='') as f:
                    reader = csv.DictReader(f)
                    for fila in reader:
                        if fila['nombre'].upper() == nombre_producto_input:
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
                print(f"Producto '{nombre_producto_input}' inexistente.")
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
            
            cantidad_input = input("Ingrese la cantidad (o 'V' [Volver], 'C' [Cancelar Pedido]): ").upper()

            if cantidad_input == 'V':
                continue
            if cantidad_input == 'C':
                print("Pedido cancelado.")
                time.sleep(1)
                pedidos()
                return

            try:
                cantidad_deseada = int(cantidad_input)
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
    
    historial_archivo = "pedidos.json"
    historial_pedidos = []
    
    try:
        if os.path.exists(historial_archivo) and os.path.getsize(historial_archivo) > 0:
            with open(historial_archivo, 'r', encoding='utf-8') as f:
                historial_pedidos = json.load(f)
                if not isinstance(historial_pedidos, list):
                    historial_pedidos = []
        else:
            historial_pedidos = []
    except json.JSONDecodeError:
        historial_pedidos = []
    except Exception:
        historial_pedidos = [] 

    historial_pedidos.append(nuevo_pedido_completo)

    try:
        with open(historial_archivo, 'w', encoding='utf-8') as f:
            json.dump(historial_pedidos, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error al guardar en {historial_archivo}: {e}")
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

def procesar_pedido():
    os.system("cls")
    archivo_pedidos = 'pedidos.json'
    archivo_db = 'basedatos.csv'
    
    try:
        if not os.path.exists(archivo_pedidos) or os.path.getsize(archivo_pedidos) == 0:
            print("No hay pedidos para procesar.")
            time.sleep(2)
            pedidos()
            return

        with open(archivo_pedidos, 'r', encoding='utf-8') as f:
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
    fieldnames = []
    try:
        with open(archivo_db, mode='r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            if not fieldnames:
                 print(f"Error CRÍTICO: El archivo '{archivo_db}' está vacío o corrupto.")
                 time.sleep(3)
                 pedidos()
                 return
            for fila in reader:
                inventario[fila['sku']] = fila
    except FileNotFoundError:
        print(f"Error CRÍTICO: No se encontró el archivo de base de datos '{archivo_db}'.")
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
            stock_actual = int(inventario[sku]['stock'])
        except (ValueError, TypeError):
            print(f"ERROR: Stock inválido para SKU {sku} en basedatos.csv.")
            stock_actual = 0

        
        if cantidad_pedida > stock_actual:
            print(f"ERROR: Stock insuficiente para '{item['producto']}' (SKU: {sku}).")
            print(f"   Pedido: {cantidad_pedida} | Disponible: {stock_actual}")
            stock_suficiente = False
            break 

    if stock_suficiente:
        print("\nStock verificado. Actualizando inventario...")
        for item in items_a_procesar:
            sku = item['sku']
            cantidad_pedida = item['cantidad']
            
            stock_actual = int(inventario[sku]['stock'])
            nuevo_stock = stock_actual - cantidad_pedida
            inventario[sku]['stock'] = str(nuevo_stock)
        
        try:
            with open(archivo_db, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(inventario.values())
        except Exception as e:
            print(f"Error CRÍTICO al guardar el inventario: {e}")
            time.sleep(3)
            pedidos()
            return
        
        print("Inventario actualizado en 'basedatos.csv'.")

    else:
        print("\nEl pedido no puede ser procesado por falta de stock.")


    pedido_procesado = lista_pedidos.pop(0) 
    
    try:
        with open(archivo_pedidos, 'w', encoding='utf-8') as f:
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

def explorar():
    load_category_tree()
    current_node = category_root
    path_stack = [category_root]

    while True:
        os.system("cls")
        current_path = " / ".join(n.name for n in path_stack)
        print(f"Explorando: {current_path}\n")

        print("--- Subcategorías ---")
        subcategories = list(current_node.children.keys())
        if not subcategories:
            print("No hay subcategorías.")
        else:
            for i, name in enumerate(subcategories, 1):
                print(f"{i}. {name}")
        
        print("\n--- Productos en esta y subcategorías ---")
        all_products = get_all_products_recursive(current_node)
        if not all_products:
            print("No hay productos.")
        else:
            for prod in all_products:
                print(f"- {prod['nombre']} (SKU: {prod['sku']}, Stock: {prod['stock']})")

        print("\n" + "-"*30)
        print("Ingrese un NÚMERO para entrar a una subcategoría.")
        print("Ingrese '..' para subir un nivel.")
        print("Ingrese '0' para volver al menú principal.")
        
        choice = input("Opción: ").strip().lower()

        if choice == '0':
            menu()
            return
        elif choice == '..':
            if len(path_stack) > 1:
                path_stack.pop()
                current_node = path_stack[-1]
            else:
                print("Ya estás en la raíz.")
                time.sleep(1)
        else:
            try:
                choice_index = int(choice) - 1
                if 0 <= choice_index < len(subcategories):
                    chosen_category_name = subcategories[choice_index]
                    current_node = current_node.children[chosen_category_name]
                    path_stack.append(current_node)
                else:
                    print("Número fuera de rango.")
                    time.sleep(1)
            except ValueError:
                print("Opción no válida.")
                time.sleep(1)

class SimpleHashMap:
    def __init__(self, size=1000):
        self.size = size
        self.buckets = [[] for _ in range(size)]

    def hash_function(self, key):
        return sum(ord(char) for char in str(key)) % self.size

    def insert(self, key, value_data):
        index = self.hash_function(key)
        bucket = self.buckets[index]
        
        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                bucket[i] = (key, value_data)
                return
        
        bucket.append((key, value_data))

    def get(self, key):
        index = self.hash_function(key)
        bucket = self.buckets[index]
        
        for existing_key, value_data in bucket:
            if existing_key == key:
                return value_data 
        return None

def buscar_producto_con_hash(nombre_archivo='basedatos.csv', sku_columna='sku'):
    os.system("cls")
    mapa_productos = SimpleHashMap()
    
    try:
        with open(nombre_archivo, mode='r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            
            fieldnames = reader.fieldnames or []
            if not fieldnames:
                print(f"Error: El archivo '{nombre_archivo}' está vacío o no tiene cabecera.")
                time.sleep(1)
                return
            
            if sku_columna not in fieldnames:
                print(f"Error: La columna '{sku_columna}' no se encontró en '{nombre_archivo}'.")
                print(f"Columnas disponibles: {', '.join(fieldnames)}")
                return
            
            for fila in reader:
                sku_key = fila.get(sku_columna, "").strip()
                if sku_key:
                    mapa_productos.insert(sku_key, fila)

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

    datos_producto = mapa_productos.get(sku_a_buscar.strip())

    if datos_producto:
        print("\nProducto Encontrado:")
        for clave, valor in datos_producto.items():
            print(f"{clave}: {valor}")
        
        
        historial_busqueda.append(datos_producto)
        
        if len(historial_busqueda) > 5:
            historial_busqueda.pop(0)
        

        
        try:
            with open('historial.json', 'w', encoding='utf-8') as json_file:
                json.dump(historial_busqueda, json_file, ensure_ascii=False, indent=4)
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

def eliminar_producto_con_hash(nombre_archivo='basedatos.csv', sku_columna='sku'):
    
    ultimo_id = 1000
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

    
    mapa_productos = SimpleHashMap(size=ultimo_id)
    
    try:
        with open(nombre_archivo, mode='r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            
            
            fieldnames = reader.fieldnames or []
            if not fieldnames:
                print(f"Error: El archivo '{nombre_archivo}' está vacío o no tiene cabecera.")
                time.sleep(1)
                gestion_productos()
                return
            
            if sku_columna not in fieldnames:
                print(f"Error: La columna '{sku_columna}' no se encontró en '{nombre_archivo}'.")
                print(f"Columnas disponibles: {', '.join(fieldnames)}")
                return
            
            for fila in reader:
                sku_key = fila.get(sku_columna, "").strip()
                if sku_key:
                    mapa_productos.insert(sku_key, fila)
                nombre = fila.get("nombre")
        
        sku_a_buscar = input("Ingrese el SKU del producto a buscar o 0 para volver al menu: ").upper()
        
        if sku_a_buscar == "0":
            gestion_productos()
            return
            
        elif not sku_a_buscar:
            print("No se ingresó ningún SKU.")
            return

        datos_producto = mapa_productos.get(sku_a_buscar.strip())

        if datos_producto:
            print("\nEl producto seleccionado es el siguiente: ")
            for clave, valor in datos_producto.items():
                print(f"{clave}: {valor}")
            borrar_volver = input("\n¿Seguro que desea eliminar este producto? Presione S para continuar o cualquier otra tecla para cancelar: ").strip().upper()
            if borrar_volver == "S":
                temp_archivo = nombre_archivo + '.tmp'
                try:
                    with open(nombre_archivo, mode='r', encoding='utf-8', newline='') as f_in, open(temp_archivo, mode='w', encoding='utf-8', newline='') as f_out:
                        reader = csv.DictReader(f_in)
                        fieldnames = reader.fieldnames
                        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
                        writer.writeheader()
                        for fila in reader:
                            if fila.get(sku_columna, "").strip().upper() != sku_a_buscar.strip().upper():
                                writer.writerow(fila)
                    os.replace(temp_archivo, nombre_archivo)
                    print(f"Producto con SKU {sku_a_buscar} eliminado exitosamente.")
                except Exception as e:
                    print(f"Ocurrió un error al intentar eliminar el producto: {e}")
                    if os.path.exists(temp_archivo):
                        os.remove(temp_archivo)
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

menu()