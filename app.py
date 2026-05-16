"""
Laboratorio de Comunicacion Basada en Evidencia
Evaluacion 1 - Arquitecto de Decisiones
Autor: Fredy
"""

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Paleta institucional
VERDE = '#2E8B57'
NARANJA = '#D2691E'
GRIS = '#B8B8B8'
GRIS_OSCURO = '#555555'

st.set_page_config(page_title="Evaluacion 1 - Visualizacion",
                   page_icon="", layout="wide")

# ========== CARGA ==========
@st.cache_data
def cargar():
    url = "https://github.com/owid/energy-data/raw/master/owid-energy-data.csv"
    df = pd.read_csv(url)
    df = df[['country', 'year', 'iso_code', 'renewables_share_elec']].copy()
    df = df.dropna(subset=['renewables_share_elec'])
    df = df[df['iso_code'].notna()]  # excluir agregados regionales
    return df

df = cargar()
ultimo = df['year'].max()

# ========== SIDEBAR ==========
st.sidebar.title("Evaluacion 1")
st.sidebar.markdown("**Visualizacion de Datos** - MCD 2026")
st.sidebar.markdown("---")

reto = st.sidebar.radio(
    "Navegacion",
    ["Portada","Reto 1: Jerarquia", "Reto 2: Contraste",
     "Reto 3: Persuasion", "Conclusiones"]
)

st.sidebar.markdown("---")
st.sidebar.caption(f"Dataset: Our World in Data\nUltimo ano: {ultimo}")

