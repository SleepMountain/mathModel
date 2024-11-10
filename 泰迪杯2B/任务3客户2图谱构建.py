from neo4j import GraphDatabase

def create_node(tx, label, properties):
    keys = ', '.join([f'{key}: "{value}"' for key, value in properties.items()])
    query = f'MERGE (n:{label} {{{keys}}})'
    tx.run(query)
    print(f"创建节点: {label} {properties}")

# 创建关系
def create_relationship(tx, start_label, start_key, end_label, end_key, relation_type):
    query = f'MATCH (a:{start_label} {{编号: "{start_key}"}}), (b:{end_label} {{编号: "{end_key}"}}) MERGE (a)-[:{relation_type}]->(b)'
    tx.run(query)
    print(f"创建关系: {start_label}({start_key}) -[{relation_type}]-> {end_label}({end_key})")

def clear_database(tx):
    query = "MATCH (n) DETACH DELETE n"
    tx.run(query)
    print("数据库已清空")

def build_knowledge_graph(driver, patient_data):
    with driver.session() as session:
        session.execute_write(clear_database)  # 清空数据库

        # 处理患者数据
        for patient_id, patient_info in patient_data.items():
            print(f"处理患者: {patient_id}")
            # 创建患者节点
            patient_properties = {
                '编号': patient_id,
                '健康状况': patient_info.get('健康状况', ''),
                '年龄': patient_info.get('年龄', ''),
                '性别': patient_info.get('性别', ''),
                '过敏史': patient_info.get('过敏史', ''),
            }
            session.execute_write(create_node, '患者', patient_properties)

# 主函数
def main():

    patient_data = {
        "2": {
            "健康状况": "需要补充蛋白质",
            "年龄": "10",
            "性别": None,
            "过敏史": "乳糖不耐受"
        }
    }

    uri = "bolt://localhost:7687"
    username = "neo4j"
    password = "czxczx3224039710"

    # 创建连接
    driver = GraphDatabase.driver(uri, auth=(username, password))
    print("连接到Neo4j数据库")

    try:
        build_knowledge_graph(driver, patient_data)
        print("知识图谱构建完成")
    finally:
        driver.close()
        print("关闭数据库连接")

if __name__ == '__main__':
    main()