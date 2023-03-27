import sys
import boto3
from jinja2 import Environment, FileSystemLoader

def get_table_info(table_name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    table_info = table.meta.client.describe_table(TableName=table_name)
    return table_info

def analyze_table_info(table_info):
    attribute_definitions = table_info['Table']['AttributeDefinitions']
    key_schema = table_info['Table']['KeySchema']
    global_secondary_indexes = table_info['Table'].get('GlobalSecondaryIndexes', [])
    return attribute_definitions, key_schema, global_secondary_indexes

def attribute_type_to_java_type(attribute_type):
    if attribute_type == 'S':
        return 'String'
    elif attribute_type == 'N':
        return 'BigDecimal'
    elif attribute_type == 'B':
        return 'ByteBuffer'
    else:
        raise ValueError(f"Unsupported attribute type: {attribute_type}")




def create_attributes_map(attribute_definitions, key_schema, global_secondary_indexes):
    attributes_map = {}

    for attribute in attribute_definitions:
        attribute_name = attribute['AttributeName']
        attributes_map[attribute_name] = {
            'name': attribute_name,
            'type': attribute_type_to_java_type(attribute['AttributeType']),
            'is_primary_partition_key': False,
            'is_primary_sort_key': False,
            'is_gsi_partition_key': {},
            'is_gsi_sort_key': {}
        }

    for key in key_schema:
        attribute_name = key['AttributeName']
        if key['KeyType'] == 'HASH':
            attributes_map[attribute_name]['is_primary_partition_key'] = True
        elif key['KeyType'] == 'RANGE':
            attributes_map[attribute_name]['is_primary_sort_key'] = True

    for gsi in global_secondary_indexes:
        gsi_name = gsi['IndexName']
        gsi_partition_key = gsi['KeySchema'][0]['AttributeName']
        attributes_map[gsi_partition_key]['is_gsi_partition_key'][gsi_name] = True

        if len(gsi['KeySchema']) > 1:
            gsi_sort_key = gsi['KeySchema'][1]['AttributeName']
            attributes_map[gsi_sort_key]['is_gsi_sort_key'][gsi_name] = True

    return attributes_map.values()

def main(table_name):
    if len(sys.argv) != 2:
        print("Usage: python generate_dynamodb_bean.py <table_name>")
        sys.exit(1)

    table_name = sys.argv[1]

    table_info = get_table_info(table_name)
    attribute_definitions, key_schema, global_secondary_indexes = analyze_table_info(table_info)

    key_attributes = {key['AttributeName']: key['KeyType'] for key in key_schema}

    gsi_keys = {}
    for gsi in global_secondary_indexes:
        gsi_name = gsi['IndexName']
        for key in gsi['KeySchema']:
            if gsi_name not in gsi_keys:
                gsi_keys[gsi_name] = {}
            gsi_keys[gsi_name][key['AttributeName']] = key['KeyType']

    # 属性名と属性タイプをJavaの型に変換
    attributes = [
        {
            'name': attribute['AttributeName'],
            'type': attribute_type_to_java_type(attribute['AttributeType']),
            'is_hash_key': key_attributes.get(attribute['AttributeName']) == 'HASH',
            'is_sort_key': key_attributes.get(attribute['AttributeName']) == 'RANGE',
            'is_gsi_key': {gsi_name: gsi_key.get(attribute['AttributeName']) for gsi_name, gsi_key in gsi_keys.items()}
        }
        for attribute in attribute_definitions
    ]
    # テンプレートを読み込む
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('dynamodb_bean_template.j2')
    # テンプレートにデータを埋め込んでJavaコードを生成
    java_code = template.render(class_name=table_name, attributes=attributes)

    # 生成されたJavaコードを出力
    print(java_code)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_dynamodb_bean.py <table_name>")
        sys.exit(1)

    table_name = sys.argv[1]
    main(table_name)