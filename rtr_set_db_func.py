import sqlite3 as sql
import datetime
from rtr_scrap_func import rtr_request_sitemenu
from rtr_scrap_func import rtr_urls_in_family
from rtr_scrap_func import rtr_request_data_tuple


def create_db():
    conn = sql.connect("database/rtr_db.db")
    conn.commit ()
    conn.close()

# Crea tablas en funcion de una lista dada con ID de ARTICULO y DATESTAMP ojo detect_types en SQLITE
def create_multi_tables (nombres_tablas):
    for i in nombres_tablas:
        conn = sql.connect("database/rtr_db.db",
                             detect_types=sql.PARSE_DECLTYPES |
                             sql.PARSE_COLNAMES)
        cursor = conn.cursor()
        instruccion = f"CREATE TABLE IF NOT EXISTS {i} (id_it INTEGER NOT NULL PRIMARY KEY, nombre_it TEXT, precio_it REAL, date TIMESTAMP)"
        cursor.execute(instruccion)
        conn.commit()
        conn.close()

#Corrección de lista para importar nombres sin espacios en columnas de SQLite
def correc_list_spaces (lista_familias):
    #lista_familias = [k for k, v in lista_familias.items()]
    lista_familias_corregida =[]
    for i in lista_familias:
        i = i.replace(",","")
        i = i.replace(" ", "")
        lista_familias_corregida.append(i)
        #print (i)
    return lista_familias_corregida

# Introduce list() de datos en la tabla dada y TIMESTAMP
def insert_family_data_in_table(table, item_list):
    actual_date = datetime.datetime.now()
    conn = sql.connect("database/rtr_db.db", detect_types=sql.PARSE_DECLTYPES |sql.PARSE_COLNAMES)
    cursor = conn.cursor()
    instruccion = f"INSERT INTO {table} VALUES (NULL,?, ?,'{actual_date}')"
    cursor.executemany(instruccion, item_list)
    conn.commit()
    conn.close()

# Request and insert all data from all pages from each family
def insert_all_families_data_in_all_tables():
    sitemenu = rtr_request_sitemenu("https://www.rtrvalladolid.es/87-crawler")
    families_list = list(sitemenu.keys())
    families_list = correc_list_spaces(families_list) #Retorna la lista corregida para importar a SQLite
    main_urls_list = list(sitemenu.values())
    for i in range(len(families_list)):#For para moverse por las Familias Y almacena las urls secundarias
        table_name = families_list[i]
        main_family_url = main_urls_list[i]
        pages = rtr_urls_in_family(main_family_url)
        
        total_family_data = []
        for pag in range(len(pages)):#For para moverse y recopilar datos de las urls secundarias
            data = rtr_request_data_tuple(pages[pag])
            total_family_data.append(data)
        
        tuple_list_tot_fam_data = [i for x in total_family_data for i in x] #Desempaquetamos para obtener lista de tuplas
        print("los datos de la familias",table_name, "son en total: ", len(tuple_list_tot_fam_data))
        insert_family_data_in_table (table_name,tuple_list_tot_fam_data)

#Rebuild_db_with_tables ()
def rebuild_db_with_tables ():
    create_db()
    sitemenu = rtr_request_sitemenu("https://www.rtrvalladolid.es/87-crawler")
    list_familias = list(sitemenu.keys())
    list_familias = correc_list_spaces(list_familias)
    create_multi_tables(list_familias)



