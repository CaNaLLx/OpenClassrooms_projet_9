from collections import Counter
from pathlib import Path
import re

import pandas as pd
import plotly.express as px
import streamlit as st
from setfit import SetFitModel
from wordcloud import WordCloud


# Configuration

st.set_page_config(
    page_title="Analyse de sentiments",
    layout="wide",
)

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "Data" / "SPLIT" / "test.csv"
RESULT_PATH = ROOT / "Results" / "comparaison_modeles.csv"
MODEL_ID = "AllanC23/setfit-mpnet-sentiment"

LABELS = {0: "Négatif", 1: "Positif"}
COLORS = {"Négatif": "#D55E00", "Positif": "#0072B2"}


# Chargement des données et du modèle

@st.cache_data
def load_data():
    data = pd.read_csv(DATA_PATH)
    data["tweet"] = data["tweet"].fillna("").astype(str)
    data["sentiment"] = data["label"].map(LABELS)
    data["nombre_mots"] = data["tweet"].str.split().str.len()
    return data


@st.cache_resource
def load_model():
    return SetFitModel.from_pretrained(MODEL_ID)


df = load_data()


# En-tête

st.title("Analyse de sentiments de tweets")
st.write(
    "Cette application présente le jeu de données et prédit "
    "si un tweet exprime un sentiment positif ou négatif."
)

tab_eda, tab_prediction, tab_performance = st.tabs(
    ["Analyse des données", "Prédiction", "Performances"]
)


# Analyse exploratoire

with tab_eda:
    st.header("Analyse exploratoire")

    selected_sentiments = st.multiselect(
        "Sentiments à afficher",
        options=list(COLORS),
        default=list(COLORS),
    )

    filtered_df = df[df["sentiment"].isin(selected_sentiments)]

    if filtered_df.empty:
        st.warning("Sélectionnez au moins un sentiment.")

    else:
        col1, col2, col3 = st.columns(3)
        col1.metric("Nombre de tweets", len(filtered_df))
        col2.metric(
            "Longueur moyenne",
            f"{filtered_df['nombre_mots'].mean():.1f} mots",
        )
        col3.metric(
            "Longueur médiane",
            f"{filtered_df['nombre_mots'].median():.0f} mots",
        )

        st.subheader("Répartition des sentiments")

        class_counts = (
            filtered_df["sentiment"]
            .value_counts()
            .rename_axis("Sentiment")
            .reset_index(name="Nombre")
        )

        fig = px.bar(
            class_counts,
            x="Sentiment",
            y="Nombre",
            color="Sentiment",
            color_discrete_map=COLORS,
            text_auto=True,
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Longueur des tweets")

        fig = px.histogram(
            filtered_df,
            x="nombre_mots",
            color="sentiment",
            color_discrete_map=COLORS,
            nbins=30,
            barmode="overlay",
            opacity=0.7,
            labels={
                "nombre_mots": "Nombre de mots",
                "sentiment": "Sentiment",
            },
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Mots les plus fréquents")

        number_words = st.slider(
            "Nombre de mots",
            min_value=5,
            max_value=30,
            value=15,
        )

        text = " ".join(filtered_df["tweet"]).lower()
        words = re.findall(r"\b[a-zA-Z]{3,}\b", text)

        frequencies = pd.DataFrame(
            Counter(words).most_common(number_words),
            columns=["Mot", "Fréquence"],
        )

        fig = px.bar(
            frequencies,
            x="Fréquence",
            y="Mot",
            orientation="h",
            text_auto=True,
        )
        fig.update_layout(yaxis_categoryorder="total ascending")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Nuage de mots")

        if words:
            wordcloud = WordCloud(
                width=1200,
                height=500,
                background_color="white",
                random_state=42,
            ).generate(" ".join(words))

            st.image(
                wordcloud.to_array(),
                use_container_width=True,
            )


# Prédiction

with tab_prediction:
    st.header("Prédire le sentiment d'un tweet")

    mode = st.radio(
        "Méthode de saisie",
        ["Saisir un tweet", "Choisir un exemple"],
        horizontal=True,
    )

    if mode == "Saisir un tweet":
        tweet = st.text_area(
            "Texte du tweet",
            placeholder="Saisissez un tweet en anglais...",
            max_chars=280,
        )
    else:
        examples = df["tweet"].sample(
            min(20, len(df)),
            random_state=42,
        )
        tweet = st.selectbox(
            "Sélectionnez un tweet",
            examples,
        )

    if st.button("Analyser le sentiment", type="primary"):
        if not tweet.strip():
            st.warning("Veuillez saisir ou sélectionner un tweet.")

        else:
            with st.spinner("Analyse en cours..."):
                prediction = load_model().predict([tweet])[0]

            try:
                sentiment = LABELS[int(prediction)]
            except (ValueError, TypeError):
                sentiment = str(prediction).capitalize()

            if sentiment == "Positif":
                st.success("Prédiction : sentiment positif")
            else:
                st.error("Prédiction : sentiment négatif")

            st.write("Texte analysé :", tweet)


# Performances

with tab_performance:
    st.header("Performances comparées")

    st.write(
        "Les modèles sont évalués sur le même jeu de test. "
        "La métrique principale est le F1-score macro."
    )

    # À remplacer par les résultats définitifs
    results = pd.DataFrame(
        {
            "Modèle": ["BiLSTM", "SetFit"],
            "Accuracy": [0.80, 0.83],
            "F1 macro": [0.80, 0.83],
            "Exemples d'entraînement": [300_000, 1_024],
        }
    )

    st.dataframe(
        results,
        hide_index=True,
        use_container_width=True,
    )

    results_long = results.melt(
        id_vars="Modèle",
        value_vars=["Accuracy", "F1 macro"],
        var_name="Métrique",
        value_name="Score",
    )

    fig = px.bar(
        results_long,
        x="Modèle",
        y="Score",
        color="Métrique",
        barmode="group",
        text_auto=".3f",
        range_y=[0, 1],
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "SetFit est entraîné avec moins de données que le BiLSTM. "
        "La comparaison évalue donc également son efficacité en données."
    )