# ========== PORTADA ==========
if reto == "Portada":
    st.title("Laboratorio de Comunicacion Basada en Evidencia")
    st.subheader("Evaluacion 1 - Arquitecto de Decisiones")

    st.markdown("""
    ### Pregunta de negocio
    > **Como se posiciona Colombia en la transicion energetica global
    > y que debe hacer en los proximos 5 anos?

    ### Narrativa unica
    Los tres retos comparten dataset (OWID Energy) y construyen una historia:
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**Reto 1 - Jerarquia**\n\nDonde esta Colombia en el ranking mundial?")
    with col2:
        st.warning("**Reto 2 - Contraste**\n\nQue cambio en su trayectoria reciente?")
    with col3:
        st.success("**Reto 3 - Persuasion**\n\nQue debe hacer Colombia?")

    st.markdown("---")
    st.caption(f"Dataset cargado: {df.shape[0]:,} filas - {df['country'].nunique()} paises - {df['year'].min()}-{ultimo}")

# ========== RETO 1 ==========
elif reto == "Reto 1: Jerarquia":
    st.title("Reto 1: Jerarquia")
    st.caption("Eje: Eficiencia (atributos pre-atentivos)")

    # Top 8 + Colombia
    ranking = df[df['year'] == ultimo].sort_values('renewables_share_elec', ascending=False).reset_index(drop=True)
    pos_col = ranking[ranking['country'] == 'Colombia'].index[0] + 1

    top8 = df[df['year'] == ultimo].nlargest(8, 'renewables_share_elec')
    col = df[(df['country'] == 'Colombia') & (df['year'] == ultimo)]
    plot_df = pd.concat([top8, col]).drop_duplicates('country')
    plot_df = plot_df.sort_values('renewables_share_elec', ascending=True)

    # Gráfico
    colores = [VERDE if p == 'Colombia' else GRIS for p in plot_df['country']]

    fig, ax = plt.subplots(figsize=(13, 5.5))
    ax.barh(plot_df['country'], plot_df['renewables_share_elec'], color=colores, height=0.7)

    for s in ['top', 'right', 'bottom', 'left']:
        ax.spines[s].set_visible(False)
    ax.tick_params(left=False, bottom=False, labelsize=13)
    ax.set_xticks([])

    for i, (pais, val) in enumerate(zip(plot_df['country'], plot_df['renewables_share_elec'])):
        color_txt = VERDE if pais == 'Colombia' else GRIS_OSCURO
        peso = 'bold' if pais == 'Colombia' else 'normal'
        ax.text(val + 1, i, f'{val:.0f}%', va='center', fontsize=14,
                color=color_txt, fontweight=peso)

    for label in ax.get_yticklabels():
        if label.get_text() == 'Colombia':
            label.set_color(VERDE)
            label.set_fontweight('bold')
            label.set_fontsize(14)

    ax.set_title(f'Colombia ocupa el puesto #{pos_col} mundial en electricidad renovable',
                 loc='left', fontsize=16, fontweight='bold', pad=25, color='#222')
    fig.text(0.125, 0.92, f'Top 8 paises del mundo - Ano {ultimo}',
             fontsize=11, color='#888', style='italic')
    fig.text(0.125, 0.02, f'Fuente: Our World in Data ({ultimo})',
             fontsize=9, color='#999')

    st.pyplot(fig)

    st.markdown("---")
    st.subheader("Justificacion critica")
    st.markdown(f"""
    **Tipo de sintesis aplicada:** Comparacion (quien tiene mas, quien tiene menos?). Por eso bar chart horizontal y no scatter ni pie.

    **Acto de habla:** Informar (declarativo).

    **Atributo pre-atentivo dominante:** color (hue). El cerebro detecta la barra verde antes de leer texto - esto explota la **memoria sensorial iconica** (< 1 segundo) y evita saturar la atencion consciente.

    **Por que solo 8 paises + Colombia:** la **memoria de trabajo** procesa entre 4 y 7 elementos. Mostrar 15 paises saturaria al lector. La posicion exacta (#{pos_col}) se comunica en el titulo-mensaje, no en el grafico.

    **Ley Gestalt aplicada:** similitud - las barras grises se perciben como un unico grupo "contexto"; la barra verde rompe esa similitud y se vuelve **figura sobre fondo**.

    **Test del HiPPO:** un directivo entiende en 3 segundos *"estoy en el top extendido pero lejos de los lideres"* sin leyendas.
    """)

# ========== RETO 2 ==========
elif reto == "Reto 2: Contraste":
    st.title("Reto 2: Contraste")
    st.caption("Eje: Sintaxis (Gestalt figura/fondo)")

    peers = ['Colombia', 'Brazil', 'Chile', 'Argentina', 'Mexico']
    sub = df[df['country'].isin(peers) & (df['year'] >= 1995)].copy()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # ANTES: ruido visual
    colores_ruido = ['red', 'blue', 'green', 'orange', 'purple']
    for pais, c in zip(peers, colores_ruido):
        d = sub[sub['country'] == pais]
        ax1.plot(d['year'], d['renewables_share_elec'], color=c, label=pais, linewidth=2)
    ax1.set_title('ANTES: que pais debo mirar?', fontsize=12, fontweight='bold', color='#B22222')
    ax1.legend(loc='lower right')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlabel('Ano')
    ax1.set_ylabel('% Electricidad renovable')

    # DESPUÉS: figura/fondo
    for pais in peers:
        d = sub[sub['country'] == pais]
        if pais == 'Colombia':
            ax2.plot(d['year'], d['renewables_share_elec'], color=VERDE, linewidth=3, zorder=3)
        else:
            ax2.plot(d['year'], d['renewables_share_elec'], color='#CCCCCC', linewidth=1.5, zorder=1)

    for pais in peers:
        val = sub[(sub['country'] == pais) & (sub['year'] == ultimo)]['renewables_share_elec']
        if len(val) == 0:
            continue
        val = val.values[0]
        color_txt = VERDE if pais == 'Colombia' else '#888'
        peso = 'bold' if pais == 'Colombia' else 'normal'
        ax2.text(ultimo + 0.3, val, pais, va='center', fontsize=9, color=color_txt, fontweight=peso)

    col_2018 = sub[(sub['country'] == 'Colombia') & (sub['year'] == 2018)]['renewables_share_elec'].values[0]
    col_ult = sub[(sub['country'] == 'Colombia') & (sub['year'] == ultimo)]['renewables_share_elec'].values[0]
    delta = col_ult - col_2018

    texto_insight = f'Estancación 2018-{ultimo}: {delta:+.1f} pp en {ultimo-2018} años'
    ax2.annotate(texto_insight,
                 xy=(2021, col_ult), xytext=(2003, 35),
                 fontsize=11, color=VERDE, fontweight='bold',
                 arrowprops=dict(arrowstyle='->', color=VERDE, lw=1.5))

    ax2.set_title('DESPUES: Colombia se quedo atras', fontsize=12, fontweight='bold', color=VERDE)
    for s in ['top', 'right']:
        ax2.spines[s].set_visible(False)
    ax2.set_xlabel('Ano')
    ax2.set_ylabel('% Electricidad renovable')
    ax2.set_xlim(1995, ultimo + 3)

    plt.suptitle('El poder del contraste: figura sobre fondo neutro',
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("---")
    st.subheader("Justificacion critica")
    st.markdown(f"""
    **Tipo de sintesis aplicada:** Correlacion temporal (relacion entre variable y tiempo). Por eso lineas y no barras agrupadas.

    **Acto de habla:** Convencer (directivo).

    **Por que el "ANTES" falla:** cinco colores saturados compiten por la atencion. El cerebro intenta procesar las cinco series simultaneamente y excede el limite de 4-7 elementos de la **memoria de trabajo**.

    **Por que el "DESPUES" funciona:**
    - **Figura/fondo (Gestalt):** Colombia (verde, grueso) actua como figura; los peers (gris claro, fino) son fondo.
    - **Anotacion directa:** el insight cuantificado ({delta:+.1f} pp) esta en el grafico.
    - **Sin leyenda:** las etiquetas de pais estan al final de cada linea (ley de proximidad).
    """)

# ========== RETO 3 ==========
elif reto == "Reto 3: Persuasion":
    st.title("Reto 3: Persuasion")
    st.caption("Eje: Acto de habla (storytelling ejecutivo)")

    sub = df[df['country'].isin(['Colombia', 'Chile']) & (df['year'] >= 2000)].copy()

    chile_2018 = sub[(sub['country'] == 'Chile') & (sub['year'] == 2018)]['renewables_share_elec'].values[0]
    chile_ult = sub[(sub['country'] == 'Chile') & (sub['year'] == ultimo)]['renewables_share_elec'].values[0]
    tasa_chile = (chile_ult - chile_2018) / (ultimo - 2018)

    anos_proy = list(range(ultimo, ultimo + 8))
    proy = [chile_ult + tasa_chile * (y - ultimo) for y in anos_proy]

    fig, ax = plt.subplots(figsize=(13, 7.5))

    for pais, color, ancho in [('Colombia', VERDE, 3), ('Chile', NARANJA, 2.5)]:
        d = sub[sub['country'] == pais]
        ax.plot(d['year'], d['renewables_share_elec'], color=color, linewidth=ancho, zorder=3)

    ax.plot(años_proy, proy, color=NARANJA, linewidth=1.5, linestyle='--', alpha=0.7, zorder=2)

    col_ult = sub[(sub['country'] == 'Colombia') & (sub['year'] == ultimo)]['renewables_share_elec'].values[0]
    ax.axhline(col_ult, color=VERDE, linestyle=':', alpha=0.4, zorder=1)

    ax.text(ultimo + 0.5, col_ult, ' Colombia', va='center', fontsize=12, color=VERDE, fontweight='bold')
    ax.text(anos_proy[-1] + 0.3, proy[-1], ' Chile (proyeccion)', va='center',
            fontsize=11, color=NARANJA, fontweight='bold')

    def bloque(x, y, titulo, texto, color):
        ax.text(x, y + 4, titulo, fontsize=11, fontweight='bold', color=color)
        ax.text(x, y, texto, fontsize=9.5, color='#333', va='top')

    txt_contexto = ('Colombia ha liderado renovables en LatAm\n'
                    'durante 20 anos gracias a su matriz hidrica.')
    txt_hallazgo = (f'Mientras Chile crecio {chile_ult-chile_2018:+.0f} pp en 5 anos,\n'
                    f'Colombia se estanco (~76%).')
    txt_recomend = ('Adjudicar subastas eolicas y solares\n'
                    '2026-2028 antes de perder liderazgo.')

    bloque(2000.5, 32, '1. CONTEXTO', txt_contexto, '#555')
    bloque(2010.5, 32, '2. HALLAZGO', txt_hallazgo, NARANJA)
    bloque(2020.5, 32, '3. RECOMENDACION', txt_recomend, VERDE)

    ax.set_title('Colombia perdera su liderazgo regional en renovables hacia 2028 si no acelera la transicion',
                 loc='left', fontsize=14, fontweight='bold', pad=15)

    for s in ['top', 'right']:
        ax.spines[s].set_visible(False)
    ax.spines['left'].set_color('#CCC')
    ax.spines['bottom'].set_color('#CCC')
    ax.tick_params(colors='#666')
    ax.set_ylabel('% Electricidad renovable', color='#666')
    ax.set_ylim(20, 95)
    ax.set_xlim(2000, anos_proy[-1] + 4)

    ax.text(2000, 16,
            f'Fuente: Our World in Data (2000-{ultimo}). Proyeccion: extrapolacion lineal de la tasa 2018-{ultimo}.',
            fontsize=8, color='#888', style='italic')

    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("---")
    st.subheader("Justificacion critica")
    st.markdown("""
    **Tipo de sintesis aplicada:** Correlacion temporal + proyeccion. Linea continua para historico, punteada para proyeccion - Gestalt: similitud diferenciada por estilo.

    **Acto de habla:** Motivar (compromisorio). El titulo no describe ("Evolucion de renovables") sino que **predice y exige accion**.

    **Storytelling tripartito:**
    1. **Contexto** (gris): establece el punto de partida.
    2. **Hallazgo** (naranja = alerta): cuantifica el riesgo.
    3. **Recomendacion** (verde = accion): concreta el "que hacer".

    **Test de 5 segundos:** el lector debe poder decir *"Vamos bien, pero nos estan alcanzando, hay que mover las subastas ya"*.
    """)

# ========== CONCLUSIONES ==========
elif reto == "Conclusiones":
    st.title("Conclusiones")

    st.subheader("Sintesis del framework aplicado")

    tabla = pd.DataFrame({
        'Eje': ['Eficiencia (pre-atentivo)', 'Sintaxis (Gestalt)', 'Sintesis de datos', 'Acto de habla'],
        'Reto 1': ['Color (hue)', 'Similitud + continuidad', 'Comparacion', 'Informar'],
        'Reto 2': ['Grosor + color', 'Figura/fondo', 'Correlacion temporal', 'Convencer'],
        'Reto 3': ['Color + posicion', 'Proximidad + figura/fondo', 'Correlacion + proyeccion', 'Motivar']
    })
    st.dataframe(tabla, use_container_width=True, hide_index=True)

    st.subheader("Limitaciones")
    st.markdown("""
    - La proyeccion lineal de Chile asume continuidad de la tasa 2018-{ultimo}; en la realidad podria desacelerar.
    - "Renewables share" no distingue entre hidroelectrica (legado de Colombia) y nueva capacidad solar/eolica.
    - Seria ideal complementar con datos de capacidad instalada y subastas adjudicadas (CREG / UPME).
    """.replace("{ultimo}", str(ultimo)))

    st.subheader("Reflexion metodologica")
    st.info("""
    El mismo dataset puede **informar, convencer o motivar** dependiendo del diseno.
    La decision sobre que atributos pre-atentivos activar es, en ultima instancia,
    una decision retorica - no estetica. El analista no "muestra datos",
    **construye argumentos visuales**.
    """)
