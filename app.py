import streamlit as st
import pandas as pd
import requests as rq
import altair as alt
import altair as alt

# ==============================
# CONFIGURACIÓN BÁSICA STREAMLIT
# ==============================
st.set_page_config(
    page_title="Analítica FEB",
    page_icon="🏀",
    layout="wide"
)

# ==============================
# 1) LOGIN SENCILLO CON SESIÓN
# ==============================
USERS = {
    "admin": "admin",
    "professor": "feb2024"
}

def login_page():
    st.title("🏀 Aplicación FEB - Login")

    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Entrar"):
        if username in USERS and USERS[username] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success("Sesión iniciada correctamente.")
            st.rerun()

        else:
            st.error("Credenciales incorrectas.")

def check_login():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        login_page()
        st.stop()

# ==============================
# 2) PRIMERA FUENTE: CSV LOCAL
# ==============================
@st.cache_data
def load_csv_data():
    """
    Carga el CSV baloncestoenvivo.csv y corrige los nombres de columnas.
    """
    df = pd.read_csv("baloncestoenvivo.csv")

    # Mapeo por nombre original
    rename_map = {}

    # Si existen estas columnas, las renombramos
    if "nombre" in df.columns:
        rename_map["nombre"] = "EQUIPO"
    if "nombre href" in df.columns:
        rename_map["nombre href"] = "ENLACE"
    if "partidos" in df.columns:
        rename_map["partidos"] = "PARTIDOS"
    if "tot" in df.columns:
        rename_map["tot"] = "MIN totales"
    if "med" in df.columns:
        rename_map["med"] = "Media MIN"
    if "tot" in df.columns:
        rename_map["tot 2"] = "PTS totales"
    if "med" in df.columns:
        rename_map["med 2"] = "Media PTS"
    if "tot" in df.columns:
        rename_map["tot 3"] = "T2"
    if "med" in df.columns:
        rename_map["med 3"] = "T2P"
    if "tot" in df.columns:
        rename_map["tot 4"] = "T3"
    if "med" in df.columns:
        rename_map["med 4"] = "T3P"
    if "tot" in df.columns:
        rename_map["tot 5"] = "TC"
    if "med" in df.columns:
        rename_map["med 5"] = "TCP"
    if "tot" in df.columns:
        rename_map["tot 6"] = "TL"
    if "med" in df.columns:
        rename_map["med 6"] = "TLP"
    if "tot" in df.columns:
        rename_map["tot 7"] = "RO totales"
    if "med" in df.columns:
        rename_map["med 7"] = "Media RO"
    if "tot" in df.columns:
        rename_map["tot 8"] = "RD totales"
    if "med" in df.columns:
        rename_map["med 8"] = "Media RD"
    if "tot" in df.columns:
        rename_map["tot 9"] = "RT totales"
    if "med" in df.columns:
        rename_map["med 9"] = "Media RT"
    if "tot" in df.columns:
        rename_map["tot 10"] = "AST totales"
    if "med" in df.columns:
        rename_map["med 10"] = "Media AST"
    if "tot" in df.columns:
        rename_map["tot 11"] = "REC totales"
    if "med" in df.columns:
        rename_map["med 11"] = "Media REC"
    if "tot" in df.columns:
        rename_map["tot 12"] = "PERD totales"
    if "med" in df.columns:
        rename_map["med 12"] = "Media PERD"
    if "tot" in df.columns:
        rename_map["tot 13"] = "TAPF totales"
    if "med" in df.columns:
        rename_map["med 13"] = "Media TAPF"
    if "tot" in df.columns:
        rename_map["tot 14"] = "TAPC totales"
    if "med" in df.columns:
        rename_map["med 14"] = "Media TAPC"
    if "tot" in df.columns:
        rename_map["tot 15"] = "MAT totales"
    if "med" in df.columns:
        rename_map["med 15"] = "Media MAT"
    if "tot" in df.columns:
        rename_map["tot 16"] = "FALC totales"
    if "med" in df.columns:
        rename_map["med 16"] = "Media FALC"
    if "tot" in df.columns:
        rename_map["tot 17"] = "FALR totales"
    if "med" in df.columns:
        rename_map["med 17"] = "Media FALR"
    if "tot" in df.columns:
        rename_map["tot 18"] = "VAL total"
    if "med" in df.columns:
        rename_map["med 18"] = "Media VAL"
    
    df = df.rename(columns=rename_map)

    return df


