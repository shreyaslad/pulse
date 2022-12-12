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

        # 1. Create health check for minecraft server
        # 2. Create REST API and Lambda function
        # 3. Reroute minecraft server to mc.shreyaslad.com
        # 4. Set REST API to api.mc.shreyaslad.com
        # 5. Set Grafana dashboard to mc.shreyaslad.com/insights
        # 6. Set web dashboard to admin.mc.shreyaslad.com

        hosted_zone = r53.HostedZone.from_hosted_zone_id(self, "server-hzone", HOSTED_ZONE_ID)

        monitor_function = pylambda.PythonFunction(
            self, "monitor-function",
            function_name="monitor-function",
            entry="app",
            index="monitor.py",
            architecture=lambda_.Architecture.ARM_64,
            runtime=lambda_.Runtime.PYTHON_3_9
        )

        discord_handler = pylambda.PythonFunction(
            self, "discord-handler-function"
        )

        api = apigw.RestApi(
            self, "pulse-discord-api",
            rest_api_name="pulse-discord-api"
        )

        event_resource = api.root.add_resource("/event")
        event_integration = apigw.LambdaIntegration(monitor_function)
        event_resource.add_method("POST", event_integration)
