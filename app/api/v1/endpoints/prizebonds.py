from fastapi import APIRouter, Request
import boto3
import jwt
import os
from boto3.dynamodb.conditions import Key


prize_bond_table_name = os.getenv("PRIZE_BOND_TABLE")
dynamodb = boto3.resource('dynamodb')
prize_bond_table = dynamodb.Table(prize_bond_table_name)

def get_username(request: Request):
    token = request.headers["authorization"].replace('Bearer ', '')
    return jwt.decode(token, options={"verify_signature": False})["username"]

router = APIRouter()

@router.get('/')
def get_prize_bonds(request: Request):
    username = get_username(request)
    
    response = prize_bond_table.query(
        KeyConditionExpression=Key('Username').eq(username)
    )
    return response["Items"]


    
@router.post("/")
async def add_prize_bond(request: Request):
    username = get_username(request)
    request_body = await request.json()
    prize_bond_number =request_body["number"]
    prize_bond_table.put_item(
    TableName=prize_bond_table_name,
    Item={
        'BondNumber': prize_bond_number,
        'Username': username
    })

@router.delete("/")
async def delete_prize_bond(request: Request):
    username = get_username(request)
    request_body = await request.json()
    prize_bond_number =request_body["number"]
    prize_bond_table.delete_item(
    Key={
        'BondNumber': prize_bond_number,
        'Username': username
    })
