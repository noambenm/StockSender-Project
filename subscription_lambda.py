import json
import boto3

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('StockSubscriptions')

def lambda_handler(event, context):
    try:
        # Extract data from the API Gateway request
        data = json.loads(event['body'])
        user_email = data['user_email'].lower()
        chosen_ticker = data['chosen_ticker'].upper()

        # Insert data into DynamoDB table
        response = table.put_item(
            Item={
                'user_email': user_email,
                'chosen_ticker': chosen_ticker
            }
        )

        # Return success response
        return {
            'statusCode': 200,
            'body': json.dumps('Subscription saved successfully!')
        }

    except Exception as e:
        # Return error response
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }
