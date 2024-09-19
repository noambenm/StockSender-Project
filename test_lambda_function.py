import boto3
import yfinance as yf
import messages
import os
import logging

# Initialize DynamoDB and SES clients
dynamodb = boto3.resource('dynamodb')
ses_client = boto3.client('ses', region_name='us-east-1')  # Change region as needed

# Load environment variables
table_name = os.environ.get('DYNAMODB_TABLE_NAME', 'UserSubscriptions')
sender_email = os.environ.get('SENDER_EMAIL')  # Verified SES email
sns_topic_arn = os.environ.get('SNS_TOPIC_ARN')  # If you still want to use SNS

# Initialize DynamoDB table
table = dynamodb.Table(table_name)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def publish_to_sns(topic_arn, subject, message):
    sns_client = boto3.client('sns')
    try:
        sns_client.publish(
            TopicArn=topic_arn,
            Subject=subject,
            Message=message
        )
    except Exception as e:
        logger.error(f"Failed to publish message to SNS: {str(e)}")
        raise

def send_email(recipient_email, subject, body):
    try:
        response = ses_client.send_email(
            Source=sender_email,
            Destination={
                'ToAddresses': [recipient_email],
            },
            Message={
                'Subject': {
                    'Data': subject,
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': body,
                        'Charset': 'UTF-8'
                    }
                }
            }
        )
        logger.info(f"Email sent to {recipient_email}: {response['MessageId']}")
    except Exception as e:
        logger.error(f"Failed to send email to {recipient_email}: {str(e)}")

def lambda_handler(event, context):
    try:
        # Scan the DynamoDB table to get all subscriptions
        response = table.scan()
        subscriptions = response.get('Items', [])

        if not subscriptions:
            logger.info("No subscriptions found.")
            return {
                'statusCode': 200,
                'body': 'No subscriptions to process.'
            }

        for subscription in subscriptions:
            user_email = subscription['user_email']
            ticker_symbol = subscription['chosen_ticker']

            # Fetch stock data
            ticker = yf.Ticker(ticker_symbol)
            usd = yf.Ticker('USDILS=X')

            try:
                current_value = ticker.info['ask']
                usd_value = usd.info['ask']
                ticker_history = ticker.history(period="1mo")
                average_open = round(ticker_history['Open'].mean(), 2)
                commission = round(7.5 * usd_value, 2)
            except Exception as e:
                logger.error(f"Error fetching data for {ticker_symbol}: {str(e)}")
                continue  # Skip to the next subscription

            # Determine the message based on stock performance
            if current_value < average_open * 0.85:
                subject = f'{ticker_symbol} Alert: Stock Price Drop and it is {current_value} - Buy Now!'
                message = messages.buy_now_message(current_value, average_open, usd_value, commission)
            elif current_value < average_open * 0.95:
                subject = f'{ticker_symbol} Alert: {ticker_symbol} opened at {current_value} - Buy Opportunity!'
                message = messages.buy_opportunity_message(current_value, average_open, usd_value, commission)
            else:
                subject = f'{ticker_symbol} Status: Normal Trading Level at {current_value}'
                message = messages.normal_status_message(current_value, average_open, usd_value, commission)

            # Send email to the user
            send_email(user_email, subject, message)

            # Optionally, publish to SNS
            # publish_to_sns(sns_topic_arn, subject, message)

        return {
            'statusCode': 200,
            'body': 'Emails sent successfully.'
        }

    except Exception as e:
        logger.error(f"Error in lambda_handler: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"Error occurred: {str(e)}"
        }
