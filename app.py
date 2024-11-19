
import streamlit as st
import requests
from PIL import Image, ImageDraw
import io

# Cambiar el color de fondo
page_bg = """
<style>
/* Fondo general de la página */
    [data-testid="stAppViewContainer"] {
        background-color: #f0f0f5; /* Color claro */
        color: black; /* Texto negro */
    }

/* Fondo del Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f0f0f5; /* Color del sidebar */
        color: black;
    }

/* Opcional: Cambiar estilo de los encabezados */
    h1, h2, h3, h4, h5, h6 {
        color: #333333; /* Color del texto de encabezados */
    }
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Configuración de la aplicación en Streamlit
st.title("Detección de armas de fuego")
st.write("Sube una imagen para ver las predicciones")

# Subida de imagen
uploaded_file = st.file_uploader("Selecciona una imagen", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Mostrar la imagen cargada
    image = Image.open(uploaded_file)
    st.image(image, caption='Imagen subida', use_column_width=True)

    # Convertir la imagen a bytes para enviar a la API
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='JPEG')
    image_bytes = image_bytes.getvalue()

    # Realizar la solicitud a la API
    response = requests.post(
        "http://127.0.0.1:8000/predict/",  # URL de la API
        files={"file": image_bytes}
    )

    if response.status_code == 200:
        # Obtener las predicciones y mostrarlas
        predicciones = response.json().get("predicciones", [])
        st.write(f"Se han encontrado {len(predicciones)} objetos detectados.")
        
        for pred in predicciones:
            st.write(f"Índice de clase: {pred['índice_clase']} | Confianza: {pred['confianza']:.2f}")
        
        # Mostrar la imagen con las cajas de las predicciones
        pred_image = image.copy()
        draw = ImageDraw.Draw(pred_image)

        for pred in predicciones:
            # Aquí deberías agregar lógica para dibujar las cajas en la imagen usando las coordenadas
            # Suponiendo que ya tienes las coordenadas de las predicciones
            x_min, y_min, x_max, y_max = pred["coordenadas"]
            draw.rectangle([x_min, y_min, x_max, y_max], outline="blue", width=3)
        
        st.image(pred_image, caption='Imagen procesada satisfactoriamente', use_column_width=True)
    else:
        st.write("Error en la solicitud a la API.")
