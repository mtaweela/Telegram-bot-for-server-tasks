"""
ref:
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.stop_instances
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html
"""

import boto3


class Ec2Servers:
    def __init__(self, instance_dict):
        self.instance_dict = instance_dict

    @property
    def ec2(self):
        SCOUT_ACCESS_KEY = self.instance_dict.get("access_key")
        SCOUT_SECRET_KEY = self.instance_dict.get("secret_key")

        return boto3.client(
            "ec2",
            aws_access_key_id=SCOUT_ACCESS_KEY,
            aws_secret_access_key=SCOUT_SECRET_KEY,
            region_name=self.instance_dict.get("region"),
        )

    def reboot(self):
        try:
            return self.ec2.reboot_instances(
                InstanceIds=[
                    self.instance_dict.get("id")
                ],
                DryRun=False,
            )
        except Exception as e:
            return e

    def stop(self):
        try:
            return self.ec2.stop_instances(
                InstanceIds=[
                    self.instance_dict.get("id")
                ],
                DryRun=False,
            )
        except Exception as e:
            return e

    def start(self):
        try:
            return self.ec2.start_instances(
                InstanceIds=[
                    self.instance_dict.get("id")
                ],
                DryRun=False,
            )
        except Exception as e:
            return e
