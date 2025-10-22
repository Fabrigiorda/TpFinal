import os, time, csv

productos = {}




def menu():

    

    os.system("cls")
    print("Menu:")
    print("1. Gestión de Productos")
    print("2. Procesar pedidos")
    print("3. Historial")
    print("4. Explorar")
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


    nuevo.append(nuevo_id)
    nuevo.append(nuevo_nombre)
    nuevo.append(stock)
    nuevo.append(precio)
    nuevo.append(sku)
    
    file_exists = os.path.isfile(archivo)

    with open(archivo, 'a', newline='', encoding='utf-8') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        if not file_exists or os.path.getsize(archivo) == 0:
             escritor_csv.writerow(["id", "nombre", "stock", "precio", "sku"])
        escritor_csv.writerow(nuevo)

def actualizar_producto():
    nombre_archivo = 'basedatos.csv'
    archivo_temporal = 'temp_basedatos.csv'

    os.system("cls")
    print("Modificar Producto por SKU")
    sku_a_buscar = input("Ingrese el SKU del producto que desea modificar: ")

    try:
        datos_actualizados = []
        producto_encontrado = False

        with open(nombre_archivo, 'r', newline='', encoding='utf-8') as archivo_lectura:
            lector = csv.reader(archivo_lectura)

            cabecera = next(lector)
            datos_actualizados.append(cabecera)

            for fila in lector:
                if len(fila) > 4 and fila[4].upper() == sku_a_buscar.upper():
                    producto_encontrado = True
                    print(f"\nProducto encontrado: ID={fila[0]}, Nombre={fila[1]}, Stock={fila[2]}, Precio={fila[3]}, SKU={fila[4]}")
                    print("Por favor, ingrese los nuevos datos.")

                    nuevo_nombre = input("Nuevo nombre: ")
                    nuevo_stock = input("Nuevo stock: ")
                    nuevo_precio = input("Nuevo precio: ")
                    nuevo_SKU = input("Nuevo SKU: ")

                    fila[1] = nuevo_nombre.upper()
                    fila[2] = nuevo_stock
                    fila[3] = nuevo_precio
                    fila[4] = nuevo_SKU.upper()
                datos_actualizados.append(fila)
        if producto_encontrado:
            with open(archivo_temporal, 'w', newline='', encoding='utf-8') as archivo_escritura:
                escritor = csv.writer(archivo_escritura)
                escritor.writerows(datos_actualizados)

            os.replace(archivo_temporal, nombre_archivo)
            print(f"\n¡Éxito! El producto '{sku_a_buscar}' ha sido actualizado.")
        else:
            print(f"\nNo se encontró ningún producto con el SKU '{sku_a_buscar}'.")

    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no fue encontrado.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

def pedidos():
    pass

def historial():
    pass

def explorar():
    pass

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
    mapa_productos = SimpleHashMap()
    
    try:
        with open(nombre_archivo, mode='r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            
            # Evitar TypeError si el archivo está vacío o no tiene cabecera
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
    else:
        print(f"\nNo se encontró ningún producto con el SKU: {sku_a_buscar}")
        time.sleep(1)
        buscar_producto_con_hash()
    salir = input("Presione cualquier tecla para volver al menu: ")
    if salir:
        menu()

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
            
            # Evitar TypeError si el archivo está vacío o no tiene cabecera
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
        salir = input("Presione cualquier tecla para volver al menu: ")
        if salir:
            menu()
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{nombre_archivo}'.")
        time.sleep(1)
        gestion_productos()
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return

menu()