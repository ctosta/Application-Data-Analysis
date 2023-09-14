######## author = Caroline Tosta
######## insitution = Comunidade DS
######## website = https://www.linkedin.com/in/ctosta/
######## version = 2.0

# --------------------------------------------------------------------- FOME ZERO --------------------------------------------------------------------
# Libraries #
import pandas                       as pd
import numpy                        as np
import inflection
import folium
import streamlit                    as st
import plotly.express               as px
import plotly.graph_objects         as go

from numerize                       import numerize                     as nm
from haversine                      import haversine
from streamlit_folium               import folium_static
from PIL                            import Image
from streamlit_option_menu          import option_menu
from folium.plugins                 import MarkerCluster


st.set_page_config(
    page_title = "Fome Zero",
    page_icon = "🍴",
    layout= "wide"
)

# Import dataset #

data = pd.read_csv('dataset/zomato.csv')

df = data.copy()

#-----------------------------------------------------------------------FUNCÕES DF--------------------------------------------------------------------

# Excluir linhas NaN e duplicadas

def clean_code (df):

    df = df.dropna()
    df = df.drop_duplicates()
    
    return df

df = clean_code (df)

#Renomear as colunas do df

def rename_columns(df):
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ","")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df

df = rename_columns(df)


# Alterar linhas

def change_rows (df):
    
    df['cuisines'] = df.loc[ :, "cuisines"].apply(lambda x: x.split(",")[0])
    df["restaurant_name"]= df["restaurant_name"].str.title()
    
    return df

df = change_rows (df)


# Substituindo código/países

def country_name (df):
    df['country_code'] = df['country_code'].map({
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
})
    return df   

df = country_name(df)


#Renomeando linhas de uma coluna específica

def create_price_type (df):
    df['price_range'] = df['price_range'].map({
    1: "Cheap",
    2: "Normal",
    3: "Expensive",
    4: "Gourmet",
})
    return df

df = create_price_type(df)   


# Definindo cores

def color_name (df):
    df['rating_color'] = df['rating_color'].map({
    '3F7E00': 'darkgreen',
    '5BA829': 'green',
    '9ACD32': 'lightgreen',
    'CDD614': 'orange',
    'FFBA00': 'red',
    'CBCBC8': 'darkred',
    'FF7800': 'darkred',
})
    return df 

df = color_name(df)

# Criando uma coluna com os valores de um prato para duas pessoas em dólar

def price_in_dollar (df):
    df['price_in_dollar'] = df[['currency', 'average_cost_for_two']].apply(lambda x: (x['average_cost_for_two'] / 12.85) if x['currency'] == 'Botswana Pula(P)' else
                                                                                     (x['average_cost_for_two'] / 5.31) if x['currency'] == 'Brazilian Real(R$)' else
                                                                                     (x['average_cost_for_two'] / 1) if x['currency'] == 'Dollar($)' else
                                                                                     (x['average_cost_for_two'] / 3.67) if x['currency'] == 'Emirati Diram(AED)' else
                                                                                     (x['average_cost_for_two'] / 82.68) if x['currency'] == 'Indian Rupees(Rs.)' else
                                                                                     (x['average_cost_for_two'] / 15608.45) if x['currency'] == 'Indonesian Rupiah(IDR)' else
                                                                                     (x['average_cost_for_two'] / 1.57) if x['currency'] == 'NewZealand($)' else
                                                                                     (x['average_cost_for_two'] / 0.819257) if x['currency'] == 'Pounds(£)' else
                                                                                     (x['average_cost_for_two'] / 3.64) if x['currency'] == 'Qatari Rial(QR)' else
                                                                                     (x['average_cost_for_two'] / 17.59) if x['currency'] == 'Rand(R)' else
                                                                                     (x['average_cost_for_two'] / 366.86) if x['currency'] == 'Sri Lankan Rupee(LKR)' else
                                                                                     (x['average_cost_for_two'] / 18.65) if x['currency'] == 'Turkish Lira(TL)' else 0, axis = 1)
    return df

df = price_in_dollar(df)

#---------------------------------------------------------------------------------FILTRO-----------------------------------------------------------------------------------
def select_countries (df):
    all_countries = ['Philippines', 'Brazil', 'Australia', 'United States of America',
                     'Canada', 'Singapure', 'United Arab Emirates', 'India',
                     'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
                     'Sri Lanka', 'Turkey']

    container = st.container()
    all_countries = df.loc[:, 'country_code'].unique().tolist()   
        
    container = st.container()
    paises = container.multiselect(
        'Escolha os países que deseja visualizar as informações',
        all_countries,
        default = all_countries
    )
    
    return paises

