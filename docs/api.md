# API Documentation

The Battle Results API provides endpoints to manage game battle results. This document provides a detailed overview of the available endpoints, their expected inputs, and outputs.

## Base URL

All API endpoints are relative to the base URL of the application. In development, this is typically:

```
http://localhost:8080
```

## Endpoints

### List All Battle Entries

**GET /entries**

Returns a list of all battle entries in the database.

**Response**

- Status: 200 OK
- Content-Type: application/json

```json
{
  "entries": [
    {
      "id": 1,
      "gameTag": "dweeb_fight",
      "player1Name": "Player 1",
      "player2Name": "Player 2",
      "winnerName": "Player 2",
      "finishedDate": "2025-07-21 15:30:45"
    },
    {
      "id": 2,
      "gameTag": "battle_arena",
      "player1Name": "John",
      "player2Name": "Alice",
      "winnerName": "Alice",
      "finishedDate": "2025-07-22 10:15:22"
    }
  ]
}
```

### Create a New Battle Entry

**POST /entries**

Creates a new battle entry in the database.

**Request Body**

```json
{
  "gameTag": "dweeb_fight",
  "player1Name": "Player 1",
  "player2Name": "Player 2",
  "winnerName": "Player 2"
}
```

**Required Fields**
- `gameTag`: Identifier for the game
- `player1Name`: Name of the first player
- `player2Name`: Name of the second player
- `winnerName`: Name of the winner (must match either player1Name or player2Name)

**Response**

- Status: 201 Created
- Content-Type: application/json

```json
{
  "message": "Battle entry created with id 3"
}
```

### Get a Specific Battle Entry

**GET /entries/{entryId}**

Returns a specific battle entry by ID.

**Parameters**
- `entryId`: The ID of the battle entry to retrieve

**Response**

- Status: 200 OK
- Content-Type: application/json

```json
{
  "entry": {
    "id": 1,
    "gameTag": "dweeb_fight",
    "player1Name": "Player 1",
    "player2Name": "Player 2",
    "winnerName": "Player 2",
    "finishedDate": "2025-07-21 15:30:45"
  }
}
```

### Update a Battle Entry

**PATCH /entries/{entryId}**

Updates a specific battle entry by ID.

**Parameters**
- `entryId`: The ID of the battle entry to update

**Request Body**

```json
{
  "winnerName": "Player 1"
}
```

**Updatable Fields**
- `player1Name`: Name of the first player
- `player2Name`: Name of the second player
- `winnerName`: Name of the winner (must match either player1Name or player2Name)
- `finishedDate`: Date and time when the battle was finished (format: "YYYY-MM-DD HH:MM:SS")

**Note**: The `gameTag` field cannot be updated.

**Response**

- Status: 200 OK
- Content-Type: application/json

```json
{
  "message": "Battle entry with id 1 has been updated"
}
```

### Delete a Battle Entry

**DELETE /entries/{entryId}**

Deletes a specific battle entry by ID.

**Parameters**
- `entryId`: The ID of the battle entry to delete

**Response**

- Status: 200 OK
- Content-Type: application/json

```json
{
  "message": "Battle entry with id 1 has been deleted"
}
```

## Error Responses

### Resource Not Found

- Status: 404 Not Found
- Content-Type: application/json

```json
{
  "message": "Entry with id 999 was not found"
}
```

### Bad Request

- Status: 400 Bad Request
- Content-Type: application/json

```json
{
  "error": "Inform different player names and ensure that the winner's name matches one of the player's names"
}
```

### Internal Server Error

- Status: 500 Internal Server Error
- Content-Type: application/json

```json
{
  "error": "An unexpected error occurred."
}
```
