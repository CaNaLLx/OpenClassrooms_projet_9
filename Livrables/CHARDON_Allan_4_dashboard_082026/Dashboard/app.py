from collections import Counter
import base64
from io import BytesIO
from pathlib import Path
import re
import sys

import pandas as pd
import plotly.express as px
import streamlit as st
from setfit import SetFitModel
from wordcloud import WordCloud


st.set_page_config(
    page_title="Analyse de sentiments",
    layout="wide",
)
st.markdown(
    "<style>[data-testid='stCaptionContainer'] {opacity: 1 !important;} "
    "[data-testid='stCaptionContainer'] p, th {color: #262730 !important;}</style>",
    unsafe_allow_html=True,
)

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from SRC.preprocessing import clean_tweet_SETFIT
from SRC.prediction import convertir_predictions_setfit

DATA_PATH = ROOT / "Data" / "SPLIT" / "test_independant.csv"
RESULT_PATH = ROOT / "Results" / "comparaison_modeles.csv"
MODEL_ID = "AllanC23/setfit-mpnet-sentiment"
MODEL_REVISION = "403b8b648f16e6eb919ef76037ae62fcc80daa1d"

LABELS = {0: "Négatif", 1: "Positif"}
COLORS = {"Négatif": "#D55E00", "Positif": "#0072B2"}


def afficher_graphique(figure, description, donnees=None, titre_tableau=None):
    figure.update_layout(
        font={"size": 16, "color": "#262730"},
        legend={"font": {"size": 16, "color": "#262730"}},
        legend_title_font={"size": 16, "color": "#262730"},
        hoverlabel={"font_size": 16, "font_color": "#262730", "bgcolor": "white"},
        paper_bgcolor="white",
        plot_bgcolor="white",
        autosize=True,
    )
    figure.update_xaxes(tickfont={"size": 16, "color": "#262730"}, title_font={"size": 16, "color": "#262730"}, automargin=True)
    figure.update_yaxes(tickfont={"size": 16, "color": "#262730"}, title_font={"size": 16, "color": "#262730"}, automargin=True)
    st.plotly_chart(figure, width="stretch", config={"displaylogo": False})
    st.caption(description)
    if donnees is not None:
        with st.expander(titre_tableau):
            st.table(donnees)


@st.cache_data
def load_data():
    data = pd.read_csv(DATA_PATH)
    if not {"tweet", "label"}.issubset(data.columns):
        raise ValueError("Le fichier de test doit contenir les colonnes tweet et label.")
    if not data["label"].isin(LABELS).all():
        raise ValueError("Les labels du test doivent être 0 ou 1.")
    data["tweet"] = data["tweet"].fillna("").astype(str)
    data["sentiment"] = data["label"].map(LABELS)
    data["nombre_mots"] = data["tweet"].str.split().str.len()
    return data


@st.cache_resource
def load_model():
    return SetFitModel.from_pretrained(MODEL_ID, revision=MODEL_REVISION, device="cpu")


try:
    df = load_data()
except (OSError, ValueError) as error:
    st.error(f"Impossible de charger le jeu de test : {error}")
    st.stop()

st.title("Analyse de sentiments de tweets")
st.write(
    "Cette application présente le jeu de données et prédit "
    "si un tweet exprime un sentiment positif ou négatif."
)
st.caption("Parcours : explorer les tweets, tester un message, puis comparer les modèles.")

tab_eda, tab_prediction, tab_performance = st.tabs(
    ["Analyse des données", "Prédiction", "Performances"]
)


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
        fig.update_traces(textposition="outside", textfont={"size": 16, "color": "#262730"}, cliponaxis=False)
        repartition = "; ".join(
            f"{row.Sentiment} : {row.Nombre:,}".replace(",", " ")
            for row in class_counts.itertuples()
        )
        afficher_graphique(
            fig, f"Tweets sélectionnés — {repartition}.",
            class_counts.set_index("Sentiment"), "Voir les effectifs par sentiment",
        )

        st.subheader("Longueur des tweets")

        fig = px.histogram(
            filtered_df,
            x="nombre_mots",
            color="sentiment",
            color_discrete_map=COLORS,
            pattern_shape="sentiment",
            pattern_shape_map={"Négatif": "", "Positif": "/"},
            nbins=30,
            barmode="overlay",
            opacity=0.7,
            labels={
                "nombre_mots": "Nombre de mots",
                "sentiment": "Sentiment",
            },
        )
        longueurs = pd.crosstab(filtered_df["nombre_mots"], filtered_df["sentiment"])
        longueurs.index.name = "Nombre de mots"
        afficher_graphique(
            fig,
            "La longueur des tweets est comparée par sentiment. Les noms et les motifs distinguent les groupes.",
            longueurs, "Voir les effectifs par longueur",
        )

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
        fig.update_traces(textposition="outside", textfont={"size": 16, "color": "#262730"}, cliponaxis=False)
        afficher_graphique(
            fig,
            "Ces mots sont les plus fréquents dans la sélection. Leur fréquence ne mesure pas leur influence sur le modèle.",
            frequencies.set_index("Mot"), "Voir les fréquences des mots",
        )

        st.subheader("Nuage de mots")

        if words:
            wordcloud = WordCloud(
                width=1200,
                height=500,
                background_color="white",
                random_state=42,
                max_words=50,
                min_font_size=16,
                color_func=lambda *args, **kwargs: "#262730",
            ).generate(" ".join(words))

            buffer = BytesIO()
            wordcloud.to_image().save(buffer, format="PNG")
            image_data = base64.b64encode(buffer.getvalue()).decode("ascii")
            st.markdown(
                f'<img src="data:image/png;base64,{image_data}" '
                'alt="Nuage des mots fréquents. La liste et leurs poids relatifs sont disponibles dans le tableau suivant." '
                'style="width:100%;height:auto;">',
                unsafe_allow_html=True,
            )
            with st.expander("Lire les mots du nuage en tableau"):
                st.table(pd.DataFrame(
                    wordcloud.words_.items(), columns=["Mot", "Poids relatif dans le nuage"]
                ).set_index("Mot").round(3))