# --------------------------------------------------------------------------MENU PAÍSES---------------------------------------------------------------------------------
def cols_operations (df, col1, col2, operation, labelx, labely, order):
    if operation == 'count':
        
        df_aux = df.loc[:, [col1, col2]].groupby(col1).count().reset_index()
        fig = px.bar(df_aux, x = col1, y = col2, text_auto=True, color = col1, 
                     color_discrete_sequence = px.colors.sequential.amp, 
                     labels={col2:labely, col1:labelx}, height= 600)
        
        fig.update_traces(textfont_size=14, textposition="outside", marker_line_color='rgb(69, 71, 72, 1)', 
                          marker_line_width=0.8)
        fig.update_layout(barmode='stack', xaxis={'categoryorder': order}, showlegend=False)
    
    elif operation == 'nunique':
        df_aux = df.loc[:, [col1, col2]].groupby(col1).nunique().reset_index()
        fig = px.bar(df_aux, x = col1, y = col2, text_auto=True, color = col1,
                     color_discrete_sequence = px.colors.sequential.amp, 
                    labels={col2:labely, col1:labelx}, height= 600)
        fig.update_traces(textfont_size=14, textposition="outside", marker_line_color='rgb(69, 71, 72, 1)', 
                          marker_line_width=0.8)
        fig.update_layout(barmode='stack', xaxis={'categoryorder': order}, showlegend=False)
        
    elif operation == 'mean':
        df_aux = np.round ( df.loc[:, [col1, col2]].groupby(col1).mean().reset_index(), 2)
        fig = px.bar(df_aux, x = col1, y = col2, text_auto=True, color = col1,
                     color_discrete_sequence = px.colors.sequential.amp, 
                    labels={col2:labely, col1:labelx}, height= 600)
        fig.update_traces(textfont_size=14, textposition="outside", marker_line_color='rgb(69, 71, 72, 1)', 
                          marker_line_width=0.8)
        fig.update_layout(barmode='stack', xaxis={'categoryorder': order}, showlegend=False)
    
    return fig

def df_tables (df, condicao):
    if condicao == 'mean':
        df_tab = np.round(df.loc[: ,['country_code', 'price_in_dollar']]
                         .groupby('country_code')
                         .mean('price_in_dollar')
                         .sort_values(['price_in_dollar'], ascending = False)
                         .reset_index(),2)
        df_tab.columns = ['Country', 'Average Cost for Two (US$)']
    
    elif condicao == 'nunique':
        df_tab = np.round(df.loc[:, ['country_code', 'cuisines']]
                            .groupby('country_code')
                            .nunique()
                            .sort_values(by = 'cuisines', ascending = False)
                            .reset_index(),2)
        df_tab.columns = ['Country', 'Cuisines']
    
    return df_tab

# -----------------------------------------------------MENU CIDADES-------------------------------------------------------------------------

def top_ten_countries (df):
    lin = (df['country_code'].isin(paises))
    df_aux = (df.loc[lin,['restaurant_name','city', 'country_code']]
                .groupby(['city','country_code'])
                .nunique()
                .sort_values(by = 'restaurant_name', ascending = True)
                .tail(10)
                .reset_index())
    fig = px.bar(df_aux, x = 'city', y = 'restaurant_name', color = 'country_code',  
                 color_discrete_sequence = px.colors.sequential.amp, text_auto=True, 
                 labels={'city': 'Cidades', 'restaurant_name':'Quantidade de Restaurantes', 
                         'country_code':'Países'}, height= 600)

    fig.update_traces(textfont_size=14, textposition="outside", marker_line_color='rgb(69, 71, 72, 1)', marker_line_width=0.8)
    fig.update_layout(xaxis={'categoryorder': 'total descending'})
    
    return fig

