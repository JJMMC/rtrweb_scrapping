from bs4 import BeautifulSoup
import requests

# Función de selección para Familias

def seleccion_familia (num_seleccionado):
    sitemenu = rtr_request_sitemenu("https://www.rtrvalladolid.es/87-crawler")
    sitemenu_list = sitemenu.items()
    sitemenu_list = [i for t in sitemenu_list for i in t]
    sitemenu_list_url = []
    for i in range(1,len(sitemenu_list),2):
        sitemenu_list_url.append(sitemenu_list[i])
        
    
    for i in range(len(sitemenu_list_url)):
        if i == num_seleccionado:
              familia_seleccionada = sitemenu_list_url[i-1]
    return familia_seleccionada

# Función de Contador urls

def rtr_pages_to_scan (url):
	url_base = url
	total_paginas_url= []
	for i in range (1,10):
		
		test_url = f"{url_base}?page={str(i)}" # formato de las urls de RTR para moverse entre páginas
		
		res = requests.get(test_url, timeout=10)
		content = res.text
		soup = BeautifulSoup(content,"html.parser")
		vacio = soup.find(class_="page-content page-not-found") #Buscamos esta clase para encontrar la página sin datos
		
		if vacio == None:
			total_paginas_url.append(test_url)
			
		else:
			break			
		
	return total_paginas_url

# Func para obtener los datos de artículo y precio

def rtr_request_multi_data (website):
    coches_list = []
    
    res = requests.get(website)
    content = res.text
    soup = BeautifulSoup(content,"html.parser")

    items_list = soup.find_all("div", class_="product-description")
    items_prices = soup.find_all(class_="price")

    for i in items_list:
        d = {}
        index = items_list.index(i)
        
        producto = i.h2.get_text(strip=True)
        d["producto"] = producto
              
        precio = items_prices[index].text.replace("€","").replace(",",".").strip()
        # Ajustamos los datos para que nos queden como queremos con sólo un "." para el precio en los número mayores de 1000
        if len(precio) > 6:
            precio = float(precio.replace(".","",1))
            d["precio"] = precio
        else:
            d["precio"] = precio
     
        coches_list.append(d)
    return coches_list

# Función para obtener el menú de la web por el que navegar

def rtr_request_sitemenu (website):
    website = "https://www.rtrvalladolid.es/87-crawler"
    res = requests.get(website,timeout=10)
    content = res.text
    soup = BeautifulSoup(content,"html.parser")
    url_familias = soup.find("ul", class_="category-sub-menu").find_all("a")
    #A continuación vamos a definir un filtro para los submenús
    los_submenus = soup.find("ul", class_="category-sub-menu").find_all("a",class_="category-sub-link")

    d = {}
    for link in url_familias:
        if link in los_submenus:
            continue
        else:
            d[link.string] = link.get("href") #Añadimos los valores al diccionario
    return d

