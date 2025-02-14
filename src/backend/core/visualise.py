import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st
import plotly.graph_objects as go


class DataVisualizer:
    def __init__(self, df, dark_mode=True):
        self.df = df
        self.dark_mode = dark_mode
        self._set_style()

    def _set_style(self):
        """Configure le mode sombre ou clair pour les visualisations"""
        if self.dark_mode:
            sns.set_theme(style="darkgrid")
            plt.style.use("dark_background")
        else:
            sns.set_theme(style="whitegrid")
            plt.style.use("seaborn-white")

    def show_dataframe(self):
        """Affiche un aperçu des premières lignes du DataFrame"""
        st.write("### DataFrame")
        st.write(self.df.head())

    def plot_histogram(self, column, bins=20, kde=False):
        """Histogramme avec option KDE"""
        st.write(f"### Histogram of {column}")
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.histplot(self.df[column], bins=bins, kde=kde, ax=ax)
        st.pyplot(fig)

    def plot_boxplot(self, x, y=None):
        """Boxplot pour analyser la distribution des données"""
        st.write(f"### Boxplot of {x} by {y}" if y else f"### Boxplot of {x}")
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.boxplot(x=x, y=y, data=self.df if y else self.df[[x]], ax=ax)
        st.pyplot(fig)

    def plot_scatter(self, x, y, color=None, size=None):
        """Graphique de dispersion"""
        st.write(f"### Scatter plot between {x} & {y}")
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.scatterplot(x=x, y=y, hue=color, size=size, data=self.df, ax=ax)
        st.pyplot(fig)

    def plot_pairplot(self, hue=None, palette="viridis"):
        """Pairplot des variables numériques"""
        st.write("### Pairplot")
        numeric_df = self.df.select_dtypes(include=["number"])
        fig = plt.subplots(figsize=(10, 8))
        sns.pairplot(numeric_df, hue=hue, palette=palette)
        st.pyplot(fig)

    def plot_correlation_heatmap(self):
        """Carte de chaleur des corrélations entre variables (interactive avec Plotly)"""
        st.write("### Correlation matrix")
        numeric_df = self.df.select_dtypes(include=["number"])
        corr_matrix = numeric_df.corr()
        fig = go.Figure(
            data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale="Viridis",
                zmin=-1,
                zmax=1,
                colorbar=dict(title="Correlation"),
                text=corr_matrix.round(2).values,
                texttemplate="%{text}",
                textfont=dict(color="black"),
                hoverinfo="text",
            )
        )
        fig.update_layout(
            xaxis_title="Variables",
            yaxis_title="Variables",
            xaxis=dict(
                tickmode="array",
                tickvals=list(range(len(corr_matrix.columns))),
                ticktext=corr_matrix.columns,
            ),
            yaxis=dict(
                tickmode="array",
                tickvals=list(range(len(corr_matrix.columns))),
                ticktext=corr_matrix.columns,
            ),
            autosize=True,
            height=800,
        )
        st.plotly_chart(fig)

    def plot_interactive_scatter(self, x, y, color=None, size=None):
        """Graphique de dispersion interactif avec Plotly"""
        st.write(f"### Scatter of {x} by {y}")
        fig = px.scatter(self.df, x=x, y=y, color=color, size=size)
        st.plotly_chart(fig)

    def plot_interactive_histogram(self, column, bins=20):
        """Histogramme interactif avec Plotly"""
        st.write(f"### Histogram of {column}")
        fig = px.histogram(self.df, x=column, nbins=bins)
        st.plotly_chart(fig)

    def plot_interactive_boxplot(self, x, y=None):
        """Boxplot interactif avec Plotly"""
        st.write(f"### Boxplot of {x} by {y}" if y else f"### Boxplot of {x}")
        fig = px.box(self.df, x=x, y=y)
        st.plotly_chart(fig)

    def plot_time_series(self, x, y):
        """Graphique de séries temporelles"""
        st.write(f"### Time series {y} in fonction of {x}")
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.lineplot(x=x, y=y, data=self.df, ax=ax)
        st.pyplot(fig)

    def summarize_data(self):
        """Affiche un résumé statistique des données"""
        st.write("### Statistical Summary")
        numeric_df = self.df.select_dtypes(include=["number"])
        st.write(numeric_df.describe())

    def missing_data(self):
        """Affiche un graphique de la quantité de données manquantes"""
        st.write("### Missing Data")
        missing_data = self.df.isnull().sum()
        st.write(missing_data)

    def plot_distplot(self, column, kde=True, bins=20):
        """Visualisation interactive de la distribution avec option KDE"""
        st.write(f"### Distribution of {column}")
        if kde:
            fig = px.histogram(
                self.df,
                x=column,
                nbins=bins,
                marginal="rug",
                title=f"Distribution of {column}",
            )
            fig.update_traces(marker=dict(line=dict(width=1, color="black")))
        else:
            fig = px.histogram(
                self.df, x=column, nbins=bins, title=f"Distribution of {column}"
            )
        st.plotly_chart(fig)

    def plot_ohlc(
        self, date_column, open_column, high_column, low_column, close_column
    ):
        """Affiche un graphique OHLC interactif"""
        st.write("### OHLC Chart")
        col1, col2 = st.columns([1, 1])
        with col1:
            protocol = st.selectbox(
                "Select a protocol", self.df["protocol_name"].unique()
            )
        with col2:
            frequency = st.selectbox(
                "Select a frequency", ["1YE", "1ME", "1D", "12h", "1h"]
            )
        df = self.df[self.df["protocol_name"] == protocol]

        if not all(
            col in df.columns
            for col in [date_column, open_column, high_column, low_column, close_column]
        ):
            st.write(
                f"Following colonnes missing into DataFrame: "
                f"{', '.join([col for col in [date_column, open_column, high_column, low_column, close_column] if col not in self.df.columns])}"
            )
            return
        df_resampled = (
            self.df.resample(frequency, on=date_column)
            .agg(
                {
                    open_column: "median",
                    high_column: "median",
                    low_column: "median",
                    close_column: "median",
                }
            )
            .dropna()
        )
        fig = go.Figure(
            data=[
                go.Ohlc(
                    x=df_resampled.index,
                    open=df_resampled[open_column],
                    high=df_resampled[high_column],
                    low=df_resampled[low_column],
                    close=df_resampled[close_column],
                )
            ]
        )
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Price",
            xaxis_rangeslider_visible=False,
            template="plotly_dark",
            autosize=True,
            height=600,
        )
        st.plotly_chart(fig)
