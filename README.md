# App Runner Cloud Notes API

A small Flask notes API packaged as a Docker container and designed to run on AWS App Runner. Notes are stored in an encrypted, on-demand DynamoDB table. The CloudFormation template creates the table and a least-privilege App Runner instance role.

## Routes

- `GET /health` — health check.
- `GET /notes` — list up to 50 recent notes.
- `POST /notes` — create a note from `{"text":"..."}`.
- `DELETE /notes/{note_id}` — delete a note.

## Deploy

1. Create the table and App Runner instance role:

   ```bash
   aws cloudformation deploy --template-file template.yaml --stack-name cloud-notes --capabilities CAPABILITY_IAM
   aws cloudformation describe-stacks --stack-name cloud-notes --query "Stacks[0].Outputs"
   ```
2. Build the Docker image, push it to Amazon ECR, and create an App Runner service from that ECR image.
3. Configure the service port as `5000`, health check path as `/health`, environment variable `TABLE_NAME` from the stack output, and the instance role from `AppRunnerInstanceRoleArn`.
4. Call the service URL returned by App Runner.

For local image build: `docker build -t cloud-notes .`.

## Security note

This classroom sample has no user authentication. A public App Runner URL allows anyone to read, add, and delete notes. Use only demo data; add authentication and per-user authorization before public use. App Runner, ECR, and DynamoDB usage may incur charges.

## Clean up

Delete the App Runner service and ECR image repository, then delete the CloudFormation stack. Delete the DynamoDB table only if its notes are no longer needed.
