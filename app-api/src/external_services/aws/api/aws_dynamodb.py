from botocore.exceptions import ClientError
from logging import Logger
from src.config import Settings
from src.external_services.aws.api.aws_session import AwsSession


class AwsDynamoDB:

    aws_session: AwsSession
    settings: Settings
    logger: Logger
    resource: object
    client: object

    def __init__(self, aws_session: AwsSession, settings: Settings, logger: Logger) -> None:
        self.aws_session = aws_session
        self.settings = settings
        self.logger = logger
        self.client = self.aws_session.client('dynamodb')
        self.resource = self.aws_session.resource('dynamodb')

    def get_all_rows_from_dynamodb(self, table_name: str, projection=None):
        try:
            # Retrieve the table
            table = self.resource.Table(table_name)

            scan_kwargs = {}
            if projection:
                if 'ALL' not in projection:
                    expression_attribute_names = {}
                    projection_expression = []
                    for attribute in projection:
                        if attribute == "name":
                            placeholder = "#n"
                            expression_attribute_names[placeholder] = attribute
                            projection_expression.append(placeholder)
                        else:
                            projection_expression.append(attribute)

                    scan_kwargs['ProjectionExpression'] = ', '.join(
                        projection_expression)
                    if expression_attribute_names:
                        scan_kwargs['ExpressionAttributeNames'] = expression_attribute_names

            response = table.scan(**scan_kwargs)

            # List to hold the items
            items = response['Items']

            # Handle pagination
            while 'LastEvaluatedKey' in response:
                response = table.scan(
                    ExclusiveStartKey=response['LastEvaluatedKey'], **scan_kwargs)
                items.extend(response['Items'])

            return items

        except ClientError as e:
            # Check if the exception is due to the table not existing
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                return []
            else:
                raise e

    def get_item(self, table_name: str, partition_key_name: str, partition_key_value: str):
        # Access the DynamoDB table
        table = self.resource.Table(table_name)

        # Retrieve the item
        try:
            response = table.get_item(
                Key={
                    partition_key_name: partition_key_value
                }
            )
        except Exception as e:
            print(e)
            return None

        # Return the item if found, else return None
        return response.get('Item')
