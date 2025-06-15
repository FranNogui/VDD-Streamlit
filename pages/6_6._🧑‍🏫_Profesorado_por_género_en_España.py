import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
import json
from streamlit_folium import st_folium
from branca.colormap import LinearColormap

universidad_a_provincia = {
  "Alcalá de Henares": "Madrid",
  "Alicante": "Alacant/Alicante",
  "Almería": "Almería",
  "Autónoma de Barcelona": "Barcelona",
  "Autónoma de Madrid": "Madrid",
  "Barcelona": "Barcelona",
  "Burgos": "Burgos",
  "Cádiz": "Cádiz",
  "Cadiz": "Cádiz",
  "Cantabria": "Cantabria",
  "Carlos III": "Madrid",
  "Castilla-La Mancha": "Ciudad Real",
  "Complutense de Madrid": "Madrid",
  "Córdoba": "Córdoba",
  "Cordoba": "Córdoba",
  "Extremadura": "Badajoz",
  "Girona": "Girona",
  "Granada": "Granada",
  "Huelva": "Huelva",
  "Illes Balears": "Illes Balears",
  "Islas Baleares": "Illes Balears",
  "Jaén": "Jaén",
  "Jaen": "Jaén",
  "Jaume I de Castellón": "Castelló/Castellón",
  "La Rioja": "La Rioja",
  "León": "León",
  "Lleida": "Lleida",
  "Málaga": "Málaga",
  "Malaga": "Málaga",
  "Miguel Hernández de Elche": "Alacant/Alicante",
  "Murcia (1)": "Murcia",
  "Murcia": "Murcia",
  "Oviedo": "Asturias",
  "Pablo de Olavide": "Sevilla",
  "País Vasco": "Bizkaia",
  "Politécnica de Cartagena (1)": "Murcia",
  "Politécnica de Cartagena": "Murcia",
  "Politécnica de Catalunya": "Barcelona",
  "Politécnica de Cataluña": "Barcelona",
  "Politécnica de Madrid": "Madrid",
  "Politécnica de Valencia": "València/Valencia",
  "Católica de Valencia":"València/Valencia",
  "Pompeu Fabra": "Barcelona",
  "Pública de Navarra": "Navarra",
  "Rey Juan Carlos": "Madrid",
  "Rovira i Virgili": "Tarragona",
  "Salamanca": "Salamanca",
  "Santiago de Compostela (2)": "A Coruña",
  "Santiago de Compostela": "A Coruña",
  "Santiago": "A Coruña",
  "Sevilla": "Sevilla",
  "U.N.E.D.": "Madrid",
  "Valencia (Est. General)": "València/Valencia",
  "Valladolid": "Valladolid",
  "Zaragoza": "Zaragoza",
  "Abat Oliba-CEU": "Barcelona",
  "Alfonso X El Sabio": "Madrid",
  "Camilo José Cela": "Madrid",
  "Católica S. Antonio de Murcia": "Murcia",
  "Deusto": "Bizkaia",
  "Europea de Madrid": "Madrid",
  "Francisco de Vitoria": "Madrid",
  "Internacional de Catalunya": "Barcelona",
  "Internacional de La Rioja": "La Rioja",
  "Internacional  de La Rioja": "La Rioja",
  "Navarra": "Navarra",
  "Oberta de Catalunya": "Barcelona",
  "Ramón Llull": "Barcelona",
  "San Jorge": "Zaragoza",
  "UDIMA": "Madrid",
  "Vic": "Barcelona",
  "TOTAL": "TOTAL",
  "UNIVERSIDADES PÚBLICAS": "UNIVERSIDADES PÚBLICAS",
  "UNIVERSIDADES PRIVADAS": "UNIVERSIDADES PRIVADAS",
  "UNIVERSIDADES PúBLICAS": "UNIVERSIDADES PÚBLICAS",
  "La Laguna": "Canarias",
  "Palmas (Las)": "Canarias",
  "UNIVERSIDADES PUBLICAS": "UNIVERSIDADES PUBLICAS",
  "Coruña, A": "A Coruña",
  "Coruña, La": "A Coruña",
  "Vigo": "A Coruña",
  "Antonio de Nebrija": "Madrid",
  "Cardenal Herrera-CEU": "Castelló/Castellón",
  "Católica de Avila": "Ávila",
  "Católica de Ávila": "Ávila",
  "Internal. de Cataluña": "Barcelona",
  "Mondragón": "Gipuzkoa",
  "Pontificia Comillas": "Madrid",
  "Pontificia de Salamanca": "Salamanca",
  "SEK": "Madrid",
  "San Pablo-CEU": "Madrid",
  "Europea Miguel de Cervantes": "Valladolid",
  "Internal. de Catalunya": "Barcelona",
  "IE Universidad": "Madrid",
  "Internacional Valenciana": "València/Valencia",
  "Internacional Menéndez Pelayo": "Madrid",
  "Internacional de Andalucía": "Sevilla",
  "Católica S.Antonio de Murcia": "Murcia",
  "CENTROS ADSCRITOS A UNIV. PUBLICAS": "CENTROS ADSCRITOS A UNIV. PUBLICAS",
  "Católica de ávila": "Ávila",
  "InternacionaI Menéndez Pelayo": "València/Valencia",
  "Internacional de Cataluña": "Barcelona"
}

