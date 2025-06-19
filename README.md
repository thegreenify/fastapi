# FastAPI eSewa Allottee API

## Description
Lambda function + API Gateway exposing FastAPI endpoints to get allottee details from DynamoDB.

## Deployment

1. Set up AWS CLI credentials with `aws configure`.
2. Install SAM CLI.
3. Initialize and build:

   ```bash
   sam build
   ```

4. Create the DynamoDB table manually:

   - Table Name: `AllotteeTable`
   - Partition Key: `aan` (String)

5. Deploy using guided SAM:

   ```bash
   sam deploy --guided
   ```
   - Example inputs:
     - Stack name: `fastapi-esewa`
     - AWS Region: `ap-south-1`
     - Accept defaults, save settings.

6. Once deployed, invoke:

   ```
   GET https://<api-id>.execute-api.ap-south-1.amazonaws.com/Prod/api/allottee/<AAN>
   ```

   - Use header: `x-api-key: YOUR_API_KEY_HERE`
