
from mysecrets import usr,passw,account
from snowflake.snowpark.session import Session
import time
from socket import socket
import websocket

SPCS_SERV='WS_STREAMING_SPCS_SERVICE'
ENDPOINT_NAME='ui'
SPCS_DB='WS_STREAMING_SPCS_DB'
SPCS_SC='WS_STREAMING_SPCS_SC'
SPCS_ROLE='WS_STREAMING_SPCS_ROLE'

snowflake_connection_info = {
    "account": account,
    "user": usr,
    "password": passw
}

session = Session.builder.configs(snowflake_connection_info).create()
print('Connected to Snowflake...')

session.sql(f'''USE WAREHOUSE WS_STREAMING_WH''').collect()
session.sql(f'''USE ROLE {SPCS_ROLE}''').collect()
edpts = session.sql(f'''show endpoints in service {SPCS_DB}.{SPCS_SC}.{SPCS_SERV} ''')
print('Endpoints found...')

df = edpts.filter(f''' "name" = '{ENDPOINT_NAME}' ''').to_pandas()
url = df['ingress_url'].iloc[0]
print(f'Found Ingress: {url}...')

session.sql(f"alter session set python_connector_query_result_format = json;").collect()
tkdata = session.connection._rest._token_request('ISSUE')
token = tkdata['data']['sessionToken']
print('Token grabbed...')

header = {'Authorization': f'''Snowflake Token="{token}"'''}
sock=f'wss://{url}/'

def on_error(ws, error):
    print(error)

def on_open(ws):
    print (f'Websocket connected to the server: {sock}')
    print ('Sending MSG every second...')
    print (f'Check https://{url}')
    loopSend()

def loopSend():
    ws.send("Hey from python")
    time.sleep(1)
    loopSend()

ws=websocket.WebSocketApp(sock, header=header,on_open=on_open, on_error=on_error)
ws.run_forever()


