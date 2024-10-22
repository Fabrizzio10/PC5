import pandas as pd
import sqlite3

# Cargar el dataset
df_wine = pd.read_csv('./data/winemag-data-130k-v2.csv')

# Exploración básica del dataframe
print(df_wine.shape)  # Dimensiones del dataframe
print(df_wine.columns)  # Nombres de las columnas
print(df_wine.head())  # Primeras filas del dataframe

# Renombrar columnas
df_wine.rename(columns={
    'country': 'Country',
    'points': 'Points',
    'price': 'Price',
    'variety': 'Variety',
    'winery': 'Winery'
}, inplace=True)

# Crear nuevas columnas
# 1. Crear una columna de "Continent" en base al país
continent_map = {
    'US': 'North America', 'France': 'Europe', 'Italy': 'Europe', 'Chile': 'South America',
    'Argentina': 'South America', 'Australia': 'Oceania', 'Spain': 'Europe', 'Portugal': 'Europe'
}
df_wine['Continent'] = df_wine['Country'].map(continent_map)

# 2. Crear una columna "Price_Category" según el precio
df_wine['Price_Category'] = pd.cut(df_wine['Price'], bins=[0, 20, 50, 100, 500], labels=['Budget', 'Mid-range', 'Premium', 'Luxury'])

# 3. Crear una columna "Review_Length" para indicar la longitud de la descripción
df_wine['Review_Length'] = df_wine['description'].apply(len)

# 4. Crear una columna "Value_Score" calculada como puntos/precio
df_wine['Value_Score'] = df_wine['Points'] / df_wine['Price']

# Reporte 1: Vinos mejor puntuados por continente
best_wines_by_continent = df_wine.groupby('Continent').apply(lambda x: x.nlargest(1, 'Points'))
best_wines_by_continent.reset_index(drop=True, inplace=True)
print(best_wines_by_continent[['Country', 'Points', 'Price', 'Variety', 'Winery']])

# Reporte 2: Promedio de precio y cantidad de reviews por país, ordenado por precio promedio
price_reviews_by_country = df_wine.groupby('Country').agg(
    avg_price=('Price', 'mean'),
    num_reviews=('description', 'count')
).sort_values(by='avg_price', ascending=False)
print(price_reviews_by_country)

# Reporte 3: Vinos con mejor relación calidad/precio
best_value_wines = df_wine[df_wine['Value_Score'].notnull()].sort_values(by='Value_Score', ascending=False).head(10)
print(best_value_wines[['Country', 'Points', 'Price', 'Value_Score', 'Winery']])

# Reporte 4: Cantidad de vinos por categoría de precio
wine_by_price_category = df_wine['Price_Category'].value_counts()
print(wine_by_price_category)

# Exportar los reportes a distintos formatos
# 1. CSV
best_wines_by_continent.to_csv('best_wines_by_continent.csv', index=False)

# 2. Excel
price_reviews_by_country.to_excel('price_reviews_by_country.xlsx', index=True)

# 3. SQLite
conn = sqlite3.connect('wine_data.db')
best_value_wines.to_sql('best_value_wines', conn, if_exists='replace', index=False)
conn.close()

# 4. Enviar un archivo como adjunto en un correo (no implementado aquí)
# Se puede usar 'smtplib' o servicios como Gmail API o SendGrid para enviar correos con adjuntos.
# Este paso depende de la configuración del servicio de correo electrónico.

print("Reportes generados y exportados con éxito.")