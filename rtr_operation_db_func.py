import sqlite3 as sql
import os

def read_all_rows(tabla):
    conn = sql.connect("database/rtr_db.db")
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM {tabla} "
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()    
    print (datos)
    return datos
    
#Función para obtener lista de tablas en las BD
def list_of_tables(path_db):
    conn = sql.connect(path_db)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    tables = [i for family in tables for i in family]
    conn.close()
#    print(tables)
    return (tables)

#Función para filtrar por precio MENOR
def filter_precio_menor (tabla,precio):
    conn = sql.connect("database/rtr_db.db")
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM {tabla} WHERE precio_it < {precio} ORDER BY precio_it DESC"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()   
    return datos

#Función para filtrar por precio MAYOR
def filter_precio_mayor (tabla,precio):
    conn = sql.connect("database/rtr_db.db")
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM {tabla} WHERE precio_it > {precio} ORDER BY precio_it DESC"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()   
    return datos

#Función para filtrar por precio IGUAL
def filter_precio_igual (tabla,precio):
    conn = sql.connect("database/rtr_db.db")
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM {tabla} WHERE precio_it = {precio} ORDER BY precio_it DESC"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()   
    return datos

#Función para filtrar resultados de una tabla por precio. 3 tipos: menor,mayor o igual.
def filter_precio (tipo,tabla,precio):
    if tipo == "menor":
        result_filter = filter_precio_menor (tabla,precio)
        return result_filter
    elif tipo == "mayor":
        result_filter = filter_precio_mayor (tabla,precio)
        return result_filter
    elif tipo == "igual":
        result_filter = filter_precio_igual (tabla,precio)
        return result_filter
    else:
        print("ERROR")

#Funcion para filtrar por nombre
def filter_nombre (tabla, nombre):
    #nombre = f"%{nombre}%"
    conn = sql.connect("database/rtr_db.db")
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM {tabla} WHERE nombre_it LIKE '%{nombre}%' ORDER BY precio_it DESC"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()   
    return datos

#Funcion para saber si esta creada la BD
def check_if_db_exists(db_directory = "database/rtr_db.db"):
	if os.path.exists(db_directory):
		return (True)
	else:
		return (False)

#Funcion para saber si la BD esstá vacía
def check_if_empty_db(db_directory = "database/rtr_db.db"):
	if list_of_tables(db_directory) == []:
		print ("Base de datos vacía")
	else:
		print ("Base de datos llena")
