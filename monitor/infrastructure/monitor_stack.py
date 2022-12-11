from aws_cdk import (
    # Duration,
    Stack,
    aws_apigateway as apigw,
    aws_lambda as lambda_,
    aws_lambda_python_alpha as pylambda,
    aws_route53 as r53,
    aws_iam as iam
)

from constructs import Construct

HOSTED_ZONE_ID: str = "Z02204627UX1LNXVIRPB"

class MonitorStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        hosted_zone = r53.HostedZone.from_hosted_zone_id(self, "server-hzone", HOSTED_ZONE_ID)

        monitor_function = pylambda.PythonFunction(
            self, "monitor-function",
            function_name="monitor-function",
            entry="app",
            index="monitor.py",
            architecture=lambda_.Architecture.ARM_64,
            runtime=lambda_.Runtime.PYTHON_3_9
        )

        api = apigw.RestApi(
            self, "pulse-api",
        )