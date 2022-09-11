import pandas
import plotly
import plotly.express as px


def generate_bar_graph(data: pandas.DataFrame) -> plotly.graph_objs.Figure:
    if data.shape[1] != 3:
        raise ValueError("Bar graph expects 3 columns.")

    spec_column_name = "Spec"
    if spec_column_name not in data.columns:
        raise ValueError(f"One of the Columns needs to be called '{spec_column_name}'.")

    color_column_name = "color"
    if color_column_name not in data.columns:
        raise ValueError(
            f"One of the Columns needs to be called '{color_column_name}'."
        )

    data_column_name = [
        c for c in data.columns if c not in (spec_column_name, color_column_name)
    ][0]
    height = len(data.index) * 21

    sorted_data = data.sort_values([data_column_name], axis=0)

    bar = px.bar(
        # data_frame=sorted_data,
        title=data_column_name,
        y=sorted_data[spec_column_name],
        x=sorted_data[data_column_name],
        orientation="h",
        width=500,
        height=height,
        text=sorted_data[data_column_name],
    )
    bar.update_traces(
        textfont_size=50,
        textangle=0,
        textposition="outside",
        cliponaxis=False,
        marker={"color": sorted_data[color_column_name]},
    )
    bar.update_layout(
        uniformtext_minsize=40,
        # uniformtext_mode="hide",
        paper_bgcolor="rgb(0,0,0,0)",
        plot_bgcolor="rgb(0,0,0,0)",
        font_color="#aaa",
        yaxis={"title": None},
        xaxis={"title": None},
    )

    return bar
