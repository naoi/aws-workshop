# Events API Documentation

## Base URL
```
https://kwwm5oy0kl.execute-api.us-west-2.amazonaws.com/prod
```

## Endpoints

### Health Check
```
GET /health
```
Returns the health status of the API.

**Response:**
```json
{"status": "healthy"}
```

### Create Event
```
POST /events
```

**Request Body:**
```json
{
  "title": "string (1-200 chars)",
  "description": "string (1-1000 chars)",
  "date": "string (ISO format)",
  "location": "string (1-200 chars)",
  "capacity": "integer (> 0)",
  "organizer": "string (1-100 chars)",
  "status": "string (active|cancelled|completed)"
}
```

**Response:**
```json
{
  "eventId": "uuid",
  "title": "string",
  "description": "string",
  "date": "string",
  "location": "string",
  "capacity": integer,
  "organizer": "string",
  "status": "string"
}
```

### List All Events
```
GET /events
```

**Response:**
```json
{
  "events": [
    {
      "eventId": "uuid",
      "title": "string",
      "description": "string",
      "date": "string",
      "location": "string",
      "capacity": integer,
      "organizer": "string",
      "status": "string"
    }
  ],
  "count": integer
}
```

### Get Event by ID
```
GET /events/{event_id}
```

**Response:**
```json
{
  "eventId": "uuid",
  "title": "string",
  "description": "string",
  "date": "string",
  "location": "string",
  "capacity": integer,
  "organizer": "string",
  "status": "string"
}
```

### Update Event
```
PUT /events/{event_id}
```

**Request Body:** (all fields optional)
```json
{
  "title": "string",
  "description": "string",
  "date": "string",
  "location": "string",
  "capacity": integer,
  "organizer": "string",
  "status": "string"
}
```

**Response:**
```json
{
  "eventId": "uuid",
  "title": "string",
  "description": "string",
  "date": "string",
  "location": "string",
  "capacity": integer,
  "organizer": "string",
  "status": "string"
}
```

### Delete Event
```
DELETE /events/{event_id}
```

**Response:**
```json
{
  "message": "Event deleted successfully",
  "eventId": "uuid"
}
```

## Error Responses

### 404 Not Found
```json
{
  "detail": "Event not found"
}
```

### 400 Bad Request
```json
{
  "detail": "Validation error message"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Error message"
}
```

## CORS
The API is configured with CORS enabled for all origins, methods, and headers.

## Example Usage

### Create an Event
```bash
curl -X POST https://kwwm5oy0kl.execute-api.us-west-2.amazonaws.com/prod/events \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Tech Conference 2024",
    "description": "Annual technology conference",
    "date": "2024-12-15T10:00:00",
    "location": "Seattle, WA",
    "capacity": 500,
    "organizer": "Tech Corp",
    "status": "active"
  }'
```

### List All Events
```bash
curl https://kwwm5oy0kl.execute-api.us-west-2.amazonaws.com/prod/events
```

### Get Specific Event
```bash
curl https://kwwm5oy0kl.execute-api.us-west-2.amazonaws.com/prod/events/{event_id}
```

### Update Event
```bash
curl -X PUT https://kwwm5oy0kl.execute-api.us-west-2.amazonaws.com/prod/events/{event_id} \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

### Delete Event
```bash
curl -X DELETE https://kwwm5oy0kl.execute-api.us-west-2.amazonaws.com/prod/events/{event_id}
```
