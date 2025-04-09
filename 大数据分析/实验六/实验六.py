"""
PySpark基础操作实验
功能：
1. 读取文本文件并基础操作
2. 实现单词计数
3. 演示缓存机制
4. 构建完整Spark应用
"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import os


def basic_operations(spark):
    """基础Spark操作演示"""
    print("\n=== 基础操作演示 ===")

    # 读取文本文件
    text_file = spark.read.text("README.md")

    # 基础操作
    print(f"文件总行数: {text_file.count()}")
    print(f"第一行内容: {text_file.first()}")

    # 过滤操作
    lines_with_spark = text_file.filter(text_file.value.contains("Spark"))
    print(f"包含'Spark'的行数: {lines_with_spark.count()}")


def word_count(spark):
    """单词计数实现"""
    print("\n=== 单词计数实现 ===")

    text_file = spark.read.text("README.md")

    # 单词计数
    word_counts = text_file.select(
        F.explode(F.split(text_file.value, "\s+")).alias("word")
    ).groupBy("word").count()

    # 显示结果
    print("出现频率最高的10个单词:")
    word_counts.orderBy("count", ascending=False).show(10)


def caching_demo(spark):
    """缓存机制演示"""
    print("\n=== 缓存机制演示 ===")

    text_file = spark.read.text("README.md")
    lines_with_spark = text_file.filter(text_file.value.contains("Spark"))

    # 缓存DataFrame
    lines_with_spark.cache()

    # 第一次操作会计算并缓存
    start_time = time.time()
    print(f"第一次计数: {lines_with_spark.count()}")
    print(f"耗时: {time.time() - start_time:.4f}秒")

    # 第二次操作直接从缓存读取
    start_time = time.time()
    print(f"第二次计数: {lines_with_spark.count()}")
    print(f"耗时: {time.time() - start_time:.4f}秒")


class SimpleApp:
    """完整的Spark应用示例"""

    def __init__(self, file_path):
        self.file_path = file_path
        self.spark = SparkSession.builder.appName("SimpleApp").getOrCreate()

    def run(self):
        """运行应用"""
        try:
            log_data = self.spark.read.text(self.file_path).cache()

            num_as = log_data.filter(log_data.value.contains('a')).count()
            num_bs = log_data.filter(log_data.value.contains('b')).count()

            print(f"\n=== 应用执行结果 ===")
            print(f"包含a的行数: {num_as}")
            print(f"包含b的行数: {num_bs}")
        finally:
            self.spark.stop()


if __name__ == "__main__":
    import time

    # 初始化SparkSession
    spark = SparkSession.builder \
        .appName("PySparkDemo") \
        .getOrCreate()

    try:
        # 执行各个实验部分
        basic_operations(spark)
        word_count(spark)
        caching_demo(spark)

        # 运行完整应用
        app = SimpleApp("README.md")
        app.run()

    finally:
        spark.stop()
        print("\nSpark会话已终止")