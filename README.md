# DynamoDB Enhanced Client Java Bean Generator

This tool is a Python script that generates Java Bean source code for use with the AWS
DynamoDB Enhanced Client based on a given DynamoDB table schema.

## Installation

Install the required Python packages for running this tool:

```bash
pip install -r requirements.txt
```

Additionally, this tool provides an example that processes a list of DynamoDB tables
using `aws-cli` and `jq`. Install them as needed.

## Usage

### Simple Usage

```bash
python main.py <table_name>
```

This command generates Java Bean source code based on the schema of the specified
DynamoDB table.

### Batch Output Example

```bash
aws dynamodb list-tables | jq -r '.TableNames[]' | xargs -I {} sh -c 'echo "Processing table: {}"; python main.py "{}" > "out/{}.java"; echo "Saved to {}.java"'
```

This one-liner uses `aws-cli` and `jq` to obtain a list of DynamoDB tables, then calls
`main.py` multiple times with `xargs` to generate Java code for each table, and saves
the Java code to a file named `out/<table_name>.java`.

## About the Template File

The `dynamodb_bean_template.j2` file is a template file used by the Jinja2 template engine
to generate Java Bean source code. By editing this file, you can customize the structure
and style of the generated Java code.