# ==============================
# 3) SEGUNDA FUENTE: API FEB (SCRAPING)
# ==============================

DEFAULT_GAME_IDS = [2480158]
DEFAULT_FINAL_NUMBER = 1728856032308

HEADERS = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'en-GB,en;q=0.9,es-ES;q=0.8,es;q=0.7,en-US;q=0.6',
    'connection': 'keep-alive',
    'host': 'intrafeb.feb.es',
    'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImQzOWE5MzlhZTQyZmFlMTM5NWJjODNmYjcwZjc1ZDc3IiwidHlwIjoiSldUIn0.eyJuYmYiOjE3NjM1NDM3OTYsImV4cCI6MTc2MzYzMDE5NiwiaXNzIjoiaHR0cHM6Ly9pbnRyYWZlYi5mZWIuZXMvaWRlbnRpdHkuYXBpIiwiYXVkIjpbImh0dHBzOi8vaW50cmFmZWIuZmViLmVzL2lkZW50aXR5LmFwaS9yZXNvdXJjZXMiLCJsaXZlc3RhdHMuYXBpIl0sImNsaWVudF9pZCI6ImJhbG9uY2VzdG9lbnZpdm9hcHAiLCJpZGFtYml0byI6IjEiLCJyb2xlIjpbIk92ZXJWaWV3IiwiVGVhbVN0YXRzIiwiU2hvdENoYXJ0IiwiUmFua2luZyIsIktleUZhY3RzIiwiQm94U2NvcmUiXSwic2NvcGUiOlsibGl2ZXN0YXRzLmFwaSJdfQ.VhSm1RIWzAd2wpATJ5RXBcCSovbJAD81sWWnbZXzUGGBpPKKeUp-EsLfweIMYXQTg_MA3TxqlQx4GbOpd3MhpRJeKx4V1hXMES424kV5lsJaOsZGj7mWNJKIJpotI4oMk5yS8tbHqetPqP5WGxojGCP9CVuvHf8EakRAjybRTHDp5JRQuTc6dqL6zf_1oGXer-e6NFDkN0203M-UkzoifbNzsE_1W9WgWBiH9qYIr7OKb-3cza90RAnV3qp00FW5I6BIZ2Z15QUhWyw3U1GLFlOuHnqLES2Y9jEJ1AtAw_TXsJvRSoWHHjCbMDghxKK6FJexiXM_bkHQJd3SYmCO-g',
    'origin': 'https://baloncestoenvivo.feb.es',
    'referer': 'https://baloncestoenvivo.feb.es/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

def get_game_data(game_id: int, final_number: int, headers: dict):
    try:
        url_base = f"https://intrafeb.feb.es/LiveStats.API/api/v1/BoxScore/{game_id}?={final_number}"
        response = rq.get(url_base, headers=headers)
        print(f"[GET] BoxScore {game_id} - Status: {response.status_code}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error al acceder a game_id={game_id}: {e}")
        return None

def get_play_by_play(game_id: int, final_number: int, headers: dict):
    try:
        pbp_url = f"https://intrafeb.feb.es/LiveStats.API/api/v1/KeyFacts/{game_id}?={final_number}"
        response = rq.get(pbp_url, headers=headers)
        print(f"[GET] PlayByPlay {game_id} - Status: {response.status_code}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error al acceder al PBP del game_id={game_id}: {e}")
        return None

def limpiar_datos_boxscore(raw_json):
    jugadores_df = pd.DataFrame()
    for team in [0, 1]:
        b = pd.json_normalize(raw_json['BOXSCORE']['TEAM'][team]["PLAYER"])
        b["Local"] = team
        jugadores_df = pd.concat([jugadores_df, b])
    jugadores_df["Is_local"] = jugadores_df["Local"] == 0

    jugadores_df.columns = [col.upper() for col in jugadores_df.columns]

    for col in jugadores_df.columns:
        if jugadores_df[col].dtype == object:
            jugadores_df[col] = jugadores_df[col].astype(str).str.replace(",", ".", regex=False)

    jugadores_df = jugadores_df.apply(pd.to_numeric, errors='ignore')

    return jugadores_df

