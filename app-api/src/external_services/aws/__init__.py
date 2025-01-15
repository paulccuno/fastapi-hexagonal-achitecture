from src.external_services.aws.api.aws_dynamodb import AwsDynamoDB
from src.external_services.aws.api.aws_s3 import AwsS3


class Aws:

    aws_dynamodb: AwsDynamoDB
    aws_s3: AwsS3

    def __init__(
        self,
        aws_dynamodb: AwsDynamoDB,
        aws_s3: AwsS3,
    ) -> None:
        self.aws_dynamodb = aws_dynamodb
        self.aws_s3 = aws_s3
