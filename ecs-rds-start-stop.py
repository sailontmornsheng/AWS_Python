import boto3

def lambda_handler(event, context):
    # Configuration - Update these values with your actual resources
    ecs_services = [
        {'cluster': 'ecs-cluster-name', 'service': 'ecs-service-name'}
    ]

    rds_clusters = [
        'rds-cluster-identifier'
    ]

    ecs = boto3.client('ecs')
    rds = boto3.client('rds')

    try:
        if event['action'] == 'stop':
            # Stop ECS services and pause RDS clusters
            for service in ecs_services:
                ecs.update_service(
                    cluster=service['cluster'],
                    service=service['service'],
                    desiredCount=0
                )

            for cluster_id in rds_clusters:
                rds.stop_db_cluster(DBClusterIdentifier=cluster_id)

            message = 'ECS services stopped & RDS clusters paused successfully!'

        elif event['action'] == 'start':
            # Start ECS services and resume RDS clusters
            for service in ecs_services:
                ecs.update_service(
                    cluster=service['cluster'],
                    service=service['service'],
                    desiredCount=1  # Set to your normal desired count
                )

            for cluster_id in rds_clusters:
                rds.start_db_cluster(DBClusterIdentifier=cluster_id)

            message = 'ECS services started & RDS clusters resumed successfully!'

        else:
            return {
                'statusCode': 400,
                'body': 'Invalid action. Use "start" or "stop".'
            }

        return {
            'statusCode': 200,
            'body': message
        }

    except Exception as e:
        print(f'Error: {str(e)}')
        return {
            'statusCode': 500,
            'body': f'Operation failed: {str(e)}'
        }