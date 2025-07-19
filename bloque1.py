import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm, t

def run():
 
    st.title("✅Bloque 1: Conceptos Básicos de Estadística Inferencial")

    # Menú interno para este bloque
    opcion = st.sidebar.radio("Elige un tema:", [
        "Nivel de confianza",
        "Error estándar",
        "Distribuciones Z vs t",
        "Ejemplo interactivo"
    ])

    if opcion == "Nivel de confianza":
        st.header("Nivel de confianza")
        st.write("""
        El **nivel de confianza** es la probabilidad de que un intervalo contenga el verdadero valor del parámetro poblacional.

        Siempre está relacionado con el **nivel de significancia (α)**, que representa la probabilidad de cometer un **error tipo I** (rechazar la hipótesis nula siendo verdadera).

        **Nivel de confianza + Nivel de significancia = 1**

        Ejemplos:
        - Confianza **95%** → α = 0.05 (5% de probabilidad de error)
        - Confianza **99%** → α = 0.01 (1% de probabilidad de error)
        """)

        confianza = st.slider("Selecciona el nivel de confianza:", 80, 99, 95)
        alpha = 1 - confianza/100

        st.info(f"Para un nivel de confianza del {confianza}%, el nivel de significancia α = {alpha:.3f}")

        st.write("""
        **Interpretación:** Si repites el muestreo muchas veces y construyes intervalos de confianza,
        aproximadamente el **{confianza}%** de ellos contendrán el valor verdadero, y en el **{alpha*100:.1f}%** de los casos
        te equivocarás (error tipo I).
        """)

        # Pequeña visualización
        fig, ax = plt.subplots(figsize=(6,3))
        x = np.linspace(-4,4,500)
        y = norm.pdf(x)
        ax.plot(x,y,color='blue')
        z_crit = norm.ppf(1-alpha/2)
        ax.fill_between(x,0,y,where=(x<-z_crit),color='red',alpha=0.3,label='Región de error (α/2)')
        ax.fill_between(x,0,y,where=(x>z_crit),color='red',alpha=0.3)
        ax.fill_between(x,0,y,where=(x>=-z_crit)&(x<=z_crit),color='green',alpha=0.3,label='Zona de confianza')
        ax.axvline(-z_crit,color='black',linestyle='--')
        ax.axvline(z_crit,color='black',linestyle='--')
        ax.set_title(f"Zona de confianza ({confianza}%) vs Región de error ({alpha*100:.1f}%)")
        ax.legend()
        st.pyplot(fig)

    elif opcion == "Error estándar":
        st.header("Error estándar")
        st.write("""
        El **error estándar (EE)** mide la variabilidad o precisión de una estadística muestral, como la media.

        - Cuando tomamos muestras diferentes, la media muestral cambia. El EE cuantifica cuánto varían estas medias alrededor de la verdadera media poblacional.
        - Cuanto más pequeño es el EE, más confiable es la estimación.

        **¿Para qué sirve?**
        1. Construir intervalos de confianza:  
        $$\\text{Intervalo} = \\text{media muestral} \\pm (\\text{valor crítico}) \\times EE$$  
        Esto nos indica un rango probable donde está la media poblacional.
        2. Realizar pruebas de hipótesis:  
        Se usa para calcular el estadístico Z o t, por ejemplo:  
        $$Z = \\frac{\\text{media muestral} - \\text{media hipotética}}{EE}$$
        3. Comparar precisión entre estudios o muestras.

        """)

        sigma = st.number_input("Introduce la desviación estándar poblacional (σ):", 0.1, 100.0, 10.0)
        n = st.number_input("Introduce el tamaño de la muestra (n):", 1, 10000, 30)

        ee = sigma / np.sqrt(n)
        st.success(f"El error estándar es: {ee:.3f}")

        # Visualización dinámica del EE según n
        n_vals = np.arange(1, 201)
        ee_vals = sigma / np.sqrt(n_vals)

        fig, ax = plt.subplots(figsize=(8,4))
        ax.plot(n_vals, ee_vals, label="Error estándar (EE)")
        ax.axvline(n, color='red', linestyle='--', label=f'Tamaño muestra actual = {n}')
        ax.set_xlabel("Tamaño de la muestra (n)")
        ax.set_ylabel("Error estándar (EE)")
        ax.set_title("Cómo disminuye el Error Estándar al aumentar el tamaño de muestra")
        ax.legend()
        st.pyplot(fig)


    elif opcion == "Distribuciones Z vs t":
        st.header("Distribuciones Z y t de Student")
        st.write("""
        - La **distribución Z (normal estándar)** se usa cuando conocemos la desviación estándar poblacional o el tamaño de muestra es grande.
        - La **distribución t de Student** se usa cuando la desviación estándar poblacional es desconocida y la muestra es pequeña.
        
        **Grados de libertad (df):**  
        Es el número de valores independientes que pueden variar en un cálculo estadístico.  
        Para la t-Student, generalmente es \( df = n - 1 \) (donde \( n \) es el tamaño de la muestra).
        
        **Tablas Z y t:**  
        Se usan para encontrar valores críticos (puntos de corte) que nos permiten construir intervalos de confianza y realizar pruebas de hipótesis.  
        Estos valores críticos dependen del nivel de significancia (α) y, en el caso de la t, también de los grados de libertad.
        """)

        st.write("""
        ### Resumen sobre las regiones bajo la curva y las hipótesis

        - El área **central** bajo la curva (entre los valores críticos) representa la **aceptación de la hipótesis nula (H₀)**.
        - Las áreas en las **colas** (más allá de los valores críticos) representan la **región de rechazo de H₀**, es decir, donde se acepta la hipótesis alternativa (H₁).
        - El nivel de significancia (α) es la probabilidad de rechazar H₀ cuando es verdadera (error tipo I).
        - En pruebas de dos colas, α se divide entre ambas colas, ubicando valores críticos simétricos a la izquierda y derecha.
        - En pruebas de una cola, todo α se concentra en una sola cola (izquierda o derecha).

        Esta interpretación es clave para entender cómo funcionan las pruebas estadísticas y la toma de decisiones basadas en los datos.
        """)

        alpha = st.slider("Selecciona el nivel de significancia (α):", 1, 10, 5) / 100
        df = st.slider("Grados de libertad (df) para la t-Student:", 1, 100, 10)

        # Valores críticos (percentiles)
        z_crit = norm.ppf(1 - alpha/2)
        t_crit = t.ppf(1 - alpha/2, df)

        st.write(f"Valor crítico Z para α = {alpha:.3f}: **{z_crit:.3f}**")
        st.write(f"Valor crítico t para α = {alpha:.3f} y df = {df}: **{t_crit:.3f}**")

        x = np.linspace(-4, 4, 500)
        z_pdf = norm.pdf(x)
        t_pdf = t.pdf(x, df)

        fig, ax = plt.subplots(figsize=(8,4))

        # Áreas de rechazo y aceptación para la Z (normal)
        ax.fill_between(x, 0, z_pdf, where=(x < -z_crit) | (x > z_crit), color='red', alpha=0.3, label='Región rechazo H₀')
        ax.fill_between(x, 0, z_pdf, where=(x >= -z_crit) & (x <= z_crit), color='green', alpha=0.3, label='Región aceptación H₀')

        sns.lineplot(x=x, y=z_pdf, label="Z (Normal estándar)", color="blue", ax=ax)
        sns.lineplot(x=x, y=t_pdf, label=f"t-Student (df={df})", color="red", ax=ax)
        ax.axvline(z_crit, color='blue', linestyle='--', label=f'Z crítico = {z_crit:.2f}')
        ax.axvline(-z_crit, color='blue', linestyle='--')
        ax.axvline(t_crit, color='red', linestyle='--', label=f't crítico = {t_crit:.2f}')
        ax.axvline(-t_crit, color='red', linestyle='--')
        ax.set_title("Comparación: Distribución Z vs t-Student con valores críticos")
        ax.legend()
        st.pyplot(fig)


    elif opcion == "Ejemplo interactivo":
        st.header("Ejemplo interactivo")
        st.write("Simularemos intervalos de confianza para una media poblacional.")

        mu = 50
        sigma = 10
        n = st.slider("Tamaño de la muestra:", 5, 100, 30)
        confianza = st.slider("Nivel de confianza (%):", 80, 99, 95)
        alpha = 1 - confianza/100

        # Generamos una muestra aleatoria
        muestra = np.random.normal(mu, sigma, n)
        media_muestral = np.mean(muestra)
        ee = sigma/np.sqrt(n)

        # Z crítico para el nivel de confianza
        z_critico = norm.ppf(1 - alpha/2)
        intervalo = (media_muestral - z_critico*ee, media_muestral + z_critico*ee)

        st.write(f"Media muestral: **{media_muestral:.2f}**")
        st.write(f"Intervalo de confianza del {confianza}%: **({intervalo[0]:.2f}, {intervalo[1]:.2f})**")

        fig, ax = plt.subplots(figsize=(6,3))
        ax.axvline(mu, color='green', linestyle='--', label='Media real')
        ax.axvline(intervalo[0], color='red', linestyle='--', label='Límite inferior')
        ax.axvline(intervalo[1], color='red', linestyle='--', label='Límite superior')
        ax.hist(muestra, bins=10, alpha=0.5, color='blue')
        ax.legend()
        st.pyplot(fig)

