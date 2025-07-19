import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm, t

def run():

    st.title("✅Bloque 3: Intervalos de confianza y comparación de dos muestras")

    opcion = st.sidebar.radio("Elige un tema:", [
        "Intervalo de confianza para una media (recordatorio)",
        "Intervalo de confianza para dos medias",
        "Muestras independientes vs apareadas",
        "Ejemplo interactivo"
    ])

    def plot_ic(mean, se, ci_lower, ci_upper, label="Intervalo de confianza"):
        fig, ax = plt.subplots(figsize=(8, 2))
        ax.errorbar(0, mean, yerr=[[mean - ci_lower], [ci_upper - mean]], fmt='o', capsize=10, label=label)
        ax.set_xlim(-1, 1)
        ax.set_ylim(ci_lower - 1, ci_upper + 1)
        ax.set_xticks([])
        ax.set_title("Intervalo de confianza")
        ax.legend()
        st.pyplot(fig)

    if opcion == "Intervalo de confianza para una media (recordatorio)":
        st.header("Intervalo de confianza para una media (recordatorio)")
        st.write("""
        Un intervalo de confianza (IC) para la media se calcula como:

        $$ IC = \\bar{x} \\pm z_{\\alpha/2} \\times SE $$

        donde:

        - $\\bar{x}$ es la media muestral  
        - $z_{\\alpha/2}$ es el valor crítico de la distribución normal estándar  
        - $SE$ es el error estándar de la media: $SE = \\frac{s}{\\sqrt{n}}$  
        """)
        
        st.write("Este intervalo nos da un rango en el que, con un nivel de confianza $(1-\\alpha)$, esperamos que esté la verdadera media poblacional.")

    elif opcion == "Intervalo de confianza para dos medias":
        st.header("Intervalo de confianza para la diferencia de dos medias")
        st.write("""
        Para comparar dos medias, el intervalo de confianza se calcula como:

        $$ IC = (\\bar{x}_1 - \\bar{x}_2) \\pm t_{\\alpha/2, df} \\times SE $$

        donde:

        - $\\bar{x}_1$ y $\\bar{x}_2$ son las medias muestrales de los grupos 1 y 2  
        - $t_{\\alpha/2, df}$ es el valor crítico de la distribución t con grados de libertad $df$  
        - $SE$ es el error estándar de la diferencia de medias  
        """)
        
        st.write("""
        El error estándar depende si las muestras son independientes o apareadas y si se asume varianzas iguales o no.
        """)

    elif opcion == "Muestras independientes vs apareadas":
        st.header("Muestras independientes vs apareadas")
        st.write("""
        - **Muestras independientes:** las observaciones en un grupo no están relacionadas con las del otro.  
        Ejemplo: medir la presión arterial en dos grupos distintos.
        
        - **Muestras apareadas (dependientes):** las observaciones están emparejadas o relacionadas.  
        Ejemplo: medir antes y después en el mismo grupo de personas.
        """)
        
        st.subheader("📐 ¿Cómo se calcula el estadístico t?")
        st.write("""
        ✅ **Para muestras independientes:**  
        \n
        \\( t = \\frac{\\bar{X}_1 - \\bar{X}_2}{\\sqrt{\\frac{s_1^2}{n_1} + \\frac{s_2^2}{n_2}}} \\)
        
        Donde:
        - \\( \\bar{X}_1, \\bar{X}_2 \\) son las medias de cada grupo  
        - \\( s_1, s_2 \\) son las desviaciones estándar  
        - \\( n_1, n_2 \\) son los tamaños de muestra

        ✅ **Para muestras apareadas:**  
        \n
        \\( t = \\frac{\\bar{D}}{s_D / \\sqrt{n}} \\)

        Donde:
        - \\( D \\) son las diferencias entre cada par  
        - \\( \\bar{D} \\) es la media de las diferencias  
        - \\( s_D \\) es la desviación estándar de las diferencias  
        - \\( n \\) es el número de pares
        """)

        st.subheader("🔢 Ejemplo interactivo")
        tipo = st.radio("Selecciona el tipo de prueba:", ["Independientes", "Apareadas"])

        if tipo == "Independientes":
            st.write("Introduce datos para dos grupos:")
            media1 = st.number_input("Media grupo 1", value=50.0)
            media2 = st.number_input("Media grupo 2", value=55.0)
            sd1 = st.number_input("Desviación estándar grupo 1", value=10.0)
            sd2 = st.number_input("Desviación estándar grupo 2", value=12.0)
            n1 = st.number_input("Tamaño muestra grupo 1", value=30)
            n2 = st.number_input("Tamaño muestra grupo 2", value=30)

            # cálculo t para muestras independientes
            t_value = (media1 - media2) / ((sd1**2/n1 + sd2**2/n2)**0.5)
            st.write(f"**t calculado = {t_value:.3f}**")

        else:
            st.write("Introduce datos de las diferencias:")
            media_d = st.number_input("Media de las diferencias", value=-5.0)
            sd_d = st.number_input("Desviación estándar de las diferencias", value=8.0)
            n = st.number_input("Número de pares", value=30)

            # cálculo t para muestras apareadas
            t_value = media_d / (sd_d / (n**0.5))
            st.write(f"**t calculado = {t_value:.3f}**")

        st.info("📊 Recuerda que después se compara este t calculado con el valor crítico de la t-Student según α y los grados de libertad para decidir si se rechaza H₀.")


    elif opcion == "Ejemplo interactivo":
        st.header("✅ Ejemplo interactivo: Comparar dos muestras")

        tipo_muestra = st.selectbox("Tipo de muestras:", ["Independientes", "Apareadas"])

        n1 = st.number_input("Tamaño muestra 1 (n1):", min_value=2, value=30)
        n2 = n1 if tipo_muestra == "Apareadas" else st.number_input("Tamaño muestra 2 (n2):", min_value=2, value=30)
        
        mean1 = st.number_input("Media muestra 1 (X̄₁):", value=50.0)
        mean2 = st.number_input("Media muestra 2 (X̄₂):", value=52.0)
        
        std1 = st.number_input("Desviación estándar muestra 1 (s₁):", min_value=0.01, value=10.0)
        std2 = std1 if tipo_muestra == "Apareadas" else st.number_input("Desviación estándar muestra 2 (s₂):", min_value=0.01, value=10.0)
        
        alpha = st.slider("Nivel de significancia (α):", 1, 10, 5) / 100

        # Cálculos
        if tipo_muestra == "Independientes":
            se_diff = np.sqrt((std1**2)/n1 + (std2**2)/n2)
            df_num = ((std1**2)/n1 + (std2**2)/n2)**2
            df_den = (( (std1**2)/n1 )**2)/(n1-1) + (( (std2**2)/n2 )**2)/(n2-1)
            df = int(df_num / df_den)
            t_crit = stats.t.ppf(1 - alpha/2, df)
            diff_means = mean1 - mean2
        else:
            se_diff = std1 / np.sqrt(n1)
            df = n1 - 1
            t_crit = stats.t.ppf(1 - alpha/2, df)
            diff_means = mean1 - mean2  # diferencia muestral de pares
        
        ci_lower = diff_means - t_crit * se_diff
        ci_upper = diff_means + t_crit * se_diff

        st.write(f"Diferencia de medias: {diff_means:.3f}")
        st.write(f"Intervalo de confianza al {100*(1-alpha):.1f}%: [{ci_lower:.3f}, {ci_upper:.3f}]")

        # Interpretación
        if ci_lower > 0 or ci_upper < 0:
            st.success("✅ El intervalo no incluye 0, hay diferencia significativa entre las muestras.")
        else:
            st.warning("⚠️ El intervalo incluye 0, no hay diferencia significativa entre las muestras.")

        # Gráfico del intervalo
        plot_ic(diff_means, se_diff, ci_lower, ci_upper, label="Diferencia de medias")

