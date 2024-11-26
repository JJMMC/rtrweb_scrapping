from bs4 import BeautifulSoup
import requests

# Función para obtener el menú de la web por el que navegar
def rtr_request_sitemenu (website = "https://www.rtrvalladolid.es/87-crawler"): #Entregada la web retorna un dict(familia:main_url_familia)
    #website = "https://www.rtrvalladolid.es/87-crawler"
    res = requests.get(website,timeout=10)
    content = res.text
    soup = BeautifulSoup(content,"html.parser")
    url_familias = soup.find("ul", class_="category-sub-menu").find_all("a")
    #A continuación vamos a definir un filtro para los submenús. No queremos que aparezcan
    los_submenus = soup.find("ul", class_="category-sub-menu").find_all("a",class_="category-sub-link")

    d = {}
    for link in url_familias:
        if link in los_submenus:
            continue
        else:
            d[link.string] = link.get("href") #Añadimos los valores al diccionario
    return d

# Función de selección para Familias
def seleccion_familia (num_seleccionado):
    sitemenu = rtr_request_sitemenu("https://www.rtrvalladolid.es/87-crawler")
    sitemenu_families = list(sitemenu.keys())
    sitemenu_main_urls = list(sitemenu.values())
    
    for i in range(len(sitemenu_main_urls)):
        if i == num_seleccionado:
              familia_seleccionada = sitemenu_main_urls[i-1]
    return familia_seleccionada

# Función que dada la main url de la familia retorna list() de las url que descuelgan de ella para extraer los datos
def rtr_urls_in_family (url):
	url_base = url
	total_paginas_url= []
	for i in range (1,50):
		
		test_url = f"{url_base}?page={str(i)}" # formato de las urls de RTR para moverse entre páginas
		
		res = requests.get(test_url, timeout=10)
		content = res.text
		soup = BeautifulSoup(content,"html.parser")
		vacio = soup.find(class_="page-content page-not-found") #Buscamos esta clase para encontrar la página sin datos
		
		if vacio == None:
			total_paginas_url.append(test_url)
			
		else:
			break			
		
	return total_paginas_url #Retorna list con urls de la familia

# Func para obtener los datos de artículo y precio output: dict()
def rtr_request_multi_data (website):
    #inicializamos la lista
    final_list = []
    
    res = requests.get(website)
    content = res.text
    soup = BeautifulSoup(content,"html.parser")

    items_list = soup.find_all("div", class_="product-description")
    items_prices = soup.find_all(class_="price")

    for i in items_list:
        d = {}
        index = items_list.index(i)
        #d["index"] = index

        
        producto = i.h2.get_text(strip=True)
        d["producto"] = producto
      
        
        precio = items_prices[index].text.replace("€","").replace(",",".").strip()
        # Ajustamos los datos para que nos queden como queremos con sólo un "." para el precio en los número mayores de 1000
        if len(precio) > 6:
            precio = float(precio.replace(".","",1))
            d["precio"] = precio
        else:
            d["precio"] = precio

      
        final_list.append(d)
    return final_list

# Igual que la anterior pero retorna lista de tuplas para importar a SQLite
def rtr_request_data_tuple (website):
    #inicializamos la lista
    final_list = []
    
    res = requests.get(website)
    content = res.text
    soup = BeautifulSoup(content,"html.parser")

    items_list = soup.find_all("div", class_="product-description")
    items_prices = soup.find_all(class_="price")

    for i in items_list:
        d = {}
        temp_tuple = ()
        index = items_list.index(i)
        #d["index"] = index

        producto = i.h2.get_text(strip=True)
        d["producto"] = producto
      
        precio = items_prices[index].text.replace("€","").replace(",",".").strip()
        # Ajustamos los datos para que nos queden como queremos con sólo un "." para el precio en los número mayores de 1000
        if len(precio) > 6:
            precio = float(precio.replace(".","",1))
            d["precio"] = precio
        else:
            d["precio"] = precio
        temp_tuple = (producto,precio)
        final_list.append(temp_tuple)
    return final_list

