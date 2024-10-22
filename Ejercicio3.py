import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient

# Conectar a MongoDB
mongo_connection_string = "mongodb+srv://pingoaguilarf:<db:password>@clustermongodb.9rwca.mongodb.net/?retryWrites=true&w=majority&appName=ClusterMongoDb"

client = MongoClient(mongo_connection_string)

# Conectar a MongoDB Atlas
client = MongoClient(mongo_connection_string)

# Crear una base de datos llamada 'youtube_db' y una colección llamada 'videos'
db = client['youtube_db']
collection = db['videos']

# Cargar el archivo .txt
txt_file = './youtube_data/0333.txt'
df = pd.read_csv(txt_file, sep='\t', header=None)

# Imprimir las primeras filas y la cantidad de columnas
print("Primeras filas del DataFrame:")
print(df.head())
print(f"Número de columnas en el DataFrame: {df.shape[1]}")

# Asignar nombres a las columnas
df.columns = ['video_id', 'uploader', 'age', 'category', 'length', 'views', 'rate', 'ratings', 'comments', 'related_IDs'] + [f'related_id_{i}' for i in range(1, 20)]

# Filtrar solo las columnas que nos interesan
df_filtered = df[['video_id', 'uploader', 'age', 'category', 'length', 'views', 'rate', 'ratings', 'comments', 'related_IDs']]

# Filtrar por categorías de interés (ejemplo: 'Music', 'Entertainment', 'Education')
categories_of_interest = ['Music', 'Entertainment', 'Education']
df_filtered = df_filtered[df_filtered['category'].isin(categories_of_interest)]

# Exportar los datos a MongoDB Atlas
collection.insert_many(df_filtered.to_dict('records'))
print("Datos exportados a MongoDB Atlas correctamente.")

# Gráfico 1: Número de videos por categoría
videos_by_category = df_filtered['category'].value_counts()

plt.figure(figsize=(8,6))
videos_by_category.plot(kind='bar', color='skyblue')
plt.title('Número de Videos por Categoría')
plt.xlabel('Categoría')
plt.ylabel('Cantidad de Videos')
plt.show()

# Gráfico 2: Visualizaciones vs Calificación
plt.figure(figsize=(8,6))
plt.scatter(df_filtered['views'], df_filtered['rate'], color='green', alpha=0.5)
plt.title('Relación entre Visualizaciones y Calificación')
plt.xlabel('Visualizaciones')
plt.ylabel('Calificación')
plt.show()