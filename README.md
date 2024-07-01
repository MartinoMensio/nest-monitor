## Nest API

How to:
https://developers.google.com/nest/device-access/authorize

https://console.nest.google.com/device-access/project/PROJECT_ID/information

https://www.googleapis.com/oauth2/v4/token?client_id=oauth2-client-id&client_secret=oauth2-client-secret&code=authorization-code&grant_type=authorization_code&redirect_uri=https://www.google.com'


https://www.google.com/?code=OUTPUT_CODE&scope=https://www.googleapis.com/auth/sdm.service —> code: OUTPUT_CODE

OAUTH ID: OAUTH_ID.apps.googleusercontent.com

Project ID: PROJECT_ID

Oauth client secret: OAUTH_CLIENT_SECRET

Refresh token: REFRESH_TOKEN

https://developers.google.com/nest/device-access/traits


Idea:
- Store JSON response of devices every half hour —> lambda —> bucket / DB (serverless on demand?) (relational vs document? —> dynamoDB table is serverless)
- Process and collect real temp/ set temp/humidity/
- Plots online