def avg_topseven_cities (df, condition, mean):
    lin = (df['country_code'].isin(paises))
    if condition == 'maior_igual':
        df_aux = (df.loc[(df['aggregate_rating'] >= mean) & lin,['restaurant_name','city', 'country_code']]
                    .groupby(['country_code','city'])
                    .count()
                    .sort_values('restaurant_name', ascending = False)
                    .head(7)
                    .reset_index())

        fig = px.bar(df_aux, x = 'city', y = 'restaurant_name', 
                     color = 'country_code', color_discrete_sequence = px.colors.sequential.amp, text_auto=True, 
                     labels={'city': 'Cidades', 'restaurant_name':'Quantidade de Restaurantes', 
                             'country_code':'Países'}, height= 600)
        
        fig.update_traces(textfont_size=14, textposition="outside", marker_line_color='rgb(69, 71, 72, 1)',marker_line_width=0.8)
        fig.update_layout(xaxis={'categoryorder': 'total descending'})
    
    elif condition == 'menor_igual':
        df_aux = (df.loc[(df['aggregate_rating'] <= mean) & lin,['restaurant_name','city', 'country_code']]
                    .groupby(['country_code','city'])
                    .count()
                    .sort_values('restaurant_name', ascending = False)
                    .head(7)
                    .reset_index())

        fig = px.bar(df_aux, x = 'city', y = 'restaurant_name', 
                     color = 'country_code', color_discrete_sequence = px.colors.sequential.amp, text_auto=True,
                     labels={'city': 'Cidades', 'restaurant_name':'Quantidade de Restaurantes', 
                             'country_code':'Países'}, height= 600)
        
        fig.update_traces(textfont_size=14, textposition="outside", marker_line_color='rgb(69, 71, 72, 1)',marker_line_width=0.8)
        fig.update_layout(xaxis={'categoryorder': 'total descending', })
        
    return fig

def cooking_varieties (df):
    lin = (df['country_code'].isin(paises))
    df_aux = (df.loc[lin, ['country_code', 'city', 'cuisines']]
                .groupby(['city', 'country_code'])
                .nunique()
                .sort_values(by = 'cuisines', ascending = False)
                .head(10)
                .reset_index())
    fig = px.bar(df_aux, x = 'city', y = 'cuisines', color = 'country_code', color_discrete_sequence = px.colors.sequential.amp, 
                 text_auto=True, labels={'cuisines': 'Tipos de Cozinha', 'city':'Cidades', 'country_code': 'Países'}, height= 800)
    
    fig.update_traces(textfont_size=14, textposition="outside", marker_line_color='rgb(69, 71, 72, 1)',marker_line_width=0.8)
    fig.update_layout(xaxis={'categoryorder': 'total descending'}, )
    
    return fig
#------------------------------------------------------------------------------MENU CULINÁRIAS--------------------------------------------------------------------------

def top_cuisines (df, condicao, top_culinarias):
    if condicao == 'melhor':
        df_aux = np.round(df.loc[(df['aggregate_rating']  >= 4.0) & (df['rating_text']  != 'Not rated'), ['cuisines','aggregate_rating']]
                            .groupby(['cuisines'])
                            .mean('aggregate_rating')
                            .sort_values('aggregate_rating', ascending = False)
                            .reset_index(), 2)
        df_fig = df_aux.head(top_culinarias)
        fig = px.bar(df_fig, x = 'aggregate_rating', y = 'cuisines', color = 'cuisines', color_discrete_sequence = px.colors.sequential.amp, 
                     text_auto=True, labels={'cuisines': 'Tipos de Cozinha', 'aggregate_rating':'Média de Avaliação'}, height= 800)
        fig.update_traces(textfont_size=14, textposition="outside", marker_line_color='rgb(69, 71, 72, 1)',marker_line_width=0.8)
        fig.update_layout(yaxis={'categoryorder': 'total ascending'}, showlegend=False)


    elif condicao == 'pior':
        df_aux = np.round(df.loc[(df['aggregate_rating']  >= 0.0) &  (df['rating_text']  != 'Not rated'), ['cuisines','aggregate_rating']]
                            .groupby(['cuisines'])
                            .mean('aggregate_rating')
                            .sort_values('aggregate_rating', ascending = True)
                            .reset_index(), 2)
        df_fig = df_aux.head(top_culinarias)
        fig = px.bar(df_fig, x = 'aggregate_rating', y = 'cuisines', color = 'cuisines', color_discrete_sequence = px.colors.sequential.amp, 
                     text_auto=True, labels={'cuisines': 'Tipos de Cozinha', 'aggregate_rating':'Média de Avaliação'}, height= 800)
        fig.update_traces(textfont_size=14, textposition="outside", marker_line_color='rgb(69, 71, 72, 1)',marker_line_width=0.8)
        fig.update_layout(yaxis={'categoryorder': 'total descending'}, showlegend=False)
    
    return fig

