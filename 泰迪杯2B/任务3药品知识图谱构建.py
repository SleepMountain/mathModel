import json
from neo4j import GraphDatabase

def load_data(file_path):
    print(f"加载数据文件: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    print("数据加载完成")
    return data

def create_node(tx, label, properties):
    keys = ', '.join([f'{key}: "{value}"' for key, value in properties.items()])
    query = f'MERGE (n:{label} {{{keys}}})'
    tx.run(query)
    print(f"创建节点: {label} {properties}")

def create_relationship(tx, start_label, start_key, end_label, end_key, relation_type):
    query = f'MATCH (a:{start_label} {{编号: "{start_key}"}}), (b:{end_label} {{名称: "{end_key}"}}) MERGE (a)-[:{relation_type}]->(b)'
    tx.run(query)
    print(f"创建关系: {start_label}({start_key}) -[{relation_type}]-> {end_label}({end_key})")



def clear_database(tx):
    query = "MATCH (n) DETACH DELETE n"
    tx.run(query)
    print("数据库已清空")


def build_knowledge_graph(driver, data):
    with driver.session() as session:
        session.execute_write(clear_database)  # 清空数据库

        for product_id, product_info in data.items():
            print(f"处理特医食品: {product_id} - {product_info['【名称】']}")

            food_properties = {
                '编号': product_id,
                '名称': product_info['【名称】'],
                '适用人群': product_info['【适用人群】'],
                '是否含有禁忌': '否' if not product_info.get('【禁忌】', '') else '是',
            }
            session.execute_write(create_node, '特医食品', food_properties)

            for nutrient, values in product_info['【营养成分表】'].items():
                nutrient_properties = {
                    '名称': nutrient,
                    '功能': ''
                }

                result = session.read_transaction(
                    lambda tx: tx.run(f"MATCH (n:营养成分 {{名称: '{nutrient}'}}) RETURN count(n)").single())
                if result[0] == 0:
                    session.execute_write(create_node, '营养成分', nutrient_properties)

                session.execute_write(create_relationship, '特医食品', product_id, '营养成分', nutrient, '包含')


def main():
    file_path = r'D:\桌面\竞赛\泰迪杯2\B\B题-特殊医学用途配方食品数据分析\文件\output.json'
    data = load_data(file_path)

    uri = "bolt://localhost:7687"
    username = "neo4j"  #
    password = "czxczx3224039710"

    driver = GraphDatabase.driver(uri, auth=(username, password))
    print("连接到Neo4j数据库")

    try:
        build_knowledge_graph(driver, data)
        print("知识图谱构建完成")
    finally:
        driver.close()
        print("关闭数据库连接")


if __name__ == '__main__':
    main()