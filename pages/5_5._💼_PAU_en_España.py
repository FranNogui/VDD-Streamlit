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

def contarValores(prov, tabla):
    valor = 0
    tableNP = tabla.to_numpy()
    for fila in tableNP:
        if prov in fila:
            valor += 1
    return valor if valor > 0 else 0

@st.cache_data
def loadData():
  directory = './Data/Espanya/Provincias/recintos_provinciales_inspire_peninbal_etrs89.shp'
  provincias = gpd.read_file(directory)
  provincias = provincias.to_crs("EPSG:4326")
  provincias = provincias[['NAMEUNIT', 'geometry']]
  provincias = provincias.rename(columns={'NAMEUNIT': 'Provincia'})

  pauPresentados = pd.read_excel("./Data/Espanya/PAU/Alumnado presentado a las PAU.xlsx",
                                  sheet_name=0, skiprows=8, usecols=[0,1], names=['Universidad', 'Presentados'])
  pauAprobados   = pd.read_excel("./Data/Espanya/PAU/Alumnado aprobado a las PAU.xlsx",
                                sheet_name=0, skiprows=8, usecols=[0,1], names=['Universidad', 'Aprobados'])
  
  pauPresentados['Provincia'] = pauPresentados['Universidad'].apply(lambda x: universidad_a_provincia[x])
  pauAprobados['Provincia']   = pauAprobados['Universidad'].apply(lambda x: universidad_a_provincia[x])

  provincias['Presentados'] = provincias['Provincia'].apply(lambda x: anyadirValores(x, pauPresentados))
  provincias['Aprobados']   = provincias['Provincia'].apply(lambda x: anyadirValores(x, pauAprobados))

  centros = pd.read_excel("./Data/Espanya/Centros/Centros por Universidades 2010-2011.xlsx",
                              sheet_name=0, skiprows=7, usecols=[0, 1, 2, 3, 4],
                              names=['Universidad', 'Total', 'Publicas', 'OtrosEntesPublicos', 'Privadas'])
      
  centros['Provincia'] = centros['Universidad'].apply(lambda x: universidad_a_provincia[x])
  centros = centros.replace('.', 0)

  provincias['Centros'] = provincias['Provincia'].apply(lambda x: contarValores(x, centros))
  provincias['Presentados por Universidad'] = provincias['Presentados'] / provincias['Centros']
  provincias = provincias.fillna(0)

  gdf = gpd.GeoDataFrame(provincias)
  gdf['geometry'] = gdf['geometry'].simplify(0.001, preserve_topology=True)

  return gdf

def typeOfStudy(name):
  firstWord = name.split(' ')[0]
  dobleGrado = ['DOBLE', 'DOB', 'PCEO:']
  master = ['MÁSTER']
  if firstWord in dobleGrado: return 'DOBLE GRADO'
  elif firstWord in master:   return 'MÁSTER'
  else: return 'GRADO'

def prepareDataFrame(df):
  df = df.drop(['uri', 'ou_indicadoresTitulacion'], axis=1)
  df['ID_Titulacion'] = df['rdfs_label'].apply(lambda x: x[-5:-1])
  df['rdfs_label'] = df['rdfs_label'].apply(lambda x: x[len(' Indicadores demandaUniversitara XXXX '):-6])
  df['Tipo_Estudio'] = df['rdfs_label'].apply(lambda x : typeOfStudy(x))
  df['ou_cursoAcademico'] = df['ou_cursoAcademico'].apply(lambda x: x[-4:])
  df = df.rename(columns={'ou_notaMinimaAccesoMayor45': 'NMAMayor45',
                          'ou_hombresPrimeraMatriculaPrimerCurso': 'HPrMatPrC',
                          'ou_extranjerosPrimeraMatricula': 'ExtrPrMat',
                          'ou_mujeresPrimeraMatriculaPrimerCurso': 'MPrMatPrC',
                          'ou_hombresPrimeraMatricula': 'HPrMat',
                          'ou_mujeresPrimeraMatricula': 'MPrMat',
                          'ou_notaMinimaAccesoTitulados': 'NMATitulados',
                          'ou_espanolesPrimeraMatricula': 'EspPrMat',
                          'ou_notaMinimaAccesoDeportistas': 'NMADeportistas',
                          'ou_notaMinimaAccesoGeneral': 'NMAGeneral',
                          'rdfs_label': 'Titulacion',
                          'ou_notaMinimaAccesoMayor25': 'NMAMayor25',
                          'ou_notaMinimaAccesoMayor40': 'NMAMayor40',
                          'ou_notaMinimaAccesoDiscapacitados': 'NMADiscapacitados',
                          'ou_cursoAcademico': 'Anyo'
                        })
  df = df[['Anyo', 'Titulacion', 'ID_Titulacion', 'Tipo_Estudio', 
          'EspPrMat', 'ExtrPrMat', 'HPrMatPrC', 'MPrMatPrC', 'HPrMat', 'MPrMat',
          'NMAGeneral', 'NMATitulados', 'NMAMayor25', 'NMAMayor40', 'NMAMayor45', 'NMADeportistas', 'NMADiscapacitados']]
  return df

@st.cache_data
def loadDataFrame(year):
  file_dir = f"./Data/Extremadura/IndicadoresDemandaUniversitaria{year}.csv"
  df = pd.read_csv(file_dir, encoding='utf-8')
  return prepareDataFrame(df)

def loadDataFrames(yearStart, yearEnd):
  frames=[]
  for i in range(yearStart, yearEnd+1):
    frames.append(loadDataFrame(i))
  return pd.concat(frames, ignore_index=True)