def anyadirValores(prov, tabla):
  valor = 0
  tablanp = tabla.to_numpy()
  for fila in tablanp:
    if prov in fila:
      valor += fila[1]
  return valor if valor > 0 else 0

@st.cache_data
def loadData():
  directory = './Data/Espanya/Provincias/recintos_provinciales_inspire_peninbal_etrs89.shp'
  provincias = gpd.read_file(directory)
  provincias = provincias.to_crs("EPSG:4326")
  provincias = provincias[['NAMEUNIT', 'geometry']]
  provincias = provincias.rename(columns={'NAMEUNIT': 'Provincia'})

  profesoradoPublica = pd.read_excel("./Data/Espanya/Profesorado/Profesorado centros publicos.xlsx",
                                       sheet_name=0, skiprows=8, usecols=[0,1,2], names=['Universidad', 'AmbosSexos', 'Mujeres'])
  profesoradoPrivada = pd.read_excel("./Data/Espanya/Profesorado/Profesorado centros privados.xlsx",
                                      sheet_name=0, skiprows=8, usecols=[0,1,2], names=['Universidad', 'AmbosSexos', 'Mujeres'])
  
  profesorado = pd.concat([profesoradoPublica, profesoradoPrivada], ignore_index=True)
  profesorado['Hombres'] = profesorado['AmbosSexos'] - profesorado['Mujeres']
  profesorado = profesorado[["Universidad", "Hombres", "Mujeres", "AmbosSexos"]]
  profesorado['Provincia'] = profesorado['Universidad'].apply(lambda x: universidad_a_provincia[x])

  provincias["Hombres"] = provincias['Provincia'].apply(lambda x: anyadirValores(x, profesorado[['Provincia', 'Hombres']]))
  provincias["Mujeres"] = provincias['Provincia'].apply(lambda x: anyadirValores(x, profesorado[['Provincia', 'Mujeres']]))
  provincias["AmbosSexos"]  = provincias['Provincia'].apply(lambda x: anyadirValores(x, profesorado[['Provincia', 'AmbosSexos']]))

  provincias["DifSexo"] = provincias["Hombres"] / provincias["Mujeres"]
  provincias = provincias.fillna(0)

  gdf = gpd.GeoDataFrame(provincias)
  gdf['geometry'] = gdf['geometry'].simplify(0.001, preserve_topology=True)

  return gdf

