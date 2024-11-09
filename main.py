from rtr_scrap_func import *

#### EJECUCIÓN DEL PROGRAMA PPAL

sitemenu = rtr_request_sitemenu("https://www.rtrvalladolid.es/87-crawler")
    
    # Imprime en terminal el menu para seleccionar la familia a scrapear
contador = 1
for i in sitemenu:
    print(f"{contador}.-{i}")
    contador = contador + 1
seleccionado = int(input("Selecciona lo que quieres Scrapear: "))

    # Llamamos a las funciones para obtener los datos y presentarlos en terminal
url_seleccionada = (seleccion_familia(seleccionado))
lista_url_seleccionadas = rtr_pages_to_scan(url_seleccionada)
datos_scrapeados_tot = list()
for url in lista_url_seleccionadas:
    datos_scrapeados_pag = rtr_request_multi_data(url)
    datos_scrapeados_tot = datos_scrapeados_tot + datos_scrapeados_pag
for i in datos_scrapeados_tot:
    print (i)
print ("Número de artículos: ", len(datos_scrapeados_tot))

