from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
from IPython.display import display, HTML
from ipywidgets import interact, widgets
from tabulate import tabulate

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analizar', methods=['POST'])
def analizar():
    if request.method == 'POST':
        datos = request.form['datos']
        lista_numeros = convertir_a_lista(datos)
        tipo_variable = request.form['tipo-variable']

        if tipo_variable == "Cualitativa":
            cualidades = obtener_datos_unicos(lista_numeros)
            frec_absoluta = FrecuenciaAbsoluta(cualidades, lista_numeros)
            frecuencia_relativa = [round(c / sum(frec_absoluta), 4) for c in frec_absoluta]
            frecuencia_relativa_porcentual = [round(c * 100, 2) for c in frecuencia_relativa]

            df = pd.DataFrame({
                'Cualidades': cualidades,
                'Frec. absoluta': frec_absoluta,
                'Frec. relativa': frecuencia_relativa,
                'Frec. relativa porcentual': frecuencia_relativa_porcentual,
            })

            tabla_html = df.to_html(index=False)
            grafico_circular = generar_grafico_circular(cualidades, frecuencia_relativa_porcentual)
            grafico_barras = generar_grafico_barras_cualitativa(df)

            return render_template('index.html', tabla_html=tabla_html, grafico_circular=grafico_circular, grafico_barras=grafico_barras)

        elif tipo_variable == "Cuantitativa discreta":
            cualidades = obtener_datos_unicos(lista_numeros)
            frec_absoluta = FrecuenciaAbsoluta(cualidades, lista_numeros)
            frecuencia_relativa = [round(c / sum(frec_absoluta), 4) for c in frec_absoluta]
            frecuencia_relativa_porcentual = [round(c * 100, 2) for c in frecuencia_relativa]
            frecuencia_acumulada_menor = [sum(frec_absoluta[:i + 1]) for i in range(len(frec_absoluta))]
            frecuencia_acumulada_mayor = [sum(frec_absoluta[i:]) for i in range(len(frec_absoluta))]
            frecuencia_relativa_acumulada_menor = [round(sum(frecuencia_relativa[:i + 1]), 4) for i in
                                                   range(len(frecuencia_relativa))]
            frecuencia_relativa_acumulada_mayor = [round(sum(frecuencia_relativa[i:]), 4) for i in
                                                   range(len(frecuencia_relativa))]

            df = pd.DataFrame({
                'Cualidades': cualidades,
                'Frec. absoluta': frec_absoluta,
                'Frec. absoluta acumulada menor que': frecuencia_acumulada_menor,
                'Frec. absoluta acumulada mayor que': frecuencia_acumulada_mayor,
                'Frec. relativa': frecuencia_relativa,
                'Frec. relativa porcentual': frecuencia_relativa_porcentual,
                'Frec. relativa acumulada menor que': frecuencia_relativa_acumulada_menor,
                'Frec. relativa acumulada mayor que': frecuencia_relativa_acumulada_mayor,
            })

            tabla_html = df.to_html(index=False)
            grafico_circular = generar_grafico_circular(cualidades, frecuencia_relativa_porcentual)
            grafico_barras = generar_grafico_barras_cuantitativa_discreta(df)
            medidas_centralidad_dispersion = calcular_medidas_centralidad_dispersion(lista_numeros)

            medidas_html = pd.DataFrame(medidas_centralidad_dispersion.items(), columns=['Medida', 'Valor']).to_html(
                index=False)

            return render_template('index.html', tabla_html=tabla_html, grafico_circular=grafico_circular,
                                   grafico_barras=grafico_barras, medidas_html=medidas_html)

        elif tipo_variable == "Cuantitativa continua":
            def intervalos(c, m, ymin):
                interval_list = []
                ini = ymin
                fin = c + ymin
                for i in range(m):
                    interval_list.append(f"{ini}-{fin}")
                    ini = fin
                    fin += c
                return interval_list

            def MarcaDeClase(intervalos):
                marcas = []
                for intervalo in intervalos:
                    x, y = map(int, intervalo.split('-'))
                    marcas.append((x + y) / 2)
                return marcas

            def frecAbsoluta(intervalos, data):
                resultados = []
                for intervalo in intervalos:
                    ini, fin = map(int, intervalo.split('-'))
                    cantidad_numeros = sum(1 for num in data if ini <= num < fin)
                    resultados.append(cantidad_numeros)
                return resultados

            def porcentualMayorMenor(relativa):
                n = len(relativa)
                mayor = []
                menor = []
                for i in range(n):
                    mayor.append(relativa[i])
                    menor.append(relativa[-1 * (i + 1)])
                return mayor, menor

            m = round(math.sqrt(len(lista_numeros)))
            c = round((max(lista_numeros) - min(lista_numeros)) / m)
            ymin = min(lista_numeros)
            intervalos_list = intervalos(c, m, ymin)
            marcaClase = MarcaDeClase(intervalos_list)
            frec_absoluta = frecAbsoluta(intervalos_list, lista_numeros)
            frecuencia_acumulada_menor = [sum(frec_absoluta[:i + 1]) for i in range(len(frec_absoluta))]
            frecuencia_acumulada_mayor = [sum(frec_absoluta[i:]) for i in range(len(frec_absoluta))]
            frecuencia_relativa = [round(c / sum(frec_absoluta), 4) for c in frec_absoluta]
            frecuencia_relativa_acumulada_menor = [round(sum(frecuencia_relativa[:i + 1]), 4) for i in
                                                   range(len(frecuencia_relativa))]
            frecuencia_relativa_acumulada_mayor = [round(sum(frecuencia_relativa[i:]), 4) for i in
                                                   range(len(frecuencia_relativa))]
            frecuencia_relativa_porcentual = [round(c * 100, 2) for c in frecuencia_relativa]
            frecuencia_relativa_porcentual_mayor, frecuencia_relativa_porcentual_menor = porcentualMayorMenor(
                frecuencia_relativa_porcentual)

            medidas_centralidad_dispersion = calcular_medidas_centralidad_dispersion(lista_numeros)

            df = pd.DataFrame({
                'Intervalos': intervalos_list,
                'Frec. absoluta': frec_absoluta,
                'Marca de clase': marcaClase,
                'Frec. absoluta acumulada menor que': frecuencia_acumulada_menor,
                'Frec. absoluta acumulada mayor que': frecuencia_acumulada_mayor,
                'Frec. relativa': frecuencia_relativa,
                'Frec. relativa acumulada menor que': frecuencia_relativa_acumulada_menor,
                'Frec. relativa acumulada mayor que': frecuencia_relativa_acumulada_mayor,
                'Frec. relativa porcentual': frecuencia_relativa_porcentual,
                'Frec. relativa porcentual acumulada menor que': frecuencia_relativa_porcentual_menor,
                'Frec. relativa porcentual acumulada mayor que': frecuencia_relativa_porcentual_mayor,
            })

            tabla_html = df.to_html(index=False)
            grafico_circular = generar_grafico_circular(intervalos_list, frecuencia_relativa_porcentual)
            grafico_barras = generar_grafico_barras_cuantitativa_continua(df)
            medidas_html = pd.DataFrame(medidas_centralidad_dispersion.items(), columns=['Medida', 'Valor']).to_html(
                index=False)

            return render_template('index.html', tabla_html=tabla_html, grafico_circular=grafico_circular,
                                   grafico_barras=grafico_barras, medidas_html=medidas_html)

