from fastapi import APIRouter, Request
import boto3
import jwt
import os
from boto3.dynamodb.conditions import Key


prize_bond_table_name = os.getenv("PRIZE_BOND_TABLE")


def get_username(request: Request):
    token = request.headers["authorization"].replace('Bearer ', '')
    return jwt.decode(token, options={"verify_signature": False})["username"]

dynamo_client = boto3.client('dynamodb')
dynamodb = boto3.resource('dynamodb')
router = APIRouter()

@router.get('/')
def get_prize_bonds(request: Request):
    username = get_username(request)
    prize_bond_table = dynamodb.Table(prize_bond_table_name)
    response = prize_bond_table.query(
        KeyConditionExpression=Key('Username').eq(username)
    )
    return response["Items"]


    
@router.post("/add/")
async def add_prize_bond(request: Request):
    username = get_username(request)
    request_body = await request.json()
    prize_bond_number =request_body["number"]
    dynamo_client.put_item(
    TableName=prize_bond_table_name,
    Item={
        'BondNumber': {
            'S': prize_bond_number,
        },
        'Username': {
            'S': username,
        }
    })
