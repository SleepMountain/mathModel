from pyecharts.charts import WordCloud
from pyecharts import options as opts

data = [
    ("早产/低出生体重婴儿", 17),
    ("乳蛋白过敏高风险婴儿", 11),
    ("乳糖不耐受婴儿", 11),
    ("进食受限", 29),
    ("消化吸收障碍", 29),
    ("代谢紊乱", 29),
    ("补充营养", 29),
    ("腹泻", 7),
    ("脱水", 7),
    ("补充电解质", 7),
    ("术前", 6),
    ("补充碳水化合物", 6),
    ("补充蛋白质", 16),
    ("吞咽障碍", 3),
    ("误吸风险", 3),
    ("限制脂肪摄入", 3),
    ("食物蛋白过敏婴儿", 5),
    ("苯丙酮尿症婴儿", 2),
    ("苯丙酮尿症人群", 1),
    ("营养风险", 1),
    ("营养不良", 1),
    ("肿瘤患者", 1),
    ("因腹泻", 1),
    ("中链脂肪", 1),
    ("术前补充碳水化合物", 2),
    ("术前补充碳水化合物和电解质", 6),
    ("10岁以上", 29),
    ("1～10岁", 5),
    ("18岁以上", 2),
    ("1岁以上", 2),
    ("50岁以上", 1),
    ("10～14岁", 1),
    ("1～14岁", 1)
]

wordcloud = (
    WordCloud()
    .add(series_name="热点分析", data_pair=data, word_size_range=[6, 66])
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="热点分析",
            title_textstyle_opts=opts.TextStyleOpts(font_size=23)
        ),
        tooltip_opts=opts.TooltipOpts(is_show=True),
    )
)

wordcloud.render("basic_wordcloud.html")

print("词云图已生成并保存为 basic_wordcloud.html")