def zero_rating(df):
    df_zero = np.round(df.loc[(df['aggregate_rating']  == 0.0), ['restaurant_name', 'cuisines','country_code', 'city','aggregate_rating', 'price_range']]
                     .groupby(['restaurant_name', 'cuisines', 'country_code', 'city', 'price_range'])
                     .mean('aggregate_rating')
                     .sort_values('aggregate_rating', ascending = True)
                     .reset_index(), 2)
    df_zero.columns = ['Restaurant', 'Cuisines', 'Country', 'City', 'Price Range' ,'Aggregate Rating']
    
    return df_zero

#-----------------------------------------------------------------------------MENU RESTAURANTES -----------------------------------------------------------------------
def country_maps (df):
    
    df_maps = (df.loc[:, ['restaurant_name','city', 'latitude','longitude', 'rating_color', 'price_range']]
                 .groupby(['city', 'restaurant_name','rating_color', 'price_range'])
                 .median()
                 .reset_index())
    
    map_ = folium.Map( zoom_start = 16)

    marker_cluster = MarkerCluster().add_to(map_)

    for index, location_info in df_maps.iterrows():
        folium.Marker (
            location = [location_info['latitude'], location_info['longitude']],
            popup = location_info ['price_range'],
            tooltip= location_info ['restaurant_name'],
            icon = folium.Icon (color = location_info['rating_color'], prefix = 'fa', icon = 'circle'),
    ).add_to(marker_cluster)
    
    folium_static (map_, width =1024)
    
    return None

def top_restaurants(df):
    cols = ['restaurant_name', 'country_code', 'city', 'cuisines', 'price_range','price_in_dollar', 'aggregate_rating', 'votes']
    lin = (df['aggregate_rating'] <= 4.9) & (df['country_code'].isin(paises))
            
            
    dataframe= np.round(df.loc[lin,cols]
                 .groupby(['restaurant_name', 'cuisines', 'country_code', 'city', 'price_range'])
                 .mean(['aggregate_rating','votes'])
                 .sort_values(['aggregate_rating','votes'], ascending = False)
                 .reset_index(),2)
    dataframe.columns = ['Restaurant',' Cuisines','Country', 'City', 'Price Range','Average Cost for Two (US$)', 'Aggregate Rating', 'Votes']
    df2 = dataframe.head(top_20)
    
    return df2
#-----------------------------------------------------------------------------BARRA LATERAL-----------------------------------------------------------------------------
image = Image.open('page/logo.png')
st.sidebar.image(image, width = 220)

st.sidebar.markdown ("""---""")
# Painel lado esquerdo #
with st.sidebar.container():
    
    result = df['restaurant_name'].nunique()
    st.markdown(f'### 🍽️  {nm.numerize((result))}  Restaurantes')
    
with st.sidebar.container():
    
    result = df['country_code'].nunique()
    st.markdown(f'### 🌎  {result}  Países')

with st.sidebar.container():
    
    result = df['city'].nunique()
    st.markdown(f'### 🏙️  {result} Cidades')
    
with st.sidebar.container():
    
    result = df['cuisines'].nunique()
    st.markdown(f'### 🥘  {result} Tipos de Culinária')  

with st.sidebar.container():
    
    result = np.sum(df['votes']).item()
    st.markdown(f'### ⭐  {nm.numerize((result),3)} Avaliações')    

st.sidebar.markdown ("""---""")
st.sidebar.markdown ('###### Powered by Caroline Tosta - Comunidade DS')

#---------------------------------------------------------------------------------------------------------------------------------------------------------------
st.header("Fome Zero")
st.markdown("#### 📍 O melhor lugar para encontrar seu mais novo restaurante preferido!")

selected = option_menu(
    menu_title = None,
    options = ['Países','Cidades', 'Culinárias', 'Restaurantes'], 
    default_index = 0,
    orientation = 'horizontal',
)

