from pyecharts.charts import Sunburst
from pyecharts import options as opts


new_data = {
    '特医婴配食品': {'进口产品': 24, '国产产品': 27},
    '1岁以上特医食品': {'国产产品': 124, '进口产品': 7}
}


colors = [
    "#FFB6C1", "#FF69B4", "#DB7093", "#FF1493", "#C71585",
    "#DA70D6", "#D8BFD8", "#DDA0DD", "#EE82EE", "#FF00FF"
]


def convert_data(data, colors):
    color_index = 0
    items = []
    for key, value in data.items():
        children = [
            {
                "name": f"{k} ({v})",
                "value": v,
                "itemStyle": {"color": colors[color_index % len(colors)]}
            }
            for k, v in value.items()
        ]
        items.append({
            "name": key,
            "children": children,
            "itemStyle": {"color": colors[color_index % len(colors)]}
        })
        color_index += 1
    return items

converted_data = convert_data(new_data, colors)


c = (
    Sunburst(init_opts=opts.InitOpts(width="1000px", height="600px"))
    .add(
        "",
        data_pair=converted_data,
        highlight_policy="ancestor",
        radius=[0, "95%"],
        sort_="null",
        levels=[
            {},
            {
                "r0": "15%",
                "r": "35%",
                "itemStyle": {"borderWidth": 2},
                "label": {"rotate": "tangential"},
            },
            {
                "r0": "35%",
                "r": "70%",
                "label": {"align": "right"},
                "itemStyle": {"borderWidth": 1},
            },
            {
                "r0": "70%",
                "r": "72%",
                "label": {"position": "outside", "padding": 3, "silent": False},
                "itemStyle": {"borderWidth": 3},
            },
        ],
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Sunburst-特医食品示例")
    )
    .set_series_opts(
        label_opts=opts.LabelOpts(formatter="{b} - {c}")
    )
    .render("special_medical_food_sunburst.html")
)