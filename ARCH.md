
- Each service needs IAM configuration both ways

1. Trigger:
   - Event bridge or Client
2. Trigger on Lambda makes outbound request, gets inbound data, publishes to SNS topic
3. SQS Queue(s) subscribed to the topic receives message(s)
4. Send relevant message to S3


5. Create inbound lambda
   - Add IAM permissions for EventBridge, SNS, SQS, RDS, EC2 and S3 etc.
   - Add layers and version
   - Configure runtime, handler, and environment variables
6. Add trigger from EventBridge: Create or select existing rule
   <!-- The trigger <RULE_NAME> was successfully added to function <LAMBDA_FUNCTION>. The function is now receiving events from the trigger. -->
7. Add destination:
   - <https://docs.aws.amazon.com/lambda/latest/dg/invocation-async.html#invocation-async-destinations>
   - Source: Asynchronous invocation
   - Condition: Success
   - Destination type: SNS topic
   - Destination: <SNS_TOPIC_ARN>

