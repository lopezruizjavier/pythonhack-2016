#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import time
import requests
from bs4 import BeautifulSoup

r = requests.get('http://es.postcode.info/espana/p/04')
 
soup = BeautifulSoup(r.text, 'html.parser')

postalList = soup.findAll('a', href=True)

f = open("codigosPostales.csv", 'w')
f.write("Codigo Postal;Latitud;Longitud\n")

for e in postalList:
	try:
		#Coger solo codigos postales
		code = int(e['href']) 
		#Eliminar falsos positivos, los códigos postales tienen mas de 3 números 
		if len(str(code)) > 3: 
			postalCode = "0" +  str(code)
			url = "http://es.postcode.info/espana/p/" + postalCode
			r = requests.get(url)
			soup = BeautifulSoup(r.text, 'html.parser')
			gpsDiv = soup.find('div', class_="cnt")
			gps = gpsDiv.text
			# Eliminar texto tras Listado
			gps = gps.split("Listado",1 )[0] 
			# Quedarse con el texto que esta tras el código postal
			gps = gps.split(postalCode + ":",1 )[1]
			latitud = gps.split(",",1 )[0].strip()
			longitud = gps.split(",",1 )[1].strip()

			f.write(postalCode + ";" + latitud + ";" + longitud +"\n")

		# 1 petición por segundo
		time.sleep(1)
	except:
		pass

f.close()

