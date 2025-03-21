# -*- coding: utf-8 -*-
"""
Análisis de Competitividad en Dominios SICOP (Solo 4 Dígitos)
Compara la competitividad antes y después del 1 de diciembre de 2022
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mtick
import sys

# Cargar datos
def cargar_datos(ruta_archivo='lineascontratadas.csv'):
    try:
        df = pd.read_csv(ruta_archivo)
        print(f"Archivo {ruta_archivo} cargado correctamente")
        print(df.head()) # Mostrar las primeras filas del dataframe
        return df
    except FileNotFoundError:
        print(f"Error: {ruta_archivo} no encontrado. Asegúrese de que el archivo existe en el directorio actual o proporcione la ruta correcta.")
        return None
    except pd.errors.ParserError:
        print(f"Error: No se pudo analizar {ruta_archivo}. Verifique el formato del archivo.")
        return None

# Aquí puedes cambiar la ruta del archivo si es necesario
ruta_archivo = 'C:/Users/alejandro.herrera.CGR/Documents/GitHub/umbrales/lineascontratadas.csv'  # Modifica esta ruta
df = cargar_datos(ruta_archivo)

# Si no se pudo cargar el archivo, terminar la ejecución
if df is None:
    print("No se pudo cargar el archivo. El programa se detendrá.")
    sys.exit(1)

try:
    # Convertir 'FECHA_REGISTRO' a objetos datetime si aún no lo es
    df['FECHA_REGISTRO'] = pd.to_datetime(df['FECHA_REGISTRO'], errors='coerce')

    # Filtrar el DataFrame por la fecha de corte (1 de diciembre de 2022)
    df_before_dec = df[df['FECHA_REGISTRO'] < '2022-12-01']
    df_after_dec = df[df['FECHA_REGISTRO'] >= '2022-12-01']

    # Mostrar información sobre los períodos
    print(f"Registros antes del 1 de diciembre de 2022: {len(df_before_dec)}")
    print(f"Registros a partir del 1 de diciembre de 2022: {len(df_after_dec)}")

except KeyError:
    print("Error: Columna 'FECHA_REGISTRO' no encontrada en el DataFrame.")
    sys.exit(1)
except Exception as e:
    print(f"Ocurrió un error: {e}")
    sys.exit(1)

def analizar_coincidencias(df, digitos=4):
    """
    Agrupa el dataset por CEDULA_PROVEEDOR y cuenta cuántas veces aparece cada código de producto
    basado en la cantidad de dígitos indicada.
    """
    df = df.copy()
    df["CODIGO_PRODUCTO_TRUNC"] = df["CODIGO_PRODUCTO"].astype(str).str[:digitos]

    # Contar ocurrencias por proveedor y código de producto truncado
    grouped = df.groupby(["CEDULA_PROVEEDOR", "CODIGO_PRODUCTO_TRUNC"]).size().reset_index(name="CONTEO")

    # Calcular el porcentaje sobre el total de apariciones del código truncado
    total_counts = grouped.groupby("CODIGO_PRODUCTO_TRUNC")["CONTEO"].transform("sum")
    grouped["PORCENTAJE"] = (grouped["CONTEO"] / total_counts) * 100
    # Redondear para trabajar sin decimales
    grouped["PORCENTAJE"] = grouped["PORCENTAJE"].round(0).astype(int)

    return grouped

# Generar resultados solo para 4 dígitos
resultado_antesley_4 = analizar_coincidencias(df_before_dec)
resultado_despuesley_4 = analizar_coincidencias(df_after_dec)

def calcular_hhi(df):
    """
    Calcula el Índice de Herfindahl-Hirschman (HHI) para cada dominio SICOP
    identificado por CODIGO_PRODUCTO_TRUNC, trabajando con enteros.
    """
    # Resultados finales
    resultados = []
    
    # Procesar cada dominio SICOP (CODIGO_PRODUCTO_TRUNC) por separado
    for codigo, grupo in df.groupby("CODIGO_PRODUCTO_TRUNC"):
        # Calcular la suma total del CONTEO para este dominio
        total_dominio = grupo["CONTEO"].sum()
        
        # Calcular el HHI como la suma de los cuadrados de las participaciones
        hhi = 0
        for _, fila in grupo.iterrows():
            # Calcular participación como un entero (multiplicando por 100 para trabajar como porcentaje entero)
            participacion_entero = round((fila["CONTEO"] / total_dominio) * 100)
            # Sumar al HHI el cuadrado de la participación
            hhi += participacion_entero * participacion_entero
        
        # Añadir al resultado
        resultados.append({"CODIGO_PRODUCTO_TRUNC": codigo, "HHI": hhi})
    
    # Convertir a DataFrame
    return pd.DataFrame(resultados)

# Calcular HHI para ambos períodos
hhi_antesley_4 = calcular_hhi(resultado_antesley_4)
hhi_despuesley_4 = calcular_hhi(resultado_despuesley_4)

def comparar_hhi(hhi_df, hhi2_df):
    """
    Compara los valores de HHI para los mismos CODIGO_PRODUCTO_TRUNC y calcula la diferencia.
    """
    merged_df = pd.merge(hhi_df, hhi2_df, on="CODIGO_PRODUCTO_TRUNC", suffixes=("_ANTES", "_DESPUES"))

    if merged_df.empty:
        return pd.DataFrame(columns=['CODIGO_PRODUCTO_TRUNC', 'CAMBIO_HHI'])

    # Un valor negativo en CAMBIO_HHI significa que la concentración del mercado
    # ha disminuido, por lo tanto la competitividad ha aumentado
    merged_df["CAMBIO_HHI"] = merged_df["HHI_ANTES"] - merged_df["HHI_DESPUES"]
    result_df = merged_df[["CODIGO_PRODUCTO_TRUNC", "HHI_ANTES", "HHI_DESPUES", "CAMBIO_HHI"]]
    return result_df

# Comparar HHI entre ambos períodos (4 dígitos)
cambio_hhi_4_df = comparar_hhi(hhi_antesley_4, hhi_despuesley_4)
print("\nDominios con mayores aumentos en competitividad (4 dígitos):")
print(cambio_hhi_4_df.sort_values('CAMBIO_HHI').head(10))  # Los valores más negativos primero
cambio_hhi_4_df.to_csv("cambio_hhi_dominios_4digitos.csv", index=False)

# Calcular totales
total_dominios_4d = len(cambio_hhi_4_df)
dominios_mas_competitivos_4d = sum(cambio_hhi_4_df['CAMBIO_HHI'] < 0)
porcentaje_mejora_4d = (dominios_mas_competitivos_4d / total_dominios_4d) * 100

print(f"\nResumen de cambios en competitividad después del 1 de diciembre de 2022:")
print(f"* Dominios de 4 dígitos: {dominios_mas_competitivos_4d} de {total_dominios_4d} ({porcentaje_mejora_4d:.1f}%) aumentaron su competitividad")

def generar_graficos_competitividad_4digitos(cambio_hhi_4d):
    """
    Genera gráficos de barras que muestran los cambios en la competitividad de los dominios SICOP de 4 dígitos.
    """
    plt.style.use('ggplot')
    
    # Preparar los datos
    cambio_hhi_4d['CAMBIO_ABS'] = cambio_hhi_4d['CAMBIO_HHI'].abs()
    
    # Crear figura con 2 gráficos
    plt.figure(figsize=(16, 14))
    
    # 1. Gráfico para los dominios con cambios más significativos (Top 40)
    ax1 = plt.subplot(2, 1, 1)
    
    # Obtener los 40 dominios con cambios más grandes (en valor absoluto)
    top40_4d = cambio_hhi_4d.nlargest(40, 'CAMBIO_ABS').sort_values('CAMBIO_HHI')
    
    bars1 = ax1.bar(top40_4d['CODIGO_PRODUCTO_TRUNC'], 
                   top40_4d['CAMBIO_HHI'], 
                   color=np.where(top40_4d['CAMBIO_HHI'] < 0, 'green', 'red'))
    
    ax1.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax1.set_title('Top 40 Cambios en Competitividad - Dominios SICOP de 4 Dígitos', fontsize=16)
    ax1.set_xlabel('Código de Dominio SICOP')
    ax1.set_ylabel('Cambio en HHI\n(Negativo = Mayor Competitividad)')
    ax1.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{int(x)}'))
    
    # Añadir etiquetas
    for i, bar in enumerate(bars1):
        ax1.text(
            bar.get_x() + bar.get_width()/2, 
            bar.get_height() + (200 if bar.get_height() > 0 else -200),
            f"{top40_4d.iloc[i]['CODIGO_PRODUCTO_TRUNC']}",
            ha='center', va='bottom' if bar.get_height() > 0 else 'top',
            fontsize=9, rotation=90
        )
    
    plt.xticks([])  # Ocultar etiquetas del eje x por claridad
    
    # 2. Gráfico solo de dominios donde AUMENTÓ la competitividad
    ax2 = plt.subplot(2, 1, 2)
    
    # Filtrar dominios con aumento de competitividad (cambio_hhi < 0)
    # Tomar los 30 con mayor aumento de competitividad
    increased_comp_4d = cambio_hhi_4d[cambio_hhi_4d['CAMBIO_HHI'] < 0].sort_values('CAMBIO_HHI').head(30)
    
    bars2 = ax2.bar(increased_comp_4d['CODIGO_PRODUCTO_TRUNC'], 
                   increased_comp_4d['CAMBIO_HHI'], 
                   color='green')
    
    ax2.set_title('Dominios SICOP con Mayor Aumento de Competitividad (Después del 1 Dic 2022)', fontsize=16)
    ax2.set_xlabel('Código de Dominio SICOP (4 dígitos)')
    ax2.set_ylabel('Cambio en HHI\n(Más negativo = Mayor aumento en competitividad)')
    ax2.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{int(abs(x))}'))
    
    # Añadir etiquetas y valores de mejora
    for i, bar in enumerate(bars2):
        # Calcular porcentaje de mejora
        hhi_antes = increased_comp_4d.iloc[i]['HHI_ANTES']
        hhi_despues = increased_comp_4d.iloc[i]['HHI_DESPUES']
        cambio_hhi = increased_comp_4d.iloc[i]['CAMBIO_HHI']
        porcentaje_mejora = abs(cambio_hhi / hhi_antes * 100) if hhi_antes > 0 else 0
        
        # Añadir etiqueta
        ax2.text(
            bar.get_x() + bar.get_width()/2, 
            bar.get_height() - 200,  # Ajustar posición
            f"{increased_comp_4d.iloc[i]['CODIGO_PRODUCTO_TRUNC']}\n({porcentaje_mejora:.0f}%)",
            ha='center', va='top',
            fontsize=8, rotation=90
        )
    
    plt.xticks([])  # Ocultar etiquetas del eje x por claridad
    
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.25)  # Añadir espacio entre subplots
    
    # Añadir título general
    plt.suptitle('Análisis de Competitividad en Dominios SICOP de 4 Dígitos tras 1 Dic 2022', 
                fontsize=18, y=0.98)
    
    # Guardar la figura
    plt.savefig('analisis_competitividad_sicop_4digitos.png', dpi=300, bbox_inches='tight')
    plt.savefig('analisis_competitividad_sicop_4digitos.pdf', bbox_inches='tight')
    
    print("Gráficos guardados como 'analisis_competitividad_sicop_4digitos.png' y 'analisis_competitividad_sicop_4digitos.pdf'")
    
    plt.show()

# Generar gráficos
print("\nGenerando gráficos de competitividad en dominios SICOP de 4 dígitos...")
generar_graficos_competitividad_4digitos(cambio_hhi_4_df)
print("¡Análisis completado!")