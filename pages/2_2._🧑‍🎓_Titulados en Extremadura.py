import streamlit as st
import plotly.express as px
import pandas as pd

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
    page_title="Titulaciones Extremadura",
    page_icon="🧑‍🎓",
    layout='wide'
  )

  type = st.sidebar.radio("Tipo de visualización:", ["Titulados por titulaciones", 
                                                     "Comparación de matriculados por género"])

  if type == "Titulados por titulaciones":
    st.header("Titulaciones con más alumnos titulados en Extremadura")
    st.write("En esta página se muestra en una gráfica de barras el subconjunto de las titulaciones impartidas en Extremadura " \
    "con el mayor número de alumnos titulados. El usuario puede decidir sobre que años, para que géneros y cuantas titulaciones mostrar " \
    "mediante los widgets proporcionados.")


    gender = st.sidebar.radio("Género:", ["Hombre", "Mujer", "Ambos"])
    start_year = st.sidebar.slider("Año inicio:", 2008, 2025, 2008, 1)
    if start_year < 2025:
      end_year = st.sidebar.slider("Año final:", start_year, 2025, step=1) 
    else:
      end_year = 2025

    num_tit = st.sidebar.slider("Número de titulaciones:", 1, 50, step=1)

    df = createDataFrame(gender, start_year, end_year, num_tit)
    fig = px.bar(df, x='Num. Titulados', y='Titulacion', labels={'Titulacion': 'Titulación', 'Num. Titulados': 'Número de Titulados'})
    fig.update_layout(title_text="Número de alumnos titulados por titulación", title_x=0.5, height= 80 + 920 * (num_tit / 50) ,margin=dict(l=20, r=20, t=40, b=30))
    st.plotly_chart(fig, use_container_width=True)
  else:
    st.header("Comparación entre matriculados por género")
    st.write("En esta página se muestra mediante gráficos de violín una comparación entre matriculados de cada año por género.")

    year =  st.sidebar.slider("Año: ", 2008, 2025, 2008, 1)
    df1 = loadDataFrame(year)[['Anyo', 'HPrMat']].fillna(0)
    df1['Sexo'] = 'Hombre'
    df1 = df1.rename(columns={'HPrMat': 'Matriculados'})

    df2 = loadDataFrame(year)[['Anyo', 'MPrMat']].fillna(0)
    df2 = df2.rename(columns={'MPrMat': 'Matriculados'})
    df2['Sexo'] = 'Mujer'
    
    df = pd.concat([df1, df2])
    fig = px.violin(df, x="Anyo", y="Matriculados", color="Sexo")
    st.plotly_chart(fig, use_container_width=True)

main()