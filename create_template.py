#!/usr/bin/python
from troposphere import Base64, FindInMap, GetAtt
from troposphere import Parameter, Output, Ref, Template
import troposphere.ec2 as ec2

web_servers = []
calculation_servers = []
private_servers = []
db_servers = []

template = Template()

template.add_description('This template for AWS Cloud Formation. Ilevel Project')

keyname_param = template.add_parameter(Parameter(
    "KeyName",
    Description="Name of an existing EC2 KeyPair to enable SSH "
                "access to the instance",
    Type="String",
))

template.add_mapping('RegionMap', {
    "us-west-2":      {"AMI": "ami-83a5bce2"},
})


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

web_servers = [template.add_resource(ec2.Instance(
    "Ec2InstanceWEB",
    ImageId=FindInMap("RegionMap", Ref("AWS::Region"), "AMI"),
    InstanceType="t1.micro",
    KeyName=Ref(keyname_param),
    SecurityGroups=[{'Ref': 'WEB'}],
    UserData=Base64("80")
))]


db_servers = [template.add_resource(ec2.Instance(
    "Ec2InstanceDB",
    ImageId=FindInMap("RegionMap", Ref("AWS::Region"), "AMI"),
    InstanceType="t1.micro",
    KeyName=Ref(keyname_param),
    SecurityGroups=[{'Ref': 'DB'}],
    UserData=Base64("80")
))]

calculation_servers = [template.add_resource(ec2.Instance(
    "Ec2InstanceCalculation",
    ImageId=FindInMap("RegionMap", Ref("AWS::Region"), "AMI"),
    InstanceType="t1.micro",
    KeyName=Ref(keyname_param),
    SecurityGroups=[{'Ref': 'Calculation'}],
    UserData=Base64("80")
)),]

private_servers = [ template.add_resource(ec2.Instance(
    "Ec2InstansePrivate1",
    ImageId=FindInMap("RegionMap", Ref("AWS::Region"), "AMI"),
    InstanceType="t1.micro",
    KeyName=Ref(keyname_param),
    SecurityGroups=[{'Ref': 'Private'}],
    UserData=Base64("80")
)),
  template.add_resource(ec2.Instance(
    "Ec2InstansePrivate2",
    ImageId=FindInMap("RegionMap", Ref("AWS::Region"), "AMI"),
    InstanceType="t1.micro",
    KeyName=Ref(keyname_param),
    SecurityGroups=[{'Ref': 'Private'}],
    UserData=Base64("80")
)),
  
 ]

"""
template.add_output([
    Output(
        "WebServers",
        Description="InstanceIds of created web servers",
        Value=Ref(web_servers),
    ),
    Output(
        "DBServers",
        Description="InstanceIds of created DB servers",
        Value=Ref(db_servers),
    ),
    Output(
        "CalculationServers",
        Description="InstanceIds of created Calculation servers",
        Value=Ref(calculation_servers),
    ),
    Output(
        "PrivateServers",
        Description="InstanceIds of created Private servers",
        Value=Ref(private_servers),
    ),
    Output(
        "AZ",
        Description="Availability Zone of the newly created EC2 instances",
        Value=GetAtt([web_servers,db_servers,calculation_servers,private_servers], "AvailabilityZone"),
    ),
    Output(
        "PublicIP",
        Description="Public IP address of the newly created EC2 instance",
        Value=GetAtt(web_servers, "PublicIp"),
    ),
    Output(
        "PrivateIP",
        Description="Private IP address of the newly created EC2 instance",
        Value=GetAtt(web_servers, "PrivateIp"),
    ),
    Output(
        "PublicDNS",
        Description="Public DNSName of the newly created EC2 instance",
        Value=GetAtt(web_servers, "PublicDnsName"),
    ),
    Output(
        "PrivateDNS",
        Description="Private DNSName of the newly created EC2 instance",
        Value=GetAtt(web_servers, "PrivateDnsName"),
    ),
])
"""
print(template.to_json())
#
