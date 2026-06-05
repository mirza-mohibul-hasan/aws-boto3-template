from app.core.aws_session import get_boto3_session
from app.core.config import get_aws_config


class AutoScalingService:
    def __init__(self):
        session = get_boto3_session()
        self.client = session.client("autoscaling")
        self.config = get_aws_config()

    def get_asg_status(self):
        response = self.client.describe_auto_scaling_groups(
            AutoScalingGroupNames=[self.config.gpu_asg_name]
        )

        if not response["AutoScalingGroups"]:
            raise Exception("ASG not found")

        asg = response["AutoScalingGroups"][0]

        return {
            "name": asg["AutoScalingGroupName"],
            "desired_capacity": asg["DesiredCapacity"],
            "min_size": asg["MinSize"],
            "max_size": asg["MaxSize"],
            "instances": len(asg["Instances"]),
        }

    def start_gpu(self, desired_capacity: int = 1):
        return self.client.update_auto_scaling_group(
            AutoScalingGroupName=self.config.gpu_asg_name,
            MinSize=desired_capacity,
            DesiredCapacity=desired_capacity,
        )

    def stop_gpu(self):
        return self.client.update_auto_scaling_group(
            AutoScalingGroupName=self.config.gpu_asg_name,
            MinSize=0,
            DesiredCapacity=0,
        )
