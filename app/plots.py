import plotly.graph_objects as go


def return_figures(df):
    """Create Plotly figures object"""

    genres_plot = []
    genres_plot.append(
        go.Bar(
            x=df.genre.value_counts().index.tolist(),
            y=df.genre.value_counts().values.tolist(),
            hoverinfo="skip",
            marker_color="#BB764B",
        )
    )

    genres_layout = dict(
        {
            "title": {
                "text": "<b>Majority of messages come directly or via "
                "news</b><br>Small percentage of the data comes"
                " from social",
                "font": {"family": "Roboto", "size": 16},
            },
        }
    )

    label_tallies = df.iloc[:, 4:].sum().sort_values(ascending=True)
    label_plot = []
    label_plot.append(
        go.Bar(
            x=label_tallies.values.tolist(),
            y=label_tallies.index.tolist(),
            orientation="h",
            marker_color="#BB764B",
        )
    )

    label_layout = dict(
        {
            "title": {
                "text": "<b>Not all messages are relevant"
                "</b><br>75% of messages labelled <i>related</i> to mean"
                " relevant",
                "font": {"family": "Roboto", "size": 16},
            },
            "margin": {
                "pad": 10,
                "l": 140,
                "r": 40,
                "t": 80,
                "b": 40,
            },
            "hoverlabel": {
                "font_size": 18,
                "font_family": "Roboto",
            },
            "yaxis": {"dtick": 1},
        }
    )

    figures = []
    figures.append(dict(data=genres_plot, layout=genres_layout))
    figures.append(dict(data=label_plot, layout=label_layout))

    return figures
