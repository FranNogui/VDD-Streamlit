import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
import json
from streamlit_folium import st_folium
from branca.colormap import linear, LinearColormap

universidad_a_provincia = {
    "Alcalá de Henares": "Madrid",
    "Alicante": "Alacant/Alicante",
    "Almería": "Almería",
    "Autónoma de Barcelona": "Barcelona",
    "Autónoma de Madrid": "Madrid",
    "Barcelona": "Barcelona",
    "Burgos": "Burgos",
    "Cádiz": "Cádiz",
    "Cantabria": "Cantabria",
    "Carlos III": "Madrid",
    "Castilla-La Mancha": "Ciudad Real",
    "Complutense de Madrid": "Madrid",
    "Córdoba": "Córdoba",
    "Extremadura": "Badajoz",
    "Girona": "Girona",
    "Granada": "Granada",
    "Huelva": "Huelva",
    "Illes Balears": "Illes Balears",
    "Islas Baleares": "Illes Balears",
    "Jaén": "Jaén",
    "Jaume I de Castellón": "Castelló/Castellón",
    "La Rioja": "La Rioja",
    "León": "León",
    "Lleida": "Lleida",
    "Málaga": "Málaga",
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
    "CENTROS ADSCRITOS A UNIV. PUBLICAS": "CENTROS ADSCRITOS A UNIV. PUBLICAS"
}

@st.cache_data
def loadData():
  directory = './Data/Espanya/Provincias/recintos_provinciales_inspire_peninbal_etrs89.shp'
  provincias = gpd.read_file(directory)
  provincias = provincias.to_crs("EPSG:4326")
  provincias = provincias[['NAMEUNIT', 'geometry']]
  provincias = provincias.rename(columns={'NAMEUNIT': 'Provincia'})
  provinciasNames = provincias.drop(columns=['geometry'])
  gdf = gpd.GeoDataFrame(provincias)

  return provincias, provinciasNames, gdf

def main():
  prov, provNames, gdf = loadData()

  gdf['geometry'] = gdf['geometry'].simplify(0.001, preserve_topology=True)

  m = folium.Map(zoom_start=6)

  prov['geometry'] = prov['geometry'].simplify(0.001, preserve_topology=True)

  bounds = gdf.total_bounds
  m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])

  geojson = folium.GeoJson(data=json.loads(gdf.to_json()))
  geojson.add_to(m)

  st_folium(m, use_container_width=True, height=600, returned_objects=[])

main()