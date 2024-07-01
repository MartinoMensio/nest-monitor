
resource "aws_dynamodb_table" "example_table" {
  name         = "half-hour-data"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "date"
  attribute {
    name = "date"
    type = "S"
  }
  #   attribute {
  #     name = "ambient_temperature"
  #     type = "N"
  #   }
  #   attribute {
  #     name = "humidity"
  #     type = "N"
  #   }
  #   attribute {
  #     name = "set_temperature_heating"
  #     type = "N"
  #   }
  #   attribute {
  #     name = "status"
  #     type = "N"
  #   }
}