if selected == 'Países':
    menu_countries = st.container()
    
    with menu_countries:
        
        with st.container():
            st.markdown("""---""")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown ('###### _Quantidade de Restaurantes por País_')
                fig = cols_operations(df, 'country_code', 'restaurant_name', 'count', 'Países', 'Quantidade de Restaurantes', 'total descending')
                st.plotly_chart (fig, use_container_width = True)

            with col2:
                st.markdown ('###### _Quantidade de Cidades Avaliadas por País_')
                fig = cols_operations(df, 'country_code', 'city', 'nunique', 'Países', 'Quantidade de Cidades Avaliadas', 'total descending')
                st.plotly_chart (fig, use_container_width = True)
        
        with st.container():
            st.markdown("""---""")
            col3, col4 = st.columns(2)
            
            with col3:
                st.markdown ('###### _Quantidade de Avaliações feitas por País_')
                df_aux = df.loc[df['votes'] != 0, ['country_code', 'votes']].groupby('country_code').count().reset_index()
                fig = px.bar(df_aux, x = 'country_code', y = 'votes', text_auto=True, color = 'country_code', 
                             color_discrete_sequence = px.colors.sequential.amp, 
                             labels={'votes':'Quantidade de Avaliações', 'country_code':'Países'}, height= 600)
        
                fig.update_traces(textfont_size=14, textposition="outside", marker_line_color='rgb(69, 71, 72, 1)', 
                          marker_line_width=0.8)
                fig.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'}, showlegend=False)
                st.plotly_chart (fig, use_container_width = True)
                
            with col4:
                st.markdown ('###### _Média de Preço (US$) de um prato para 2 pessoas por País_')
                df_tab = df_tables(df,'mean')
                st.dataframe(df_tab.style.format({'Average Cost for Two (US$)': '{:.2f}'}), use_container_width = True)
                
        with st.container():
            st.markdown("""---""")
            st.markdown ('###### _Médias de Avaliações por Países_')
            fig = cols_operations (df, 'country_code', 'aggregate_rating', 'mean', 'Países', 'Avaliações', 'total descending')
            st.plotly_chart (fig, use_container_width = True)
        
            

elif selected == 'Cidades':
    menu_cities = st.container()
    
    with menu_cities:
        paises = select_countries(df)
            
        with st.container():
            st.markdown("""---""")
            st.markdown('######  _Top 10 Cidades com mais Restaurantes_')
            fig = top_ten_countries(df)
            st.plotly_chart (fig, use_container_width = True)


        with st.container():
            st.markdown ("""---""")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown ('######  _Top 7 Cidades com Restaurantes com Média de Avaliação acima de 4_')
                fig = avg_topseven_cities (df, 'maior_igual', 4.0)
                st.plotly_chart (fig, use_container_width = True)

            with col2:
                st.markdown ('######  _Top 7 Cidades com Restaurantes com Média de Avaliação abaixo de 2.5_')
                fig = avg_topseven_cities (df, 'menor_igual', 2.5)
                st.plotly_chart (fig, use_container_width = True)

        with st.container():
            st.markdown ("""---""")
            st.markdown('######  _Top 10 Cidades com mais Variedades Culinárias_')
            fig = cooking_varieties(df)
            st.plotly_chart (fig, use_container_width = True)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
elif selected == 'Culinárias':
    menu_culinarias = st.container()
    
    with menu_culinarias:
        
        top_culinarias = st.slider('Escolha a Quantidade de Tipos de Culinárias', 0, 20, 10)
        st.markdown ("""---""")
        
        
        with st.container():
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f'###### _Top {top_culinarias}: Os Melhores Tipos de Culinárias_')
                fig = top_cuisines(df, 'melhor', top_culinarias)
                st.plotly_chart (fig, use_container_width = True)
        
            with col2:
                st.markdown(f'###### _Top {top_culinarias}: Os Piores Tipos de Culinárias_')
                fig = top_cuisines(df, 'pior', top_culinarias)
                st.plotly_chart (fig, use_container_width = True)
#----------------------------------------------------------------------------------------------------------------------------------------
        
    
elif selected == 'Restaurantes':
    menu_restaurantes = st.container()
    
    with menu_restaurantes:
        
        with st.container():
            st.subheader(f'_Localização dos Restaurantes_')
            country_maps(df)
        
        
        with st.expander("Clica em cima para ver o Top Restaurantes de cada País"):
            top_20 = st.slider('Escolha a Quantidade de Restaurantes', 0, 20, 10)
        
            paises = select_countries(df)

            with st.container():
                st.markdown("""---""")
                st.subheader(f'_Top {top_20}: Restaurantes_')
                df2 = top_restaurants(df)
                st.dataframe(df2.style.format({'Average Cost for Two (US$)': '{:.2f}', 'Aggregate Rating': '{:.2f}', 'Votes': '{:.0f}'}), use_container_width = True)
        
        with st.expander("Clica em cima para ver os Restaurantes que não receberam Avaliação"):
            st.markdown ('###### _Restaurantes e Culinárias com avaliação 0_')
            df_zero = zero_rating(df)
            st.dataframe(df_zero.style.format({'Aggregate Rating': '{:.2f}'}), use_container_width = True)
