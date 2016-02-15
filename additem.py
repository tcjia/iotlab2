import boto
import boto.dynamodb2
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import NUMBER
from boto.dynamodb2.fields import HashKey, RangeKey, GlobalAllIndex
from boto.dynamodb2.items import Item
from boto.dynamodb2.layer1 import DynamoDBConnection
import time
import boto3

ACCOUNT_ID = '460938874778'
IDENTITY_POOL_ID = 'us-east-1:ce548f45-2294-46ee-9231-a8f876ca2658'
ROLE_ARN = 'arn:aws:iam::460938874778:role/Cognito_edisonDemoKinesisUnauth_Role'

# Use cognito to get an identity.
cognito = boto.connect_cognito_identity()
cognito_id = cognito.get_id(ACCOUNT_ID, IDENTITY_POOL_ID)
oidc = cognito.get_open_id_token(cognito_id['IdentityId'])
 
# Further setup your STS using the code below
sts = boto.connect_sts()
assumedRoleObject = sts.assume_role_with_web_identity(ROLE_ARN, "XX", oidc['Token'])

DYNAMODB_TABLE_NAME = 'edisonDemoDynamo'

# Prepare DynamoDB client
client_dynamo = boto.dynamodb2.connect_to_region(
    'us-east-1',
    aws_access_key_id=assumedRoleObject.credentials.access_key,
    aws_secret_access_key=assumedRoleObject.credentials.secret_key,
    security_token=assumedRoleObject.credentials.session_token)
 
TABLENAME = 'demo'
users=Table(TABLENAME,connection=client_dynamo)

#check table
table_exists = False
try:
    tabledescription = client_dynamo.describe_table(TABLENAME)
    table_exists = True
    print 'try'
except Exception as e:
    if "Requested resource not found: Table" in str(e): table_exists = False
    print 'exception'
if table_exists: print 'Table exists '+TABLENAME
else: print 'Table does not exist '+TABLENAME

#check item
ITEMNAME = '20160214'
if  users.has_item(username=ITEMNAME): print 'Item exists '+ITEMNAME
else: print 'Item does not exist '+ITEMNAME
#users.put_item(data={'username': '20160214','first_name':'Shiwei','last_name': 'Ren','account_type': 'standard_user',})
