import typing
import pandas


def _get_df(data: dict) -> pandas.DataFrame:
    return pandas.DataFrame(
        {
            "Spec": data.keys(),
            "color": [c["color"] for c in data.values()],
        }
    )


def sum_filter_spec_nodes(
    data: dict, node_type: str, check: typing.Callable[..., bool]
) -> typing.List[int]:
    return [
        sum(node["maxRanks"] for node in v[node_type] if check(node))
        for v in data.values()
    ]


def get_investable_talent_points(data: dict, node_type: str) -> pandas.DataFrame:
    df = _get_df(data)
    df["Number of investable talent points"] = sum_filter_spec_nodes(
        data, node_type, any
    )

    return df


def get_pre_8_gate_talent_points(data: dict, node_type: str) -> pandas.DataFrame:
    df = _get_df(data)
    df["Number of pre-8-gate talent points"] = sum_filter_spec_nodes(
        data, node_type, lambda node: node.get("reqPoints", 0) == 0
    )

    return df


def get_pre_20_gate_talent_points(data: dict, node_type: str) -> pandas.DataFrame:
    df = _get_df(data)
    df["Number of pre-20-gate talent points"] = sum_filter_spec_nodes(
        data, node_type, lambda node: 0 <= node.get("reqPoints", 0) < 20
    )

    return df


def get_post_20_gate_talent_points(data: dict, node_type: str) -> pandas.DataFrame:
    df = _get_df(data)
    df["Number of post-20-gate talent points"] = sum_filter_spec_nodes(
        data, node_type, lambda node: 20 <= node.get("reqPoints", 0)
    )

    return df


def get_unique_talents(data: dict, node_type: str) -> pandas.DataFrame:
    df = _get_df(data)
    df["Number of unique talents"] = [len(v[node_type]) for v in data.values()]

    return df


def get_choice_nodes(data: dict, node_type: str) -> pandas.DataFrame:
    df = _get_df(data)
    df["Number of choice nodes"] = [
        len([n for n in v[node_type] if len(n["entries"]) > 1]) for v in data.values()
    ]

    return df


def get_active_abilities(data: dict, node_type: str) -> pandas.DataFrame:
    df = _get_df(data)
    df["Number of additional active abilities"] = [
        len(
            [
                n
                for n in v[node_type]
                if any([entry["type"] == "active" for entry in n["entries"]])
            ]
        )
        for v in data.values()
    ]

    return df


def get_single_point_talents(data: dict, node_type: str) -> pandas.DataFrame:
    df = _get_df(data)
    df["Number of single point nodes"] = [
        len([n for n in v[node_type] if n["maxRanks"] == 1]) for v in data.values()
    ]

    return df


def get_avg_node_size(data: dict, node_type: str) -> pandas.DataFrame:
    df = _get_df(data)
    df["Average node size"] = [
        sum(node["maxRanks"] for node in v[node_type]) / len(v[node_type])
        for v in data.values()
    ]

    return df


def get_three_rankers(data: dict, node_type: str) -> pandas.DataFrame:
    df = _get_df(data)
    df["Number of nodes with three ranks"] = [
        len([node for node in v[node_type] if node["maxRanks"] >= 3])
        for v in data.values()
    ]

    return df


def get_active_abilities_pre_8_gate(data: dict, node_type: str) -> pandas.DataFrame:
    df = _get_df(data)
    df["Number of active abilities pre-8-gate"] = [
        len(
            [
                n
                for n in v[node_type]
                if any([entry["type"] == "active" for entry in n["entries"]])
                and n.get("reqPoints", 0) < 8
            ]
        )
        for v in data.values()
    ]

    return df


def get_active_abilities_pre_20_gate(data: dict, node_type: str) -> pandas.DataFrame:
    df = _get_df(data)
    df["Number of active abilities pre-20-gate"] = [
        len(
            [
                n
                for n in v[node_type]
                if any([entry["type"] == "active" for entry in n["entries"]])
                and 8 <= n.get("reqPoints", 0) < 20
            ]
        )
        for v in data.values()
    ]

    return df


def get_active_abilities_post_20_gate(data: dict, node_type: str) -> pandas.DataFrame:
    df = _get_df(data)
    df["Number of active abilities post-20-gate"] = [
        len(
            [
                n
                for n in v[node_type]
                if any([entry["type"] == "active" for entry in n["entries"]])
                and 20 <= n.get("reqPoints", 0)
            ]
        )
        for v in data.values()
    ]

    return df
