#!/usr/bin/bash

# This post-hook script tags already created DynamoDB tables
# http://docs.aws.amazon.com/cli/latest/reference/dynamodb/tag-resource.html

set -xe

if [ -z "${DYNAMODB_PREFIX}" ]; then
    echo "DYNAMODB_PREFIX was not set - not tagging resources"
    exit 0
fi

# Let's give the gremlin-server some time to create the tables, we don't hurry
sleep 10

# Get $DYNAMODB_PREFIX prefixed tables
# The aws output looks like:
# ||  someprefix_edgestore                        ||
# ||  someprefix_graphindex                       ||
# ||  someprefix_system_properties                ||
# ||  someprefix_systemlog                        ||
# ||  someprefix_titan_ids                        ||
# ||  someprefix_txlog                            ||
# so the grep checks whether there's also a white-space (on left) and _ (on right)
TABLES=$(aws dynamodb list-tables --output=table | grep " ${DYNAMODB_PREFIX}_" | awk '{print $2}')

for TABLE_NAME in ${TABLES}
do
    # Get Amazon Resource Name (ARN) of the table
    TABLE_ARN=$(aws dynamodb describe-table --output=table --table-name "${TABLE_NAME}" | grep -w TableArn | awk '{print $4}')
    if [ -n "${TABLE_ARN}" ]; then
        # Tag table with ENV:$DYNAMODB_PREFIX
        aws dynamodb tag-resource --resource-arn "${TABLE_ARN}" --tags "Key=ENV,Value=${DYNAMODB_PREFIX}"
        # List tags (for debugging)
        aws dynamodb list-tags-of-resource --resource-arn "${TABLE_ARN}"
    fi
done