with tab_prediction:
    st.header("Prédire le sentiment d'un tweet")

    mode = st.radio(
        "Méthode de saisie",
        ["Saisir un tweet", "Choisir un exemple"],
        horizontal=True,
    )
    true_label = None

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
        true_label = int(df.loc[examples[examples == tweet].index[0], "label"])

    if st.button("Analyser le sentiment", type="primary"):
        if not tweet.strip():
            st.warning("Veuillez saisir ou sélectionner un tweet.")

        else:
            try:
                with st.spinner("Analyse en cours..."):
                    prediction = convertir_predictions_setfit(
                        load_model().predict([clean_tweet_SETFIT(tweet)])
                    )[0]
            except Exception:
                st.error("Le modèle est indisponible. Veuillez réessayer dans quelques instants.")
                st.stop()

            sentiment = LABELS[prediction]

            if sentiment == "Positif":
                st.success("Prédiction : sentiment positif")
            else:
                st.error("Prédiction : sentiment négatif")

            st.write("Texte analysé :", tweet)
            if true_label is not None:
                st.write("Sentiment indiqué dans le dataset :", LABELS[true_label])


with tab_performance:
    st.header("Performances comparées")

    st.write(
        f"Les modèles sont évalués sur les mêmes {len(df):,} tweets de test, "
        "après exclusion des doublons avec l'entraînement et la validation. "
        "La métrique principale est le F1-score macro."
    )
    st.caption(
        "L'accuracy est la part de bonnes réponses. Le F1 macro combine précision et rappel "
        "pour les deux sentiments. Pour ces deux scores, 1 est la meilleure valeur."
    )

    try:
        results = pd.read_csv(RESULT_PATH)
        columns = ["Modèle", "Accuracy", "F1 macro", "Exemples d'entraînement"]
        if len(results) != 2 or not set(columns + ["Nombre de tweets test"]).issubset(results.columns):
            raise ValueError("Le fichier de résultats doit contenir les deux modèles évalués.")
        if not results["Nombre de tweets test"].eq(len(df)).all():
            raise ValueError("Les résultats ne correspondent pas au jeu de test affiché.")
        if not results[["Accuracy", "F1 macro"]].apply(lambda values: values.between(0, 1).all()).all():
            raise ValueError("Les scores doivent être compris entre 0 et 1.")
    except (OSError, ValueError):
        st.warning("Les résultats sont indisponibles. Exécutez la comparaison dans le notebook.")
        st.stop()

    st.table(results[columns].set_index("Modèle").style.format({
        "Accuracy": "{:.4f}", "F1 macro": "{:.4f}",
    }))

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
        pattern_shape="Métrique",
        pattern_shape_map={"Accuracy": "", "F1 macro": "/"},
        barmode="group",
        text_auto=".4f",
        range_y=[0, 1],
    )

    fig.update_traces(textposition="outside", textfont={"size": 16, "color": "#262730"}, cliponaxis=False)
    description = " ; ".join(
        f"{modele} : F1 macro {score:.4f}, {int(effectif)} exemples".replace(".", ",")
        for modele, score, effectif in zip(
            results["Modèle"], results["F1 macro"], results["Exemples d'entraînement"]
        )
    )
    afficher_graphique(fig, description)

    st.info(
        "SetFit est entraîné avec moins de données que le BiLSTM. "
        "La comparaison évalue donc également son efficacité en données. "
        "Un faible écart de score ne suffit pas à établir une supériorité générale."
    )