def createDataFrame(gender, start_year, end_year, num_tit):
  df = loadDataFrames(start_year, end_year)
  columns = []
  if gender == 'Hombre':  columns = ['HPrMat']
  elif gender == 'Mujer': columns = ['MPrMat']
  elif gender == 'Ambos': columns = ['HPrMat', 'MPrMat']
  columns += ['ID_Titulacion', 'Titulacion']
  df = df[columns].fillna(0)

  if gender == 'Ambos':
    df['Num. Titulados'] = df['HPrMat'] + df['MPrMat']
    df = df[['Num. Titulados', 'ID_Titulacion', 'Titulacion']]
  elif gender == 'Hombre':
    df = df.rename(columns={'HPrMat': 'Num. Titulados'})
  else:
    df = df.rename(columns={'MPrMat': 'Num. Titulados'})

  df = df.groupby('Titulacion', as_index=False)['Num. Titulados'].sum()
  df = df.sort_values(by=['Num. Titulados'], ascending=False, ignore_index=True)

  df = df.head(num_tit)

  df = df.sort_values(by=['Num. Titulados'], ascending=True, ignore_index=True)

  return df

def main():
  st.set_page_config(
    page_title="PAU",
    page_icon="💼",
    layout='wide'
  )

  gdf = loadData()

  typeInfo = st.sidebar.selectbox('Información:', ['Presentados', 'Aprobados', 'Presentados por Universidad', 'Notas de acceso en Extremadura'])

  if typeInfo == 'Presentados':
    linear = LinearColormap(["white", "blue"], vmin=0, vmax=gdf['Presentados'].max())
    linear.options = {"position": "top"}
    bounds = gdf.total_bounds

    m = folium.Map(zoom_start=6)
    m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
    linear.add_to(m)

    geojson = folium.GeoJson(data=json.loads(gdf.to_json()),
                              style_function = lambda feature: 
                              {
                              "fillColor": linear(feature['properties'].get('Presentados')),
                              "color": "black",
                              "weight": 1,
                              "fillOpacity": 0.5
                              },
                              tooltip=folium.GeoJsonTooltip(
                              fields=["Provincia", 'Presentados'],
                              aliases=["Provincia:", "Num. Presentados:"],
                              localize=True
                            ))

    geojson.add_to(m)

    st.title("Alumnos presentados a las PAU por provincia en 2011")
    st.write("Aquí se pueden observar la cantidad de alumnos que se presentaron a las PAU del año 2011 "
    "por provincia.")
    st_folium(m, use_container_width=True, height=600, returned_objects=[])

  elif typeInfo == 'Aprobados':
    linear = LinearColormap(["white", "green"], vmin=0, vmax=gdf['Aprobados'].max())
    linear.options = {"position": "top"}
    bounds = gdf.total_bounds

    m = folium.Map(zoom_start=6)
    m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
    linear.add_to(m)

    geojson = folium.GeoJson(data=json.loads(gdf.to_json()),
                              style_function = lambda feature: 
                              {
                              "fillColor": linear(feature['properties'].get('Aprobados')),
                              "color": "black",
                              "weight": 1,
                              "fillOpacity": 0.5
                              },
                              tooltip=folium.GeoJsonTooltip(
                              fields=["Provincia", 'Aprobados'],
                              aliases=["Provincia:", "Num. Aprobados:"],
                              localize=True
                            ))

    geojson.add_to(m)

    st.title("Alumnos aprobados en las PAU por provincia en 2011")
    st.write("Aquí se pueden observar la cantidad de alumnos que aprobaron las PAU del año 2011 "
    "por provincia.")
    st_folium(m, use_container_width=True, height=600, returned_objects=[])
  elif typeInfo == 'Presentados por Universidad':
    linear = LinearColormap(["white", "yellow"], vmin=0, vmax=gdf['Presentados por Universidad'].max())
    linear.options = {"position": "top"}
    bounds = gdf.total_bounds

    m = folium.Map(zoom_start=6)
    m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
    linear.add_to(m)

    geojson = folium.GeoJson(data=json.loads(gdf.to_json()),
                              style_function = lambda feature: 
                              {
                              "fillColor": linear(feature['properties'].get('Presentados por Universidad')),
                              "color": "black",
                              "weight": 1,
                              "fillOpacity": 0.5
                              },
                              tooltip=folium.GeoJsonTooltip(
                              fields=["Provincia", 'Presentados por Universidad'],
                              aliases=["Provincia:", "Presentados por Universidad:"],
                              localize=True
                            ))

    geojson.add_to(m)

    st.title("Alumnos presentados por universidad en cada provincia en 2011")
    st.write("Aquí se pueden observar la cantidad de alumnos por universidad que se presentaron a las PAU del año 2011 "
    "por provincia.")
    st_folium(m, use_container_width=True, height=600, returned_objects=[])
  else:
    df = loadDataFrames(2008, 2025)[['Anyo', 'NMAGeneral', 'Tipo_Estudio']].dropna()
    df = df.drop(df[df.NMAGeneral == 0].index)
    df = df.groupby('Anyo').agg({'NMAGeneral' : ['mean']})
    df.columns = ['_'.join(col) for col in df.columns]

    st.title("Evolución de las notas de acceso en Extremadura")
    st.write("Adicionalmente, aquí se puede ver la evolución de las notas de acceso en Extremadura "
    "desde el año 2011 hasta 2025.")
    st.line_chart(df, y='NMAGeneral_mean', x_label="Año", y_label="Nota media General")

main()