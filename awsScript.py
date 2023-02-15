import boto3
import datetime
import json

def lambda_handler(event, context):
    # Get the workspace ID from the event
    workspace_id = event['workspace_id']
    
    # Set the utilization threshold to determine if the workspace should be set to AlwaysOn or AutoStop
    utilization_threshold = 30 # in percentage
    
    # Initialize the WorkSpaces client
    workspaces_client = boto3.client('workspaces')
    
    # Get the start and end of the previous month
    today = datetime.datetime.now()
    last_month_end = datetime.datetime(today.year, today.month, 1) - datetime.timedelta(days=1)
    last_month_start = datetime.datetime(last_month_end.year, last_month_end.month, 1)
    
    # Get the utilization for the specified Workspace for the previous month
    response = workspaces_client.get_workspace_utilization(
        WorkspaceId=workspace_id,
        StartTime=last_month_start,
        EndTime=last_month_end
    )
    utilization = response['OverallUtilization']
    
    # Determine if the Workspace should be set to AlwaysOn or AutoStop
    if utilization > utilization_threshold:
        run_mode = 'ALWAYS_ON'
    else:
        run_mode = 'AUTO_STOP'
        
    # Update the Workspace with the new run mode
    response = workspaces_client.modify_workspace_properties(
        WorkspaceId=workspace_id,
        WorkspaceProperties={
            'RunningMode': run_mode
        }
    )
    
    # Return the new running mode for the Workspace
    return {
        'statusCode': 200,
        'body': json.dumps({
            'workspace_id': workspace_id,
            'run_mode': run_mode
        })
    }
