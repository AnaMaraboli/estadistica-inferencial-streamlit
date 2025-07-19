import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm, t

def run():

    st.title("✅Bloque 2: Pruebas de hipótesis para una media")

    opcion = st.sidebar.radio("Elige un tema:", [
        "Tipos de errores (I y II)",
        "Pruebas de una y dos colas",
        "Cálculo del estadístico Z o t",
        "Decisión: rechazar o no H₀",
        "Ejemplo interactivo"
    ])

    if opcion == "Tipos de errores (I y II)":
        st.header("Tipos de errores")
        st.write("""
        En toda prueba estadística hay dos tipos de errores posibles:

        - **Error tipo I (α):** Rechazar la hipótesis nula (H₀) cuando en realidad es verdadera.
        - **Error tipo II (β):** No rechazar H₀ cuando en realidad es falsa.

        - El nivel de significancia (α) es la probabilidad de cometer error tipo I.
        - La potencia de la prueba (1 - β) es la probabilidad de detectar un efecto real.
                 
        En pruebas de hipótesis, no se pueden eliminar totalmente los errores, 
        porque siempre trabajamos con datos muestrales y hay incertidumbre. 
        Lo que sí podemos es controlar las probabilidades de cometerlos.

        🔴 Error Tipo I (α)

        Definición: Rechazar la hipótesis nula (H₀) cuando en realidad es verdadera.

        Cómo controlarlo: fijamos un nivel de significancia α (por ejemplo, 0.05) antes de hacer la prueba.

        Ejemplo: Acusar a un inocente.

        🟠 Error Tipo II (β)

        Definición: No rechazar H₀ cuando en realidad es falsa.

        Cómo reducirlo: aumentando el tamaño de muestra o usando una prueba con mayor potencia.

        Ejemplo: Dejar libre a un culpable.
        """)

        st.write("### Interactividad: relación entre α y los errores")
    

        alpha_slider = st.slider("Selecciona nivel de significancia (α)", 0.01, 0.2, 0.05)
        # Para ilustrar, asumimos que al reducir α aumenta β (relación conceptual)
        beta_estimada = 0.25 - alpha_slider  # solo para fines didácticos
        if beta_estimada < 0:
            beta_estimada = 0.01

        st.write(f"**Error Tipo I (α):** {alpha_slider:.2f}")
        st.write(f"**Error Tipo II (β):** {beta_estimada:.2f} (aprox.)")

        # Visualización simple
        fig, ax = plt.subplots(figsize=(5,3))
        ax.bar(["Error Tipo I (α)", "Error Tipo II (β)"], [alpha_slider, beta_estimada], color=["red", "orange"])
        ax.set_ylim(0, 0.3)
        ax.set_title("Relación conceptual entre α y β")
        st.pyplot(fig)

        st.info("""
        🔍 **Interpretación:**  
        - Si reduces **α**, cometes menos **Error Tipo I**, pero es más probable cometer **Error Tipo II** (β).  
        - Si aumentas **α**, al revés: más riesgo de **Error Tipo I**, pero menos **Error Tipo II**.  
        Lo ideal es equilibrar α y β aumentando el tamaño de la muestra para reducir ambos.
        """)


    elif opcion == "Pruebas de una y dos colas":

        st.markdown("## 📝 Pasos para realizar una prueba de hipótesis")

        st.markdown("""
        1. **Formular las hipótesis**  
        - Hipótesis nula (H₀): afirmación que se quiere evaluar (ej. la media es igual a cierto valor).  
        - Hipótesis alternativa (H₁): afirmación contraria o diferente.

        2. **Calcular el estadístico de prueba**  
        - Valor numérico que resume la información de la muestra respecto a H₀.  
        - Ejemplos:  
            - Z = (X̄ - μ₀) / (σ / √n) (si σ conocida)  
            - t = (X̄ - μ₀) / (s / √n) (si σ desconocida)

        3. **Determinar el valor crítico**  
        - Depende del nivel de significancia (α) y tipo de prueba (una cola o dos colas).  
        - Se obtiene de tablas de distribución Z o t.

        4. **Comparar el estadístico con el valor crítico**  
        - Si está en la región de rechazo → **rechazar H₀**  
        - Si está en la región de aceptación → **no rechazar H₀**

        5. **Conclusión**  
        - Decidir si hay evidencia suficiente para rechazar H₀ o no.  
        - También se puede usar el p-valor para la decisión comparándolo con α.
        """)

        st.header("Pruebas de una y dos colas")
        st.write("""
        - **Prueba de dos colas:** H₁: μ ≠ μ₀ → Rechazamos H₀ si el estadístico cae en cualquiera de las dos colas.
        - **Prueba de cola derecha:** H₁: μ > μ₀ → Región crítica solo en la derecha.
        - **Prueba de cola izquierda:** H₁: μ < μ₀ → Región crítica solo en la izquierda.
        """)

        # Visualización de regiones de rechazo para dos colas
        x = np.linspace(-4,4,500)
        y = norm.pdf(x)
        alpha = 0.05
        z_crit = norm.ppf(1-alpha/2)
        fig, ax = plt.subplots(figsize=(8,3))
        ax.plot(x,y)
        ax.fill_between(x,0,y,where=(x<-z_crit)|(x>z_crit),color='red',alpha=0.3,label='Región de rechazo')
        ax.fill_between(x,0,y,where=(x>=-z_crit)&(x<=z_crit),color='green',alpha=0.3,label='Aceptación H₀')
        ax.legend()
        st.pyplot(fig)

    elif opcion == "Cálculo del estadístico Z o t":
        st.header("Cálculo del estadístico de prueba")
        st.write("""
        Para una media, el estadístico se calcula como:

        - Si σ es conocida:  
        **Z = (X̄ - μ₀) / (σ / √n)**
        - Si σ es desconocida:  
        **t = (X̄ - μ₀) / (s / √n)**

        Donde:
        - X̄ = media muestral
        - μ₀ = media hipotética
        - σ o s = desviación estándar poblacional o muestral
        - n = tamaño de la muestra
        """)

    elif opcion == "Decisión: rechazar o no H₀":
        st.header("Decisión en pruebas de hipótesis")
        st.write("""
        Para tomar la decisión:

        1. **Calcula el estadístico de prueba (Z o t)**.
        2. **Obtén el valor crítico** según α y el tipo de prueba.
        3. **Compara:**
        - Si cae en la **región de rechazo**, se **rechaza H₀**.
        - Si cae en la zona central, **no se rechaza H₀**.
        
        También puedes comparar el **p-valor** con α:
        - Si p < α → Rechazamos H₀
        - Si p ≥ α → No rechazamos H₀
        """)

    elif opcion == "Ejemplo interactivo":
        st.header("Ejemplo interactivo")

        mu0 = st.number_input("Media hipotética μ₀:", value=50.0)
        sigma_known = st.checkbox("¿Conoces la desviación estándar poblacional? (usa Z si sí, t si no)", value=True)
        alpha = st.slider("Nivel de significancia (α en %):", 1, 10, 5) / 100
        tipo_prueba = st.selectbox("Tipo de prueba:", ["Dos colas", "Cola derecha", "Cola izquierda"])

        n = st.number_input("Tamaño de la muestra (n):", 1, 1000, 30)
        media_muestral = st.number_input("Media muestral:", value=52.0)
        desv_muestral = st.number_input("Desviación estándar muestral:", value=10.0)

        error_estandar = desv_muestral / np.sqrt(n)
        estadistico = (media_muestral - mu0) / error_estandar

        # Valores críticos
        if tipo_prueba == "Dos colas":
            valor_critico = norm.ppf(1 - alpha/2) if sigma_known else t.ppf(1 - alpha/2, n-1)
            region_rechazo = abs(estadistico) > valor_critico
        elif tipo_prueba == "Cola derecha":
            valor_critico = norm.ppf(1 - alpha) if sigma_known else t.ppf(1 - alpha, n-1)
            region_rechazo = estadistico > valor_critico
        else:
            valor_critico = norm.ppf(alpha) if sigma_known else t.ppf(alpha, n-1)
            region_rechazo = estadistico < valor_critico

        st.write(f"Estadístico calculado: **{estadistico:.3f}**")
        st.write(f"Valor crítico: **{valor_critico:.3f}**")

        if region_rechazo:
            st.error("🚨 Conclusión: Rechazamos H₀. Hay evidencia para aceptar H₁.")
        else:
            st.success("Conclusión: No rechazamos H₀. No hay evidencia suficiente contra ella.")

        # Visualización
        x = np.linspace(-4,4,500)
        y = norm.pdf(x) if sigma_known else t.pdf(x, n-1)

        fig, ax = plt.subplots(figsize=(8,4))
        ax.plot(x,y,label="Distribución bajo H₀")
        ax.axvline(estadistico, color='green', linestyle='--', label='Estadístico muestral')

        if tipo_prueba == "Dos colas":
            ax.axvline(valor_critico, color='red', linestyle='--', label='Valor crítico')
            ax.axvline(-valor_critico, color='red', linestyle='--')
            ax.fill_between(x,0,y,where=(x>valor_critico)|(x<-valor_critico),color='red',alpha=0.3)
        else:
            ax.axvline(valor_critico, color='red', linestyle='--', label='Valor crítico')
            if tipo_prueba == "Cola derecha":
                ax.fill_between(x,0,y,where=(x>valor_critico),color='red',alpha=0.3)
            else:
                ax.fill_between(x,0,y,where=(x<valor_critico),color='red',alpha=0.3)

        ax.legend()
        ax.set_title("Prueba de hipótesis: región de rechazo vs aceptación")
        st.pyplot(fig)