def limpiar_datos_header(raw_json):
    info = pd.json_normalize(raw_json["HEADER"])[["competition", "round", "starttime"]]
    info[["Dia", "Hora"]] = info["starttime"].astype(str).str.split(r" - ", expand=True)
    return info[["competition", "round", "Dia"]]

def limpiar_datos_pbp(pbp_json):
    df_pbp = pd.json_normalize(pbp_json["PLAYBYPLAY"]["LINES"])[::-1].reset_index(drop=True)
    return df_pbp

def ejecutar_scraping(game_ids, final_number, headers):
    resultados = {}
    for gid in game_ids:
        print(f"🔄 Procesando Game_ID={gid}...")
        game_data = get_game_data(gid, final_number, headers)
        if not game_data:
            print("⚠️  No se pudo obtener game_data.")
            continue

        pbp_data = get_play_by_play(gid, final_number, headers)
        if not pbp_data:
            print("⚠️  No se pudo obtener play_by_play.")
            continue

        try:
            jugadores_df = limpiar_datos_boxscore(game_data)
            info_df = limpiar_datos_header(game_data)
            pbp_df = limpiar_datos_pbp(pbp_data)

            resultados[gid] = {
                "jugadores": jugadores_df,
                "info": info_df,
                "pbp": pbp_df
            }

            print(f"✅ DataFrames generados para Game_ID={gid}")

        except Exception as e:
            print(f"❌ Error procesando Game_ID={gid}: {e}")

    return resultados

@st.cache_data
def load_feb_api_data(game_ids, final_number):
    resultados = ejecutar_scraping(game_ids, final_number, HEADERS)

    all_jug = []
    all_info = []
    all_pbp = []

    for gid, vals in resultados.items():
        j = vals["jugadores"].copy()
        j["GAME_ID"] = gid
        all_jug.append(j)

        info = vals["info"].copy()
        info["GAME_ID"] = gid
        all_info.append(info)

        pbp = vals["pbp"].copy()
        pbp["GAME_ID"] = gid
        all_pbp.append(pbp)

    df_jug = pd.concat(all_jug, ignore_index=True) if all_jug else pd.DataFrame()
    df_info = pd.concat(all_info, ignore_index=True) if all_info else pd.DataFrame()
    df_pbp = pd.concat(all_pbp, ignore_index=True) if all_pbp else pd.DataFrame()

    return df_jug, df_info, df_pbp

# ==============================
# 4) BOTÓN IMPRIMIR
# ==============================
def print_button():
    if st.button("🖨️ Imprimir página"):
        st.markdown(
            """
            <script>
            window.print();
            </script>
            """,
            unsafe_allow_html=True
        )

