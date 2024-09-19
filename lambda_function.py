import json
import boto3
import yfinance as yf
import currency
import messages
import os
import logging

mySnsTopicArn = os.environ.get('SNS_TOPIC_ARN')
snsClient = boto3.client('sns')

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
        # Fetching VOO data
        voo = yf.Ticker("VOO")
        voo_history = voo.history(period="1mo")
        most_recent_open = round(voo_history.iloc[-1]['Open'], 2)
        average_open = round(voo_history['Open'].mean(), 2)
        usd_price = currency.usd_price
        commission = round(7.5 * usd_price, 2)

        # Condition to check if stock is 15% lower than the average
        if most_recent_open < average_open * 0.85:
            subject = f'VOO Alert: Stock Price Drop - Buy Now!'
            message = messages.buy_now_message(most_recent_open, average_open, usd_price, commission)

            publish_to_sns(mySnsTopicArn, subject, message)
            logging.info(f"Buy Now message sent successfully. Subject: {subject}")
            
            return {
                'statusCode': 200,
                'body': f"Buy Now message sent: {subject}"
            }
        
        # Condition to check if stock is below 95% but above 85% of average
        elif most_recent_open < average_open * 0.95:
            subject = f'VOO Alert: VOO opened at {most_recent_open} - Buy Opportunity!'
            message = messages.buy_opportunity_message(most_recent_open, average_open, usd_price, commission)
            
            # Publish message to SNS
            publish_to_sns(mySnsTopicArn, subject, message)
            logging.info(f"Buy Opportunity message sent successfully. Subject: {subject}")

            return {
                'statusCode': 200,
                'body': f"Message sent: {subject}"
            }
        
        else:
            subject = f'VOO Status: Normal Trading Level at {most_recent_open}'
            message = messages.normal_status_message(most_recent_open, average_open, usd_price, commission)
            
            publish_to_sns(mySnsTopicArn, subject, message)
            logging.info(f"Normal Trading Level message sent successfully. Subject: {subject}")     
            
            return {
                'statusCode': 200,
                'body': f"Message sent: {subject}"
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error occurred: {str(e)}"
        }
