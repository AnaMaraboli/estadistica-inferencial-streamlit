import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm, t , f , chi2_contingency

def run():

    st.title("✅ Bloque 4: Estadística Inferencial Avanzada")

    # Menú lateral para elegir tema
    opcion = st.sidebar.radio("Elige un tema", 
        [
            "Intervalos de confianza para medias y proporciones",
            "Pruebas para proporciones",
            "Pruebas chi-cuadrado (independencia y bondad de ajuste)",
            "Introducción a ANOVA (análisis de varianza)"
        ]
    )

    if opcion == "Intervalos de confianza para medias y proporciones":
        st.subheader("Intervalos de confianza para la media")
        st.write("""
        Un intervalo de confianza (IC) para la media es un rango donde esperamos que esté el valor real de la media poblacional, con un nivel de confianza dado.
        """)

        media_muestral = st.number_input("Media muestral (\\(\\bar{x}\\))", value=50.0)
        desviacion = st.number_input("Desviación estándar (s)", value=10.0)
        tamano_muestra = st.number_input("Tamaño de la muestra (n)", value=30)
        nivel_confianza = st.slider("Nivel de confianza (%)", 80, 99, 95)

        alpha = 1 - nivel_confianza / 100

        if tamano_muestra > 30:
            critico = norm.ppf(1 - alpha / 2)
            distribucion = "Normal (Z)"
        else:
            critico = t.ppf(1 - alpha / 2, df=tamano_muestra - 1)
            distribucion = f"t de Student (df={tamano_muestra - 1})"

        error_estandar = desviacion / np.sqrt(tamano_muestra)
        margen_error = critico * error_estandar

        limite_inferior = media_muestral - margen_error
        limite_superior = media_muestral + margen_error

        st.write(f"Distribución usada: **{distribucion}**")
        st.write(f"Valor crítico: **{critico:.3f}**")
        st.write(f"Error estándar: **{error_estandar:.3f}**")
        st.write(f"Margen de error: **{margen_error:.3f}**")
        st.write(f"Intervalo de confianza: [{limite_inferior:.3f}, {limite_superior:.3f}]")

        x = np.linspace(media_muestral - 4 * error_estandar, media_muestral + 4 * error_estandar, 500)
        if tamano_muestra > 30:
            y = norm.pdf(x, media_muestral, error_estandar)
        else:
            y = t.pdf((x - media_muestral) / error_estandar, df=tamano_muestra - 1) / error_estandar

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(x, y, label='Distribución del estimador')
        ax.fill_between(x, 0, y, where=(x >= limite_inferior) & (x <= limite_superior), color='green', alpha=0.3, label='Intervalo de confianza')
        ax.axvline(media_muestral, color='red', linestyle='--', label='Media muestral')
        ax.set_title("Intervalo de confianza para la media")
        ax.legend()
        st.pyplot(fig)


    elif opcion == "Pruebas para proporciones":
        st.subheader("Pruebas para proporciones")
        st.write("""
        Las pruebas para proporciones nos permiten evaluar hipótesis sobre la proporción poblacional \\(p\\) basada en una muestra.  

        Por ejemplo:  
        - ¿La proporción de clientes satisfechos es igual a 0.8?  
        - ¿El porcentaje de votos a un candidato es distinto al 50%?

        Usamos el estadístico Z:  
        \\[
        Z = \\frac{\\hat{p} - p_0}{\\sqrt{\\frac{p_0 (1 - p_0)}{n}}}
        \\]  
        Donde:  
        - \\(\\hat{p}\\) es la proporción muestral  
        - \\(p_0\\) es la proporción bajo hipótesis nula  
        - \\(n\\) es el tamaño de la muestra
        """)

        # Inputs
        p0 = st.number_input("Proporción bajo hipótesis nula (p0)", min_value=0.0, max_value=1.0, value=0.5)
        exito = st.number_input("Número de éxitos en la muestra", min_value=0, value=40)
        n = st.number_input("Tamaño de la muestra (n)", min_value=1, value=100)
        alpha = st.slider("Nivel de significancia (α)", min_value=0.01, max_value=0.10, value=0.05)

        # Proporción muestral
        p_hat = exito / n

        # Estadístico Z
        se = np.sqrt(p0 * (1 - p0) / n)
        z_stat = (p_hat - p0) / se

        # Prueba bilateral: p-valor
        from scipy.stats import norm
        p_value = 2 * (1 - norm.cdf(abs(z_stat)))

        st.write(f"Proporción muestral \\(\\hat{{p}}\\): **{p_hat:.3f}**")
        st.write(f"Estadístico Z: **{z_stat:.3f}**")
        st.write(f"p-valor (prueba bilateral): **{p_value:.4f}**")

        if p_value < alpha:
            st.success(f"Se rechaza la hipótesis nula con un nivel de significancia de {alpha}")
        else:
            st.info(f"No se rechaza la hipótesis nula con un nivel de significancia de {alpha}")

        # Gráfica para visualización
        x = np.linspace(-4, 4, 1000)
        y = norm.pdf(x)

        fig, ax = plt.subplots(figsize=(8,4))
        ax.plot(x, y, label="Distribución normal estándar")

        # Región rechazo para prueba bilateral
        crit = norm.ppf(1 - alpha/2)
        ax.fill_between(x, 0, y, where=(x <= -crit) | (x >= crit), color='red', alpha=0.3, label="Región de rechazo")
        ax.axvline(z_stat, color='black', linestyle='--', label="Estadístico Z calculado")
        ax.set_title("Prueba para proporciones: Regiones de rechazo")
        ax.legend()
        st.pyplot(fig)


    elif opcion == "Pruebas chi-cuadrado (independencia y bondad de ajuste)":
        st.subheader("Pruebas Chi-cuadrado")
        st.write("""
        La prueba Chi-cuadrado es una prueba no paramétrica que se usa para evaluar la relación entre variables categóricas.  
        Hay dos tipos principales:  

        1. **Prueba de independencia:**  
        Verifica si dos variables categóricas son independientes o están asociadas.  
        
        2. **Prueba de bondad de ajuste:**  
        Evalúa si una distribución observada se ajusta a una distribución esperada.

        Ambas usan la estadística:
        \\[
        \\chi^2 = \\sum \\frac{(O_i - E_i)^2}{E_i}
        \\]
        donde \\(O_i\\) son los valores observados y \\(E_i\\) los esperados.
        """)

        tipo_prueba = st.radio("Selecciona tipo de prueba Chi-cuadrado:", ["Independencia", "Bondad de ajuste"])

        if tipo_prueba == "Independencia":
            st.write("Introduce la tabla de contingencia:")

            # Ejemplo de tabla 2x2 para simplificar, se puede ampliar
            col1, col2 = st.columns(2)
            with col1:
                st.write("Grupo A")
                a11 = st.number_input("Celda (1,1)", min_value=0, value=30)
                a12 = st.number_input("Celda (1,2)", min_value=0, value=20)
            with col2:
                st.write("Grupo B")
                a21 = st.number_input("Celda (2,1)", min_value=0, value=10)
                a22 = st.number_input("Celda (2,2)", min_value=0, value=40)

            tabla = np.array([[a11, a12],
                            [a21, a22]])

            chi2_stat, p_val, dof, expected = chi2_contingency(tabla)

            st.write(f"Estadístico Chi-cuadrado: **{chi2_stat:.3f}**")
            st.write(f"Grados de libertad: **{dof}**")
            st.write(f"p-valor: **{p_val:.4f}**")

            alpha = st.slider("Nivel de significancia (α)", 0.01, 0.10, 0.05)

            if p_val < alpha:
                st.success("Se rechaza la hipótesis de independencia (hay asociación entre variables).")
            else:
                st.info("No se rechaza la hipótesis de independencia (las variables parecen independientes).")

            st.write("Tabla esperada bajo independencia:")
            st.write(expected)

        else:  # Bondad de ajuste
            st.write("Introduce los valores observados y esperados:")

            obs_str = st.text_area("Valores observados (separados por coma)", "30, 10, 20, 40")
            exp_str = st.text_area("Valores esperados (separados por coma)", "25, 15, 25, 35")

            try:
                observados = np.array([float(x.strip()) for x in obs_str.split(",")])
                esperados = np.array([float(x.strip()) for x in exp_str.split(",")])

                if len(observados) != len(esperados):
                    st.error("Los vectores de observados y esperados deben tener la misma longitud.")
                else:
                    chi2_stat = np.sum((observados - esperados) ** 2 / esperados)
                    dof = len(observados) - 1
                    p_val = 1 - chi2.cdf(chi2_stat, dof)

                    st.write(f"Estadístico Chi-cuadrado: **{chi2_stat:.3f}**")
                    st.write(f"Grados de libertad: **{dof}**")
                    st.write(f"p-valor: **{p_val:.4f}**")

                    alpha = st.slider("Nivel de significancia (α)", 0.01, 0.10, 0.05, key="bondad_alpha")

                    if p_val < alpha:
                        st.success("Se rechaza la hipótesis de bondad de ajuste (no se ajusta bien).")
                    else:
                        st.info("No se rechaza la hipótesis de bondad de ajuste (se ajusta bien).")
            except Exception as e:
                st.error(f"Error al procesar datos: {e}")


    elif opcion == "Introducción a ANOVA (análisis de varianza)":
        st.subheader("Introducción a ANOVA (Análisis de Varianza)")
        st.write("""
        ANOVA es una técnica para comparar las medias de tres o más grupos y determinar si al menos uno es significativamente diferente.  
        Se basa en analizar la variabilidad entre grupos y dentro de los grupos.

        Hipótesis:  
        - \(H_0\): Todas las medias son iguales  
        - \(H_1\): Al menos una media es diferente

        Estadístico F:  
        \[
        F = \frac{Variabilidad\ entre\ grupos}{Variabilidad\ dentro\ de\ grupos}
        \]
        """)

        # Número de grupos
        k = st.number_input("Número de grupos", min_value=2, max_value=10, value=3)

        data = []
        for i in range(1, k+1):
            grupo = st.text_area(f"Datos del grupo {i} (separados por coma)", key=f"grupo_{i}", value="12,15,14,10,13")
            try:
                valores = [float(x.strip()) for x in grupo.split(",") if x.strip() != '']
                data.append(valores)
            except:
                st.error(f"Error al procesar datos del grupo {i}")

        # Solo hacer cálculo si todos los grupos tienen datos
        if all(len(g) > 0 for g in data):
            # Calcular ANOVA one-way manualmente
            N = sum(len(g) for g in data)
            k = len(data)
            # Media global
            all_data = [item for sublist in data for item in sublist]
            media_global = np.mean(all_data)

            # Suma de cuadrados entre grupos
            ss_between = sum(len(g) * (np.mean(g) - media_global) ** 2 for g in data)
            # Suma de cuadrados dentro de grupos
            ss_within = sum(sum((x - np.mean(g)) ** 2 for x in g) for g in data)

            df_between = k - 1
            df_within = N - k

            ms_between = ss_between / df_between
            ms_within = ss_within / df_within

            F = ms_between / ms_within

            # p-valor
            p_val = 1 - f.cdf(F, df_between, df_within)

            st.write(f"Estadístico F: **{F:.3f}**")
            st.write(f"Grados de libertad entre grupos: {df_between}")
            st.write(f"Grados de libertad dentro de grupos: {df_within}")
            st.write(f"p-valor: **{p_val:.4f}**")

            alpha = st.slider("Nivel de significancia (α)", 0.01, 0.10, 0.05, key="anova_alpha")

            if p_val < alpha:
                st.success("Se rechaza la hipótesis nula: al menos un grupo tiene media diferente.")
            else:
                st.info("No se rechaza la hipótesis nula: no hay evidencia suficiente para decir que las medias difieren.")



