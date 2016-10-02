#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import psycopg2
import parametersConfig
import subprocess

host = parametersConfig.host
usuario = parametersConfig.usuario
nombreBBDD = parametersConfig.bbdd
tablaBBDD = parametersConfig.tablaBBDD

def lectorDatos(fichero, delimitador, tipos):
	# Codificación 'SECTOR'
	convUTF8 = lambda valstr: str(valstr.decode("utf-8"))
	# Para tratar reales con comas como separador de la parte decimal
	convComaAPunto = lambda valstr: float(valstr.decode("utf-8").replace(',','.'))
	c = {2:convUTF8, 5:convComaAPunto}
	datos = np.genfromtxt(fichero, delimiter=delimitador, names=True, skip_header= 0, dtype=tipos, converters = c)
	return datos

def insertaPostgreSQL(datos):
	# Creación de la BBDD
	subprocess.call(["createdb", nombreBBDD])
	
	# Se define la cadena de conexión
	conn_string = "host=" + host + " dbname=" + nombreBBDD + " user=" + usuario
	print("Conectado a PostgreSQL\n	->%s" % (conn_string))
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()
	
	# Creación de la tabla
	cursor.execute("CREATE TABLE " + tablaBBDD + "(CP_CLIENTE integer, CP_COMERCIO integer, SECTOR text, DIA DATE, FRANJA_HORARIA text, IMPORTE decimal, NUM_OP integer);")
	
	# Inserciones
	for tupla in datos:
		query = "INSERT INTO "  + tablaBBDD + " VALUES (%s, %s, %s, %s, %s, %s, %s)"
		valores = (tupla['CP_CLIENTE'],tupla['CP_COMERCIO'],tupla['SECTOR'],tupla['DIA'],tupla['FRANJA_HORARIA'],tupla['IMPORTE'],tupla['NUM_OP'])
		cursor.execute(query, valores)
	cursor.close()
	conn.commit()
	conn.close()


datos = lectorDatos('datasets/card_analytics_dataset.txt','|',(int,int,'|S30','|S10','|S5',float,int))
print datos
print 'Filas: ', datos.shape[0]
insertaPostgreSQL(datos)