# ==============================
# 5) PÁGINA 1 – RESUMEN COMPETICIÓN (CSV)
# ==============================
def page_resum_competicio():
    st.title("📊 Resumen de la competición (CSV)")

    df_partits = load_csv_data()

    st.subheader("Datos del CSV")
    st.dataframe(df_partits)

    st.markdown("#### Selecciona un equipo")

    # Forcem la columna "EQUIPO"
    col_categoria = "EQUIPO"

    # Llista d'equips (valors únics)
    categorias = sorted(df_partits[col_categoria].dropna().unique())

    # Selector d'un equip concret
    categoria_sel = st.selectbox("Equipo", categorias)

    # Filtrar només per EQUIPO seleccionat
    df_filtrat = df_partits[
        df_partits[col_categoria] == categoria_sel
    ]

    st.markdown("#### Equipo filtrado")
    st.dataframe(df_filtrat)

      # ==============================
    # GRÁFICO: PTS POR PARTIDO (Y) vs T3P (X)
    # ==============================
    st.markdown("### Relación entre puntos por partido y T3P")

    df_puntos = df_partits.copy()

    # 1) Puntos por partido
    if "Media PTS" in df_puntos.columns:
        # Limpiamos Media PTS por si viene con coma decimal
        pts = (
            df_puntos["Media PTS"]
            .astype(str)
            .str.replace(",", ".", regex=False)
        )
        df_puntos["PTS_por_partido"] = pd.to_numeric(pts, errors="coerce")

    elif {"PTS totales", "PARTIDOS"}.issubset(df_puntos.columns):
        # Nos aseguramos de que sean numéricos antes de dividir
        df_puntos["PTS totales"] = pd.to_numeric(df_puntos["PTS totales"], errors="coerce")
        df_puntos["PARTIDOS"] = pd.to_numeric(df_puntos["PARTIDOS"], errors="coerce")
        df_puntos["PTS_por_partido"] = df_puntos["PTS totales"] / df_puntos["PARTIDOS"]

    else:
        st.warning("No se pueden calcular los puntos por partido (faltan columnas necesarias).")
        print_button()
        return

    # 2) Limpiar T3P (quitar %, coma → punto, numérico)
    if "T3P" not in df_puntos.columns:
        st.warning("No se encuentra la columna T3P en el CSV.")
        print_button()
        return

    t3p = (
        df_puntos["T3P"]
        .astype(str)
        .str.replace("%", "", regex=False)
        .str.replace(",", ".", regex=False)
    )
    df_puntos["T3P"] = pd.to_numeric(t3p, errors="coerce")

    # 3) Quitamos filas sin datos válidos en alguna de las dos métricas
    df_puntos = df_puntos.dropna(subset=["PTS_por_partido", "T3P"])

    # 4) Límites dinámicos de ambos ejes
    x_min = df_puntos["T3P"].min() - 1
    x_max = df_puntos["T3P"].max() + 1

    y_min = df_puntos["PTS_por_partido"].min() - 1
    y_max = df_puntos["PTS_por_partido"].max() + 1

    # Tabla resumen (opcional)
    st.dataframe(df_puntos[["EQUIPO", "PTS_por_partido", "T3P"]])

    # 5) Gráfico de dispersión con etiquetas
    base = alt.Chart(df_puntos).encode(
        x=alt.X("T3P:Q", title="T3P (%)", scale=alt.Scale(domain=[x_min, x_max])),
        y=alt.Y("PTS_por_partido:Q", title="Puntos por partido", scale=alt.Scale(domain=[y_min, y_max]))
    )

    puntos = base.mark_circle(size=80).encode(
        tooltip=["EQUIPO", "PTS_por_partido", "T3P"]
    )

    etiquetas = base.mark_text(dy=-7).encode(
        text="EQUIPO"
    )

    chart = puntos + etiquetas

    st.altair_chart(chart, use_container_width=True)


    print_button()

# ==============================
# 6) PÁGINA 2 – ESTADÍSTICAS JUGADORES (API FEB)
# ==============================
import altair as alt

