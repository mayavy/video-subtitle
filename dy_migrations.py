from datetime import datetime, timezone
import boto3
from project.settings import dynamodb, DEBUG, DB_TABLE_NAME


def create_table(dynamodb=dynamodb):
    """
    Creates AWS dynamodb table.
    """
    table = dynamodb.create_table(
        TableName=DB_TABLE_NAME,
        KeySchema=[
            {'AttributeName': 'word', 'KeyType': 'HASH'},  # Partition key
            {'AttributeName': 'video_id', 'KeyType': 'RANGE'}  # Sort key
        ],
        AttributeDefinitions=[
            {'AttributeName': 'word', 'AttributeType': 'S'},
            {'AttributeName': 'video_id', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )
    return table


if __name__ == '__main__':
    my_table = create_table()
    my_table.wait_until_exists()
    my_table.meta.client.get_waiter(
        'table_exists').wait(TableName=DB_TABLE_NAME)
    print("Table status:", my_table.table_status)
    if DEBUG:
        # dummy entry
        my_table.put_item(
            Item={
                'word': 'word',
                'uploaded_by': datetime.now(timezone.utc).strftime(r"%d/%m/%Y, %H:%M:%S"),
                'video_id': 'video_|_name',
                            'ranges': [('00:00:00,5', '11:25:55,5'), ('00:40:00,5', '11:25:5,5')]})
    print(my_table.item_count)
