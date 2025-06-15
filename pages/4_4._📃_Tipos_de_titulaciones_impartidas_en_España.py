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

anyos = [
  "2008-2009", 
  "2009-2010",
  "2010-2011"
]

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

  for anyo in anyos:
    titulaciones = pd.read_excel(f"./Data/Espanya/Titulaciones/Grados por rama {anyo}.xlsx",
                                  sheet_name=0, skiprows=7, usecols=[0,1,2,3,4,5,6],
                                  names=['Universidad', 'Total', 'Ciencias', 'Salud', 'Sociales', 'Arte', 'Ingenieria'])
      
    titulaciones = titulaciones.replace('.', 0)
    
    titulaciones['Provincia'] = titulaciones['Universidad'].apply(lambda x: universidad_a_provincia[x])

    provincias[f'Ciencias{anyo}']    = provincias['Provincia'].apply(lambda x: anyadirValores(x, titulaciones[['Provincia', 'Ciencias']]))
    provincias[f'Salud{anyo}']       = provincias['Provincia'].apply(lambda x: anyadirValores(x, titulaciones[['Provincia', 'Salud']]))
    provincias[f'Sociales{anyo}']    = provincias['Provincia'].apply(lambda x: anyadirValores(x, titulaciones[['Provincia', 'Sociales']]))
    provincias[f'Arte{anyo}']        = provincias['Provincia'].apply(lambda x: anyadirValores(x, titulaciones[['Provincia', 'Arte']]))
    provincias[f'Ingenieria{anyo}']  = provincias['Provincia'].apply(lambda x: anyadirValores(x, titulaciones[['Provincia', 'Ingenieria']]))
    provincias[f'Total{anyo}']       = provincias['Provincia'].apply(lambda x: anyadirValores(x, titulaciones[['Provincia', 'Total']]))
    
    titulacionesMaster = pd.read_excel(f"./Data/Espanya/Titulaciones/Masteres oficiales impartidos {anyo}.xlsx",
                                        sheet_name=0, skiprows=7, usecols=[0,1], names=['Universidad', 'Titulaciones'])
    titulacionesMaster['Provincia'] = titulacionesMaster['Universidad'].apply(lambda x: universidad_a_provincia[x])
    
    provincias[f'Masteres{anyo}'] = provincias['Provincia'].apply(lambda x: anyadirValores(x, titulacionesMaster))

  gdf = gpd.GeoDataFrame(provincias)
  gdf['geometry'] = gdf['geometry'].simplify(0.001, preserve_topology=True)

  return gdf

def main():
  st.set_page_config(
    page_title="Tipo de Titulaciones",
    page_icon="📃",
    layout='wide'
  )

  gdf = loadData()

  typeTit = st.sidebar.selectbox('Tipo de titulacion:', ['Máster', 'Grado'])

  if typeTit == 'Máster':
    anyo = st.sidebar.selectbox("Año:", anyos, 0)

    linear = LinearColormap(["white", "green", "red"], vmin=0, vmax=gdf[f'Masteres{anyo}'].max())
    linear.options = {"position": "top"}
    bounds = gdf.total_bounds

    m = folium.Map(zoom_start=6)
    m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
    linear.add_to(m)

    geojson = folium.GeoJson(data=json.loads(gdf.to_json()),
                              style_function = lambda feature: 
                              {
                              "fillColor": linear(feature['properties'].get(f'Masteres{anyo}')),
                              "color": "black",
                              "weight": 1,
                              "fillOpacity": 0.5
                              },
                              tooltip=folium.GeoJsonTooltip(
                              fields=["Provincia", f'Masteres{anyo}'],
                              aliases=["Provincia:", "Num. Másteres:"],
                              localize=True
                            ))

    geojson.add_to(m)

    st.title("Másteres por provincia en Espanya")
    st.write("Aquí se muestran la cantidad de programas de master ofertados por provincia. Se da la opción de " \
    "elegir tres posibles años a visualizar, pero nuevamente no existe gran diferencia entre ellos, cumpliendo que la mayoría se "
    "encuentran en Madrid y Barcelona.")
    st_folium(m, use_container_width=True, height=600, returned_objects=[])

  else:
    anyo = st.sidebar.selectbox("Año:", anyos, 0)
    typeGrad = st.sidebar.radio("Tipo de grado:", ['Ciencias', 'Salud', 'Sociales', 'Arte', 'Ingenieria', 'Total'])

    if typeGrad != 'Total':
      linear = LinearColormap(["white", "green", "red"], vmin=0, vmax=gdf[[f'Ciencias{anyo}', f'Salud{anyo}', f'Sociales{anyo}', f'Arte{anyo}', f'Ingenieria{anyo}']].max(axis=1).max())
    else:
      linear = LinearColormap(["white", "green", "red"], vmin=0, vmax=gdf[f'Total{anyo}'].max())
    linear.options = {"position": "top"}
    bounds = gdf.total_bounds

    m = folium.Map(zoom_start=6)
    m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
    linear.add_to(m)

    typeGrad = typeGrad + anyo

    geojson = folium.GeoJson(data=json.loads(gdf.to_json()),
                              style_function = lambda feature: 
                              {
                              "fillColor": linear(feature['properties'].get(typeGrad)),
                              "color": "black",
                              "weight": 1,
                              "fillOpacity": 0.5
                              },
                              tooltip=folium.GeoJsonTooltip(
                              fields=["Provincia", typeGrad],
                              aliases=["Provincia:", "Num. Grados:"],
                              localize=True
                            ))

    geojson.add_to(m)

    st.title("Grados por provincia en Espanya")
    st.write("Por otro lado, aquí se pueden ver los grados ofertados, pudiendose elegir por el tipo de los mismos. " \
    "Además, el rango se ha declarado a partir del máximo de todos los posibles tipos de grados (a excepción del total), de tal forma que se " \
    "puede también comparar las cantidades relativas entro los mismos. Con todo esto, se puede observar que existen más grados " \
    "relacionados con el apartado social y que, nuevamente, se concentran en Madrid y Barcelona.")
    st_folium(m, use_container_width=True, height=600, returned_objects=[])

main()