def convertir_a_lista(datos):
    # Eliminamos espacios en blanco extra al inicio y final del string
    datos = datos.strip()

    # Dividimos los datos por espacios para obtener una lista
    lista_datos = datos.split()

    # Convertimos los elementos de la lista a enteros si es posible
    lista_datos = [int(d) if d.isdigit() else d for d in lista_datos]

    return lista_datos

def obtener_datos_unicos(lista):
    datos_unicos = list(set(lista))
    datos_unicos.sort()
    return datos_unicos

def FrecuenciaAbsoluta(lista, data):
    frec = []
    for i in lista:
        var = 0
        for j in data:
            if j == i:
                var += 1
        frec.append(var)
    return frec

def calcular_medidas_centralidad_dispersion(data):
    media_aritmetica = sum(data) / len(data)
    moda = max(set(data), key=data.count)
    mediana = sorted(data)[len(data) // 2] if len(data) % 2 != 0 else sum(
        sorted(data)[len(data) // 2 - 1:len(data) // 2 + 1]) / 2
    varianza = sum((x - media_aritmetica) ** 2 for x in data) / len(data)
    desviacion_estandar = math.sqrt(varianza)
    coef_asimetria_1 = (media_aritmetica - moda) / desviacion_estandar
    coef_asimetria_2 = (3 * (media_aritmetica - mediana)) / desviacion_estandar
    m3 = sum((x - media_aritmetica) ** 3 for x in data) / len(data)
    m2 = varianza
    coef_asimetria_3 = m3 / (m2 ** (3 / 2))

    return {
        "media_aritmetica": media_aritmetica,
        "moda": moda,
        "mediana": mediana,
        "varianza": varianza,
        "desviacion_estandar": desviacion_estandar,
        "coef_asimetria_1": coef_asimetria_1,
        "coef_asimetria_2": coef_asimetria_2,
        "coef_asimetria_3": coef_asimetria_3
    }

def generar_grafico_circular(cualidades, frecuencia_relativa_porcentual):
    plt.figure(figsize=(10, 5))
    plt.pie(frecuencia_relativa_porcentual, labels=cualidades, autopct='%1.1f%%', startangle=140,
            colors=sns.color_palette('viridis', len(cualidades)))
    plt.title('Diagrama Circular - Distribución de Frecuencia Relativa')
    plt.axis('equal')
    plt.tight_layout()
    graph = get_image()

    return graph

def generar_grafico_barras_cualitativa(df):
    plt.figure(figsize=(10, 5))
    sns.barplot(x='Cualidades', y='Frec. absoluta', data=df, palette='viridis')
    plt.title('Diagrama de Barras - Frec. absoluta')
    plt.xlabel('Cualidades')
    plt.ylabel('Frec. absoluta')
    plt.tight_layout()
    graph = get_image()

    return graph

def generar_grafico_barras_cuantitativa_discreta(df):
    plt.figure(figsize=(10, 5))
    sns.barplot(x='Cualidades', y='Frec. absoluta', data=df, palette='viridis')
    plt.title('Diagrama de Barras - Frec. absoluta')
    plt.xlabel('Cualidades')
    plt.ylabel('Frec. absoluta')
    plt.tight_layout()
    graph = get_image()

    return graph

def generar_grafico_barras_cuantitativa_continua(df):
    plt.figure(figsize=(10, 5))
    sns.barplot(x='Intervalos', y='Frec. absoluta', data=df, palette='viridis')
    plt.title('Diagrama de Barras - Frec. absoluta')
    plt.xlabel('Intervalos')
    plt.ylabel('Frec. absoluta')
    plt.tight_layout()
    graph = get_image()

    return graph

def get_image():
    import io
    import base64
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.clf()
    return f'data:image/png;base64,{graph_url}'

if __name__ == '__main__':
    app.run(debug=True)

