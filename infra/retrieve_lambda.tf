data "aws_iam_policy_document" "lambda_permissions" {
  version = "2012-10-17"
  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    effect    = "Allow"
    resources = ["arn:aws:logs:*:*:*"]
  }
  statement {
    actions = [
      "dynamodb:PutItem",
      "dynamodb:GetItem",
      "dynamodb:Query",
    ]
    effect = "Allow"
    # resources = [aws_dynamodb_table.example_table.arn]
    resources = ["arn:aws:dynamodb:*:*:*"]
  }
}

# Define the Lambda function
module "retrieve_lambda" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "nest-retrieve"
  description   = "retrieve from Nest"
  runtime       = "python3.11"
  timeout       = 60
  handler       = "main.lambda_handler"
  source_path = [
    {
      path             = "../src/nest_retrieve"
      pip_requirements = true
    }
  ]

  environment_variables = {
    MY_VARIABLE = "my-value"
  }

  # Define the IAM role for the Lambda function
  policy_json        = data.aws_iam_policy_document.lambda_permissions.json
  attach_policy_json = true
}

resource "aws_cloudwatch_event_rule" "schedule" {
  name        = "nest-retrieve-schedule"
  description = "schedule for nest-retrieve"
  # every half hour
  schedule_expression = "rate(30 minutes)"
}

resource "aws_cloudwatch_event_target" "target" {
  target_id = "nest-retrieve-target"
  arn       = module.retrieve_lambda.lambda_function_arn
  rule      = aws_cloudwatch_event_rule.schedule.name
}

resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = module.retrieve_lambda.lambda_function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.schedule.arn
}
