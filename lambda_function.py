import json
import boto3
import yfinance as yf

mySnsTopicArn = 'arn:aws:sns:us-east-1:590184057629:Stonk_Sender_Email_Alert'

def lambda_handler(event, context):
    snsClient = boto3.client('sns')
    
    try:
        # Fetching VOO data
        voo = yf.Ticker("VOO")
        voo_history = voo.history(period="1mo")
        most_recent_open = voo_history.iloc[-1]['Open']
        average_open = voo_history['Open'].mean()
        
        # Condition to check if stock is 15% lower than the average
        if most_recent_open < average_open * 0.85:
            subject = f'VOO Alert: VOO opened at {most_recent_open} - Buy Opportunity!'
            message = (
                f"VOO opened at {most_recent_open}, which is 15% lower than the average open price over the past month.\n\n"
                f"Average open price: {average_open}\n"
                f"Current price: {most_recent_open}\n\n"
                "This might be a good time to buy more VOO. Check your investment strategy."
            )
            
            # Publish message to SNS
            snsClient.publish(
                TopicArn=mySnsTopicArn,
                Subject=subject,
                Message=message
            )
            return {
                'statusCode': 200,
                'body': f"Message sent: {subject}"
            }
        else:
            subject = f'VOO Status: Normal Trading Level at {most_recent_open}'
            message = (
                f"VOO is trading at {most_recent_open}, which is within the normal range.\n\n"
                f"Average open price over the past month: {average_open}\n"
                "No significant price drop detected. No action required."
            )
            
            # Publish message to SNS
            snsClient.publish(
                TopicArn=mySnsTopicArn,
                Subject=subject,
                Message=message
            )
            return {
                'statusCode': 200,
                'body': f"Message sent: {subject}"
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error occurred: {str(e)}"
        }