def main():
  st.set_page_config(
    page_title="Profesorado en España",
    page_icon="🧑‍🏫",
    layout='wide'
  )

  gdf = loadData()

  typeInfo = st.sidebar.selectbox('Información:', ['Mujeres', 'Hombres', 'Ambos Sexos', 'Comparativa'])

  if typeInfo == 'Mujeres':
    linear = LinearColormap(["white", "blue", "red"], vmin=0, vmax=gdf['Mujeres'].max())
    linear.options = {"position": "top"}
    bounds = gdf.total_bounds

    m = folium.Map(zoom_start=6)
    m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
    linear.add_to(m)

    geojson = folium.GeoJson(data=json.loads(gdf.to_json()),
                              style_function = lambda feature: 
                              {
                              "fillColor": linear(feature['properties'].get('Mujeres')),
                              "color": "black",
                              "weight": 1,
                              "fillOpacity": 0.5
                              },
                              tooltip=folium.GeoJsonTooltip(
                              fields=["Provincia", 'Mujeres'],
                              aliases=["Provincia:", "Num. Profesores:"],
                              localize=True
                            ))

    geojson.add_to(m)

    st.title("Profesorado mujer por provicinas en 2011")
    st.write("En esta página se puede observar la cantidad de mujeres que ejercieron como profesoras "
    "en las universidades de las diferentes provicinas españolas.")
    st_folium(m, use_container_width=True, height=600, returned_objects=[])

  elif typeInfo == 'Hombres':
    linear = LinearColormap(["white", "blue", "red"], vmin=0, vmax=gdf['Hombres'].max())
    linear.options = {"position": "top"}
    bounds = gdf.total_bounds

    m = folium.Map(zoom_start=6)
    m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
    linear.add_to(m)

    geojson = folium.GeoJson(data=json.loads(gdf.to_json()),
                              style_function = lambda feature: 
                              {
                              "fillColor": linear(feature['properties'].get('Hombres')),
                              "color": "black",
                              "weight": 1,
                              "fillOpacity": 0.5
                              },
                              tooltip=folium.GeoJsonTooltip(
                              fields=["Provincia", 'Hombres'],
                              aliases=["Provincia:", "Num. Profesores:"],
                              localize=True
                            ))

    geojson.add_to(m)

    st.title("Profesorado hombre por provicinas en 2011")
    st.write("En esta página se puede observar la cantidad de hombres que ejercieron como profesores "
    "en las universidades de las diferentes provicinas españolas.")
    st_folium(m, use_container_width=True, height=600, returned_objects=[])
  elif typeInfo == 'Ambos Sexos':
    linear = LinearColormap(["white", "blue", "red"], vmin=0, vmax=gdf['AmbosSexos'].max())
    linear.options = {"position": "top"}
    bounds = gdf.total_bounds

    m = folium.Map(zoom_start=6)
    m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
    linear.add_to(m)

    geojson = folium.GeoJson(data=json.loads(gdf.to_json()),
                              style_function = lambda feature: 
                              {
                              "fillColor": linear(feature['properties'].get('AmbosSexos')),
                              "color": "black",
                              "weight": 1,
                              "fillOpacity": 0.5
                              },
                              tooltip=folium.GeoJsonTooltip(
                              fields=["Provincia", 'AmbosSexos'],
                              aliases=["Provincia:", "Num. Profesores:"],
                              localize=True
                            ))

    geojson.add_to(m)

    st.title("Profesorado por provicinas en 2011")
    st.write("En esta página se puede observar la cantidad total de profesores "
    "en las universidades de las diferentes provicinas españolas.")
    st_folium(m, use_container_width=True, height=600, returned_objects=[])
  else:
    linear = LinearColormap(["white", "blue", "red"], vmin=0, vmax=gdf['DifSexo'].max())
    linear.options = {"position": "top"}
    bounds = gdf.total_bounds

    m = folium.Map(zoom_start=6)
    m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
    linear.add_to(m)

    geojson = folium.GeoJson(data=json.loads(gdf.to_json()),
                              style_function = lambda feature: 
                              {
                              "fillColor": linear(feature['properties'].get('DifSexo')),
                              "color": "black",
                              "weight": 1,
                              "fillOpacity": 0.5
                              },
                              tooltip=folium.GeoJsonTooltip(
                              fields=["Provincia", 'DifSexo'],
                              aliases=["Provincia:", "Hombres / Mujeres:"],
                              localize=True
                            ))

    geojson.add_to(m)

    st.title("Comparativa de género por provicinas en 2011")
    st.write("En esta página se puede observar una comparativa entre ambos géneros obtenida mediante "
    "la división del profesorado hombre entre el profesorado mujer.")
    st_folium(m, use_container_width=True, height=600, returned_objects=[])

main()