import logging
import time
import requests
import boto3
import botocore
from settings import Config, Request

logging.basicConfig(
    format='%(asctime)s %(levelname)-4s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger()

config = Config()
request = Request()
aws_access_key = config.AWS_ACCESS_KEY
aws_secret_key = config.AWS_SECRET_KEY
cron_time = int(config.CRON_TIME)

aws_session = boto3.Session(aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)


def get_instances(region):
    instances = []
    try:
        client = aws_session.client('ec2', region_name=region)
        response = client.describe_instances()
        reservations = response.get('Reservations')
        if reservations:
            for reservation in reservations:
                for instance in reservation['Instances']:
                    instances.append({
                        'name': instance['KeyName'],
                        'type': instance['InstanceType'],
                        'launched_at': instance['LaunchTime'].strftime('%Y-%m-%d, %H:%M:%S'),
                        'public_dns': instance['PublicDnsName']
                    })
        return instances
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'LimitExceededException':
            logger.error('Fetching AWS api call limit exceeded; backing off and retrying...')
            return instances
        else:
            logger.error('error in fetching instances...', error.response.text)
            raise error


def main():
    ec2_instances = {}
    ec2_client = aws_session.client('ec2', region_name='us-west-2')
    regions = config.REGIONS.split(',') if config.REGIONS\
        else [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

    while True:
        for region in regions:
            instances = get_instances(region)
            if instances:
                ec2_instances[region] = instances
        logger.info('fetched ec2 instances successfully...')

        try:
            request.post(json_data=ec2_instances)
            logger.info('posted ec2 instances successfully....')
        except requests.exceptions.HTTPError as error:
            logger.error('error in posting ec2 instances...', error.response.text)
        time.sleep(cron_time * 60)


if __name__ == '__main__':
    main()
