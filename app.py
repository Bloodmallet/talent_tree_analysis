# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import json
import typing
from components.bargraph import generate_bar_graph
from components.filters import (
    get_investable_talent_points,
    get_post_20_gate_talent_points,
    get_pre_20_gate_talent_points,
    get_pre_8_gate_talent_points,
    get_unique_talents,
    get_choice_nodes,
    get_active_abilities,
    get_single_point_talents,
    get_avg_node_size,
    get_three_rankers,
    get_active_abilities_pre_8_gate,
    get_active_abilities_pre_20_gate,
    get_active_abilities_post_20_gate,
)

TALENT_JSON_PATH = r"data/talents.json"


def load_data() -> typing.Dict[str, typing.Dict]:
    with open(TALENT_JSON_PATH, "r") as f:
        raw_data = json.load(f)

    color_map = {
        "death knight": "#c41f3b",
        "demon hunter": "#a330c9",
        "druid": "#ff7d0a",
        "evoker": "#33937F",
        "hunter": "#abd473",
        "mage": "#69ccf0",
        "monk": "#00ff96",
        "paladin": "#f58cba",
        "priest": "#ffffff",
        "rogue": "#fff569",
        "shaman": "#0070de",
        "warlock": "#9482c9",
        "warrior": "#c79c6e",
    }

    data = {}
    for tree in raw_data:
        combined_name = f"{tree['className']} {tree['specName']}"
        data[combined_name] = tree
        data[combined_name]["color"] = color_map[tree["className"].lower()]

    return data


def main():
    app = Dash(
        __name__, title="Talent Tree Analysis", external_stylesheets=[dbc.themes.SLATE]
    )

    data = load_data()

    data_extractors = [
        get_investable_talent_points,
        get_unique_talents,
        get_single_point_talents,
        get_avg_node_size,
        get_pre_8_gate_talent_points,
        get_pre_20_gate_talent_points,
        get_post_20_gate_talent_points,
        get_choice_nodes,
        get_active_abilities,
        get_three_rankers,
        get_active_abilities_pre_8_gate,
        get_active_abilities_pre_20_gate,
        get_active_abilities_post_20_gate,
    ]

    spec_graphs = [
        dcc.Graph(
            id=extractor.__name__ + "specNodes",
            figure=generate_bar_graph(extractor(data, "specNodes")),
            className="col",
        )
        for extractor in data_extractors
    ]
    class_graphs = [
        dcc.Graph(
            id=extractor.__name__ + "classNodes",
            figure=generate_bar_graph(extractor(data, "classNodes")),
            className="col",
        )
        for extractor in data_extractors
    ]

    app.layout = html.Div(
        children=[
            html.H1(children="Talent Tree Analysis"),
            html.H2(children="Class Trees"),
            html.Div(
                className="container",
                children=[
                    html.Div(
                        className="row",
                        children=class_graphs,
                    )
                ],
            ),
            html.H2(children="Spec Trees"),
            html.Div(
                className="container",
                children=[
                    html.Div(
                        className="row",
                        children=spec_graphs,
                    )
                ],
            ),
        ]
    )
    app.run_server(debug=True)


if __name__ == "__main__":
    main()
