# SQLoslav
A Python-based SQL bot for Slack. Users send requests, and the bot analyzes the request, creates, and executes an appropriate SQL query using a provided schema to get the desired result.

## Features

- Process SQL queries from Slack messages
- Execute queries against Oracle and Vertica databases
- Return query results as files in Slack channels
- Docker support for easy deployment

## Running with Docker

### Prerequisites

- Docker and Docker Compose
- Slack App configured with proper permissions
- Database access credentials

### Setup

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/SQLoslav.git
   cd SQLoslav
   ```

2. Create an `.env` file with your environment variables (see `.env.example`):
   ```
   cp .env.example .env
   # Edit .env with your settings
   ```

3. Build and start the Docker container:
   ```
   docker-compose up -d
   ```

4. The service will be available on port 5000. 

### Configuring Slack

1. Create a Slack App in the [Slack API Console](https://api.slack.com/apps)
2. Add the following Bot Token Scopes:
   - `chat:write`
   - `files:read`
   - `files:write`
   - `incoming-webhook`
3. Enable Event Subscriptions:
   - Set the Request URL to your server's URL: `https://your-server.com/slack/events`
   - Subscribe to the following events: `message.im`, `file_shared`
4. Install the app to your workspace
5. Copy the Bot User OAuth Token to your `.env` file

## Accessing the Service

When your application is deployed, you can access it through your server's domain at:
`https://your-server.com/`

A simple health check is available at the root URL.

## Development

To run the application locally without Docker:

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   python main.py
   ```

## Troubleshooting

- If you have issues with the Slack integration, check the logs for detailed error messages
- Ensure your server's URL is publicly accessible
- Verify that all database connection credentials are correct
