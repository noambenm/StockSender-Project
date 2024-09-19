import boto3
import yfinance as yf
import messages
import os
import logging

# Imports the environment variable: SNS ARN from the AWS account in order to keep the code free of sensitive data
mySnsTopicArn = os.environ.get('SNS_TOPIC_ARN')

# Initiate the SNS feature within the lambda function using boto3
snsClient = boto3.client('sns')

# Defines a function that publishes the SNS topic using the ARN, subject and message from the messages.py file
def publish_to_sns(topic_arn, subject, message):

    try:
        snsClient.publish(
            TopicArn=topic_arn,
            Subject=subject,
            Message=message
        )
    except Exception as e:
        logging.error(f"Failed to publish message to SNS: {str(e)}")
        raise

def lambda_handler(event, context):
    
    try:
        # Fetching VOO data and establishes veriables
        voo = yf.Ticker("VOO")
        usd = yf.Ticker('USDILS=X')
        current_value = voo.info['ask']
        usd_value = usd.info['ask']
        voo_history = voo.history(period="1mo")
        average_open = round(voo_history['Open'].mean(), 2)
        commission = round(7.5 * usd_value, 2)

        # Condition to check if stock is lower than the average and sends the corresponding message
        if current_value < average_open * 0.85:
            subject = f'VOO Alert: Stock Price Drop and it is {current_value} - Buy Now!'
            message = messages.buy_now_message(current_value, average_open, usd_value, commission)
        elif current_value < average_open * 0.95:
            subject = f'VOO Alert: VOO opened at {current_value} - Buy Opportunity!'
            message = messages.buy_opportunity_message(current_value, average_open, usd_value, commission)
        else:
            subject = f'VOO Status: Normal Trading Level at {current_value}'
            message = messages.normal_status_message(current_value, average_open, usd_value, commission)

        # Publish message to SNS
        publish_to_sns(mySnsTopicArn, subject, message)
        logging.info(f"Message sent successfully. Subject: {subject}")

        return {
            'statusCode': 200,
            'body': f"Message sent: {subject}"
        }
                    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error occurred: {str(e)}"
        }
