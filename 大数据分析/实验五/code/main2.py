# -*- coding: utf-8 -*-
# 使用基于IBCF算法对电影进行推荐
from __future__ import print_function
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def item_based_recommend(train_df, test_df, n_recommendations=5):
    """
    基于物品的协同过滤推荐
    :param train_df: 训练集评分矩阵
    :param test_df: 测试集评分矩阵
    :param n_recommendations: 推荐数量
    :return: 推荐结果DataFrame
    """
    # 计算物品相似度矩阵（余弦相似度）
    item_sim = cosine_similarity(train_df.T.fillna(0))
    item_sim_df = pd.DataFrame(item_sim, index=train_df.columns, columns=train_df.columns)

    # 为每个用户生成推荐
    recommendations = {}
    for user in test_df.index:
        # 获取用户已评分的电影（在训练集中）
        rated_items = train_df.loc[user].dropna().index if user in train_df.index else []

        # 获取用户未评分的电影（在测试集中）
        unrated_items = [item for item in test_df.columns if pd.isna(test_df.loc[user, item])]

        pred_ratings = []
        for item in unrated_items:
            if item in item_sim_df.columns:
                # 找到与当前物品最相似的已评分物品
                sim_items = item_sim_df[item][rated_items]
                sim_items = sim_items[sim_items > 0]  # 只考虑正相似度

                if len(sim_items) > 0:
                    # 加权平均预测评分
                    user_ratings = train_df.loc[user][sim_items.index]
                    weighted_sum = (user_ratings * sim_items).sum()
                    sum_of_weights = sim_items.sum()
                    pred_rating = weighted_sum / (sum_of_weights + 1e-8)  # 防止除以零
                    pred_ratings.append((item, pred_rating))

        # 按预测评分排序并取前n个推荐
        pred_ratings.sort(key=lambda x: x[1], reverse=True)
        recommendations[user] = [item for item, _ in pred_ratings[:n_recommendations]]

    return pd.DataFrame.from_dict(recommendations, orient='index')


############    主程序   ##############
if __name__ == "__main__":
    print("\n--------------使用基于IBCF算法对电影进行推荐 运行中... -----------\n")

    # 读取数据
    traindata = pd.read_csv('../data/u1.base', sep='\t', header=None, index_col=None)
    testdata = pd.read_csv('../data/u1.test', sep='\t', header=None, index_col=None)

    # 删除时间标签列
    traindata.drop(3, axis=1, inplace=True)
    testdata.drop(3, axis=1, inplace=True)

    # 行与列重新命名
    traindata.rename(columns={0: 'userid', 1: 'movid', 2: 'rat'}, inplace=True)
    testdata.rename(columns={0: 'userid', 1: 'movid', 2: 'rat'}, inplace=True)

    # 创建评分矩阵
    traindf = traindata.pivot(index='userid', columns='movid', values='rat')
    testdf = testdata.pivot(index='userid', columns='movid', values='rat')

    # 重命名行列
    traindf.rename(index={i: 'usr%d' % (i) for i in traindf.index}, inplace=True)
    traindf.rename(columns={i: 'mov%d' % (i) for i in traindf.columns}, inplace=True)
    testdf.rename(index={i: 'usr%d' % (i) for i in testdf.index}, inplace=True)
    testdf.rename(columns={i: 'mov%d' % (i) for i in testdf.columns}, inplace=True)

    # 获取基于物品的推荐
    recomm_df = item_based_recommend(traindf, testdf, n_recommendations=5)

    # 打印推荐结果
    print("\n推荐结果示例:")
    print(recomm_df.head())  # 显示前5个用户的推荐结果