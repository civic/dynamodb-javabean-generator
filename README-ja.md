# DynamoDB Enhanced Client Java Bean Generator

このツールは、AWS DynamoDBのテーブルスキーマをもとにDynamoDB Enhanced Client向けのJava Beanソースコードを生成するPythonスクリプトです。

## インストール方法

このツールの実行に必要なPythonパッケージをインストールします。

```bash
pip install -r requirements.txt
```

また、このツールは`aws-cli`と`jq`を使用してDynamoDBテーブルの一覧を処理する例があります。必要に応じてインストールしてください。

## 使用方法
### シンプルな使い方

```bash
python main.py <table_name>
```
このコマンドは、指定されたDynamoDBテーブルのスキーマに基づいてJava Beanソースコードを生成します。

### 一括出力する例
```bash
aws dynamodb list-tables | jq -r '.TableNames[]' | xargs -I {} sh -c 'echo "Processing table: {}"; python main.py "{}" > "out/{}.java"; echo "Saved to {}.java"'
```

このワンライナーは、`aws-cli`と`jq`を使用してDynamoDBテーブルの一覧を取得し、`xargs`を使って`main.py`を複数回呼び出して各テーブルに対してJavaコードを生成し、それぞれのJavaコードを`out/<テーブル名>.java`という名前のファイルに保存します。

## テンプレートファイルについて
`dynamodb_bean_template.j2`ファイルは、Jinja2テンプレートエンジンを使用してJava Beanソースコードを生成するためのテンプレートファイルです。このファイルを編集することで、生成されるJavaコードの構造やスタイルをカスタマイズできます。




