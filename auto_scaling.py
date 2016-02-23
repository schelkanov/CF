from troposphere import Base64, Join
from troposphere import Parameter, Ref, Template
from troposphere import cloudformation, autoscaling
from troposphere.autoscaling import AutoScalingGroup, Tag
from troposphere.autoscaling import LaunchConfiguration
from troposphere.elasticloadbalancing import LoadBalancer
from troposphere.policies import UpdatePolicy, AutoScalingRollingUpdate
import troposphere.ec2 as ec2
import troposphere.elasticloadbalancing as elb



template = Template()

template.add_description("""\
Configures autoscaling group for ILevel Project""")

security_groups = [template.add_resource(ec2.SecurityGroup(
    "WEB",
     GroupDescription='For WEB servers',
     SecurityGroupIngress=[{'CidrIp': '0.0.0.0/0',
                                  'FromPort': '22',
                                  'IpProtocol': 'tcp',
                                  'ToPort': '22'},
                                 {'CidrIp': '0.0.0.0/0',
                                  'FromPort': '80',
                                  'IpProtocol': 'tcp',
                                  'ToPort': '80'}],
                           )),
     template.add_resource(ec2.SecurityGroup(
     "DB",
     GroupDescription='For Database servers',
     SecurityGroupIngress=[{'CidrIp': '0.0.0.0/0',
                                  'FromPort': '22',
                                  'IpProtocol': 'tcp',
                                  'ToPort': '22'},
                                 {'CidrIp': '0.0.0.0/0',
                                  'FromPort': '80',
                                  'IpProtocol': 'tcp',
                                  'ToPort': '80'}],
                           )),
     template.add_resource(ec2.SecurityGroup(
     "Private",
     GroupDescription='For Workflow(Private) servers',
     SecurityGroupIngress=[{'CidrIp': '0.0.0.0/0',
                                  'FromPort': '22',
                                  'IpProtocol': 'tcp',
                                  'ToPort': '22'},
                                 {'CidrIp': '0.0.0.0/0',
                                  'FromPort': '80',
                                  'IpProtocol': 'tcp',
                                  'ToPort': '80'}],
                           )),
    template.add_resource(ec2.SecurityGroup(
     "Calculation",
     GroupDescription='For Calculation servers',
     SecurityGroupIngress=[{'CidrIp': '0.0.0.0/0',
                                  'FromPort': '22',
                                  'IpProtocol': 'tcp',
                                  'ToPort': '22'},
                                 {'CidrIp': '0.0.0.0/0',
                                  'FromPort': '80',
                                  'IpProtocol': 'tcp',
                                  'ToPort': '80'}],
                           )),]


