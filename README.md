## Quickbooks Oauth Webapp

This app is meant to provide a quick method to authorize a QuickBooks app.

### Getting Started

#### Clone the repository:

    git clone https://github.com/apartmentlines/qbo-oauth-webapp.git

#### Install dependencies:

    cd qbo-oauth-webapp/
    pip install -r requirements.txt

#### Configure app

Before using this app, please make sure you do the following:

1. Start an ngrok, instance: `ngrok http 8000`
2. Update the parameters in `~/.qb-api/production-config-auth.json`:
  * `server_access_token` (`qb-api.json` in `config.js` in web-api-gateway)
  * `server_endpoint` (normally https://www.apartmentlines.com/api/sss)
  * `client_id` ID and `client_secret` (found at https://developer.intuit.com, Keys & credentials)
  * `redirect_host`, hostname from the 'Forwarding' value in the running ngrok instance above

#### Using the app:

    python manage.py runserver

...then...

1. Launch the app using the ngrok 'Forwarding' value from above.
2. At https://developer.intuit.com
  * Log in as `admin@apartmentlines.com`
  * Add the console output of the `REDIRECT_URI` value to Keys & credentials -> Redirect URIs
  * Log out
3. Log in to `https://qbo.intuit.com/` as an admin for the Apartment Lines Quickbooks company
4. Click `Authorize app`
5. Check the console output of `qbo-oauth-webapp`, it should have successfully written the necessary credentials to shared storage

### App Workflows

1. OAuth flow followed by QBO API call
2. Refresh and Revoke API for OAuth2 `bearer_token`
