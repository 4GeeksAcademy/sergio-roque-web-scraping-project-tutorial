import os
from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def extract_data(url):
    # Peticion a la web para extraer contenido
    response = requests.get(url)
    if response.status_code == 200:
        # Diccionario para almacenar resultados
        data = {"Año":[], "Ganancias":[], "Crecimiento":[]}
        # Parseo del HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        # Busqueda de la etiqueta tabla y separacion luego de las filas
        tabla = soup.find(class_="table")
        for fila in tabla.find_all("tr"):
            fila_separada = fila.find_all("td")
            if fila_separada:
                # Agrego los datos a mi diccionario
                data["Año"].append(fila_separada[0].get_text(strip=True))
                data["Ganancias"].append(fila_separada[1].get_text(strip=True))
                data["Crecimiento"].append(fila_separada[2].get_text(strip=True))
        # Dataframe con la informacion extraida y luego de limpieza de etiquetas HTML
        df = pd.DataFrame(data)
        print(f"Extraccion finalizada con codigo de respuesta web {response.status_code}")
        return df
    else:
        print(f"Error en la solicitud, codigo {response.status_code}")
        return

def data_2_csv(dataframe):
    # Guardo mi dataframe en csv para las pruebas del codigo
    # Me evito lanzar demasiadas peticiones mientras creo el codigo
    dataframe.to_csv("assets/revenue.csv", index=False)
    print("Dataframe guardado correctamente!!")
    return

url = "https://companies-market-cap-copy.vercel.app/index.html"

# df = extract_data(url)
# data_2_csv(df)

df = pd.read_csv("assets/revenue.csv")
df["Ganancias"] = df["Ganancias"].str.replace("$", "").str.replace("B", "").str.strip()
df["Crecimiento"] = df["Crecimiento"].str.replace("%", "").str.strip()
# No elimino el registro donde Crecimiento contiene un NaN porque al ser el dato mas antiguo el crecimiento es de 0 %
df["Crecimiento"] = df["Crecimiento"].fillna("0")
df = df.rename(columns={"Ganancias":"Ganancias (B)", "Crecimiento": "Crecimiento (%)"})


# PASAR MI DATAFRAME A BASE DE DATOS CON SQL
connection = sqlite3.connect("assets/database.db")
df.to_sql("ganancias", connection, if_exists="replace", index=False)

# Leyendo mis datos de la base de datos sql
df_read = pd.read_sql("SELECT * FROM ganancias", connection)

# VISUALIZACION DE MIS DATOS CON MATPLOTLIB









connection.close()