def page_estadistiques_jugadors_api():
    st.title("📈 Estadísticas de jugadores (API FEB)")

    # =======================
    # CONFIGURACIÓN BARRA LATERAL
    # =======================
    st.sidebar.markdown("### Configuración FEB API")

    # Desplegable con los posibles GAME IDs
    posibles_gids = [2480112, 2480113, 2480128, 2480130, 2480143, 2480158]
    game_id = st.sidebar.selectbox("Game ID", posibles_gids)

    game_ids = [game_id]  # se pasa como lista

    st.sidebar.markdown("---")

    # =======================
    # CARGA API
    # =======================
    with st.spinner("Cargando datos desde la API FEB..."):
        df_jug, df_info, df_pbp = load_feb_api_data(game_ids, DEFAULT_FINAL_NUMBER)

    if df_jug.empty:
        st.warning("No se han obtenido datos de jugadores. Revisa Game ID o el token.")
        return

    # =======================
    # MOSTRAR HEADER (sin GAME_ID)
    # =======================
    st.subheader("Información básica de partidos (HEADER)")
    if "GAME_ID" in df_info.columns:
        st.dataframe(df_info.drop(columns=["GAME_ID"]))
    else:
        st.dataframe(df_info)

    # =======================
    # MOSTRAR BOXSCORE COMPLETO
    # =======================
    st.subheader("Estadísticas de jugadores (BOXSCORE)")
    st.dataframe(df_jug)

    # =======================
    # FILTRADO JUGADORES
    # =======================
    st.markdown("### Jugadores filtrados")

    cols = st.columns(2)

    with cols[0]:
        # Local o Visitante (IS_LOCAL)
        opciones_local = ["Todos", "Local", "Visitante"]
        local_sel = st.selectbox("Equipo", opciones_local)

    with cols[1]:
        # Métrica (cualquier columna del boxscore)
        metricas = sorted([col for col in df_jug.columns if df_jug[col].dtype != 'object'])
        metrica = st.selectbox("Métrica", metricas)

    # =======================
    # APLICAR FILTROS
    # =======================
    df_filt = df_jug.copy()

    # Filtrar local/visitante
    if local_sel == "Local":
        df_filt = df_filt[df_filt["IS_LOCAL"] == 1]
    elif local_sel == "Visitante":
        df_filt = df_filt[df_filt["IS_LOCAL"] == 0]

    st.dataframe(df_filt)

    # =======================
    # TOP 5 ORDENADO (MÉTRICA)
    # =======================
    st.markdown("### Top 5 jugadores por la métrica seleccionada")

    # Detectamos nombre de jugador
    name_col = "PLAYERNAME" if "PLAYERNAME" in df_filt.columns else ("NAME" if "NAME" in df_filt.columns else None)

    if name_col is not None and metrica in df_filt.columns:
        df_temp = df_filt.copy()
        serie = df_temp[metrica].astype(str)

        # 🔹 Formatos mixtos → Convertir a numérico (funciona con %, comas y tiempos)
        if serie.str.contains(":").any():  # tiempo
            parts = serie.str.split(":", expand=True)
            for c in parts.columns:
                parts[c] = pd.to_numeric(parts[c], errors="coerce").fillna(0)

            if parts.shape[1] == 2:  # MM:SS
                metric_num = parts[0] + parts[1] / 60.0
            elif parts.shape[1] == 3:  # HH:MM:SS
                metric_num = parts[0] * 60.0 + parts[1] + parts[2] / 60.0
            else:
                metric_num = pd.to_numeric(
                    serie.str.replace(",", ".", regex=False),
                    errors="coerce"
                )
        else:
            clean = (
                serie.str.replace("%", "", regex=False)
                     .str.replace(",", ".", regex=False)
            )
            metric_num = pd.to_numeric(clean, errors="coerce")

        df_temp["_metric_num"] = metric_num
        df_top = df_temp.dropna(subset=["_metric_num"]).nlargest(5, "_metric_num")

        if not df_top.empty:
            df_top[metrica] = df_top["_metric_num"]

            df_top_plot = df_top[[name_col, metrica]]

            chart = (
                alt.Chart(df_top_plot)
                .mark_bar()
                .encode(
                    x=alt.X(f"{name_col}:N", sort="-y", title="Jugador"),
                    y=alt.Y(f"{metrica}:Q", title=metrica),
                    tooltip=[name_col, metrica]
                )
            )

            st.altair_chart(chart, use_container_width=True)

    # =======================
    # PLAY-BY-PLAY
    # =======================
#    st.markdown("### Play-by-Play (KeyFacts)")
#    st.dataframe(df_pbp.head(50))

    # ---- Botón imprimir ----
    print_button()




# ==============================
# 7) MAIN – MENÚ Y NAVEGACIÓN
# ==============================
def main():
    check_login()

    st.sidebar.title(f"Bienvenido/a, {st.session_state.get('username', '')}")
    page = st.sidebar.radio(
        "Navegación",
        ["Resumen competición (CSV)", "Estadísticas jugadores (API FEB)"]
    )

    if st.sidebar.button("Cerrar sesión"):
        st.session_state["logged_in"] = False
        st.rerun()

    if page == "Resumen competición (CSV)":
        page_resum_competicio()
    elif page == "Estadísticas jugadores (API FEB)":
        page_estadistiques_jugadors_api()

if __name__ == "__main__":
    main()
    
