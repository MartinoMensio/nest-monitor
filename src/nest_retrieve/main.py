import boto3
import requests
import datetime

dynamodb = boto3.client("dynamodb")

project_id = "PROJECT_ID"
client_id = "OAUTH_ID.apps.googleusercontent.com"
# TODO secret
client_secret = "OAUTH_CLIENT_SECRET"
# TODO secret
refresh_token = "REFRESH_TOKEN"


def get_nest_data():
    # get data from smartdevicemanagement.googleapis.com devices endpoint
    # https://developers.google.com/nest/device-access/authorize
    # https://developers.google.com/nest/device-access/api/thermostat
    # https://developers.google.com/nest/device-access/api/structure
    # https://developers.google.com/nest/device-access/api/devices
    # https://developers.google.com/nest/device-access/api/traits

    # refresh token
    get_token_url = f"https://www.googleapis.com/oauth2/v4/token"
    res = requests.post(
        get_token_url,
        params={
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        },
    )
    res.raise_for_status()
    access_token = res.json()["access_token"]
    # get devices
    get_devices_url = f"https://smartdevicemanagement.googleapis.com/v1/enterprises/{project_id}/devices"
    res = requests.get(
        get_devices_url, headers={"Authorization": f"Bearer {access_token}"}
    )
    res.raise_for_status()
    devices = res.json()["devices"]
    # thermostat
    thermostat = next(
        filter(lambda device: device["type"] == "sdm.devices.types.THERMOSTAT", devices)
    )
    return thermostat


def convert_to_dynamodb_data(data):
    # get date in format YYYY-MM-DD HH:MM timezone UTC
    date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M")
    # ambient temperature
    ambient_temperature_c = data["traits"]["sdm.devices.traits.Temperature"][
        "ambientTemperatureCelsius"
    ]
    # humidity
    humidity = data["traits"]["sdm.devices.traits.Humidity"]["ambientHumidityPercent"]
    # set temperature heating
    set_temperature_heating = data["traits"][
        "sdm.devices.traits.ThermostatTemperatureSetpoint"
    ]["heatCelsius"]
    # status
    status = data["traits"]["sdm.devices.traits.ThermostatHvac"]["status"]
    # now build dynamodb item
    dynamodb_item = {
        "date": {"S": date},
        "ambient_temperature": {"N": str(ambient_temperature_c)},
        "humidity": {"N": str(humidity)},
        "set_temperature_heating": {"N": str(set_temperature_heating)},
        "status": {"S": status},
    }
    return dynamodb_item


def save_item_dynamodb(item):
    # save data to dynamodb
    dynamodb.put_item(TableName="half-hour-data", Item=item)


def lambda_handler(event, context):
    main()


def main():
    data = get_nest_data()
    item = convert_to_dynamodb_data(data)
    save_item_dynamodb(item)
