import re
import sys
import csv
from bs4 import BeautifulSoup
import urllib.request
from urllib.error import HTTPError
import logging

def creaTabla(url,archivo_salida,paginacion,categoria):
    print (url,paginacion,categoria)
    try:
        with urllib.request.urlopen(url+str(paginacion),timeout=500) as response, open('salida/'+archivo_salida, 'wb') as out_file,  open('limpios/'+archivo_salida+".csv", 'w', newline="\n") as csvfile:
            data = response.read().decode('utf-8').encode('utf-8')
            soup = BeautifulSoup(data)

            paginas= soup.find('span',attrs={"id":"lblPaginacion"}).get_text()
            print(paginas,paginas != 'Página  1 de  1')

            total_paginas = paginas.split(' ')[-1]
            try:
                if total_paginas != '1':
                    return creaTabla(url,archivo_salida,paginacion * int(total_paginas),categoria)
                out_file.write(data)

                table = soup.find('table',attrs={"id":"tblResultados"})

                spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)

                for row in table.find_all("tr"):
                    x = [td.get_text() for td in row.find_all("td")]
                    x.append(categoria)
                    spamwriter.writerow(x)
                    #print(x)
            except:
                print ('La página no tiene tabla, ',url, paginacion)
    except Exception as e:
        print ("Error: ", url,e)

# url = "http://www.economia-sniim.gob.mx/Nuevo/Consultas/MercadosNacionales/PreciosDeMercado/Agricolas/ResultadosConsultaFechaFrutasYHortalizas.aspx?ProductoId=514&fechaInicio=20%2f06%2f1990&fechaFinal=21%2f06%2f2001&RegistrosPorPagina="
# archivo_salida = "Melón_Gotas_de_miel.aspx"

# creaTabla(url,archivo_salida,150)
# sys.exit()

#Esta liga es el mapa de sitio que contiene todas las ligas a precios
with urllib.request.urlopen('http://www.economia-sniim.gob.mx/nuevo/mapa.asp') as response, open('mapa.aspx', 'wb') as out_file:
    data = response.read() # a `bytes` object
    out_file.write(data)
    soup_directorio = BeautifulSoup(data)
    flag = False
    for anchor in soup_directorio.findAll('a', text=re.compile('Precio')):
        if anchor.text == 'Precio de Ciruela Roja':
            flag = True
        if flag:
            for anio in range(1990,2020,5):
                url = anchor['href']+"&fechaInicio=01%2f01%2f{}&fechaFinal=31%2f12%2f{}&RegistrosPorPagina=".format(anio,anio+4)
                if(url.find("http:")>=0):
                    creaTabla(url,anchor.text.replace(" ","_")+str(anio)+"-"+str(anio+4),1000,anchor.text.replace(" ","_"))
                    #print(url,anchor.text.replace(" ","_")+str(anio)+"-"+str(anio+4),1000,anchor.text.replace(" ","_"))