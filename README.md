# Pulse

On-demand gaming servers running on EC2. Automatically starting and stopping game servers depending on usage.

## Requirements

Create a .env file with your RCON password
```env
RCON_PASSWORD=your-password
```

This allows the API to keep track of online players and determine when to shutdown the server