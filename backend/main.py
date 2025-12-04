from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import boto3
from boto3.dynamodb.conditions import Key
import os
import uuid

app = FastAPI(title="Events API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DynamoDB setup
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('DYNAMODB_TABLE', 'events-table')
table = dynamodb.Table(table_name)


# Pydantic models
class Event(BaseModel):
    eventId: Optional[str] = None
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=1000)
    date: str = Field(..., description="ISO format date string")
    location: str = Field(..., min_length=1, max_length=200)
    capacity: int = Field(..., gt=0)
    organizer: str = Field(..., min_length=1, max_length=100)
    status: str = Field(..., pattern="^(active|cancelled|completed)$")


class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1, max_length=1000)
    date: Optional[str] = None
    location: Optional[str] = Field(None, min_length=1, max_length=200)
    capacity: Optional[int] = Field(None, gt=0)
    organizer: Optional[str] = Field(None, min_length=1, max_length=100)
    status: Optional[str] = Field(None, pattern="^(active|cancelled|completed)$")


@app.get("/")
def read_root():
    return {"message": "Events API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/events", status_code=201)
def create_event(event: Event):
    try:
        event_id = str(uuid.uuid4())
        event_data = event.dict()
        event_data['eventId'] = event_id
        
        table.put_item(Item=event_data)
        
        return event_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating event: {str(e)}")


@app.get("/events")
def list_events():
    try:
        response = table.scan()
        events = response.get('Items', [])
        
        return {"events": events, "count": len(events)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing events: {str(e)}")


@app.get("/events/{event_id}")
def get_event(event_id: str):
    try:
        response = table.get_item(Key={'eventId': event_id})
        
        if 'Item' not in response:
            raise HTTPException(status_code=404, detail="Event not found")
        
        return response['Item']
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving event: {str(e)}")


@app.put("/events/{event_id}")
def update_event(event_id: str, event_update: EventUpdate):
    try:
        # Check if event exists
        response = table.get_item(Key={'eventId': event_id})
        if 'Item' not in response:
            raise HTTPException(status_code=404, detail="Event not found")
        
        # Build update expression
        update_data = {k: v for k, v in event_update.dict().items() if v is not None}
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        update_expression = "SET " + ", ".join([f"#{k} = :{k}" for k in update_data.keys()])
        expression_attribute_names = {f"#{k}": k for k in update_data.keys()}
        expression_attribute_values = {f":{k}": v for k, v in update_data.items()}
        
        response = table.update_item(
            Key={'eventId': event_id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="ALL_NEW"
        )
        
        return response['Attributes']
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating event: {str(e)}")


@app.delete("/events/{event_id}")
def delete_event(event_id: str):
    try:
        # Check if event exists
        response = table.get_item(Key={'eventId': event_id})
        if 'Item' not in response:
            raise HTTPException(status_code=404, detail="Event not found")
        
        table.delete_item(Key={'eventId': event_id})
        
        return {"message": "Event deleted successfully", "eventId": event_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting event: {str(e)}")
