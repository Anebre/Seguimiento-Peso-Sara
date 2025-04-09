import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(page_title="Seguimiento Peso - Sara Natalia", layout="centered")

st.title("👶 Seguimiento del Peso de Sara Natalia")
st.write("Esta app te permite registrar y visualizar el crecimiento de tu bebé comparado con el peso ideal.")

# Cargar archivo Excel
archivo = st.file_uploader("📂 Sube tu archivo de seguimiento (.xlsx)", type=["xlsx"])

if archivo:
    df = pd.read_excel(archivo)
    df["Fecha"] = pd.to_datetime(df["Fecha"])
    df = df.sort_values("Fecha")

    # Mostrar tabla
    st.subheader("📊 Datos registrados")
    st.dataframe(df)

    # Gráfico de evolución
    st.subheader("📈 Evolución del peso")
    fig, ax = plt.subplots()
    ax.plot(df["Fecha"], df["Peso Real, gramos"], marker='o', label="Peso Real", linewidth=2)
    ax.plot(df["Fecha"], df["Peso ideal, gramos"], marker='s', linestyle='--', label="Peso Ideal")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Peso (g)")
    ax.legend()
    st.pyplot(fig)

    # Registro de nuevo peso
    st.subheader("➕ Ingresar nuevo peso")
    nueva_fecha = st.date_input("Fecha de medición")
    nuevo_peso = st.number_input("Peso real (en gramos)", step=10)

    if st.button("Guardar nuevo registro"):
        # Buscar día correspondiente
        dia = (nueva_fecha - pd.to_datetime("2025-03-25")).days
        ideal = df[df["Dia"] == dia]["Peso ideal, gramos"].values
        if len(ideal) == 0:
            st.error("No hay peso ideal proyectado para esa fecha. Actualiza el archivo.")
        else:
            ideal = ideal[0]
            diferencia = nuevo_peso - ideal
            porcentaje = diferencia / ideal
            alerta = "¡Alerta!" if porcentaje < -0.10 else ""
            nuevo_registro = pd.DataFrame([{
                "Fecha": nueva_fecha,
                "Dia": dia,
                "Peso Real, gramos": nuevo_peso,
                "Peso ideal, gramos": ideal,
                "Diferencia (g)": diferencia,
                "% Diferencia": porcentaje,
                "Alerta": alerta
            }])
            df = pd.concat([df, nuevo_registro], ignore_index=True).sort_values("Fecha")
            st.success("Registro agregado con éxito ✅")

    # Exportar archivo actualizado
    st.subheader("📥 Descargar seguimiento actualizado")
    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    st.download_button("Descargar Excel", data=buffer.getvalue(), file_name="Peso_SaraNatalia_Actualizado.xlsx")
