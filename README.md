# ms_sql_server_proxy
Sql server proxy server for when you need it.

## purpose
This api serves the purpose as an api first implementation of the Data Access Layer

## methods
- Swagger (http://127.0.0.1:5800/apidocs/)
- Heartbeat '/'  (http://127.0.0.1:5800/heartbeat/)
- Read
- Upsert (Insert or Update)
- Execute

## Common Issues:
### Getting Error [===> Error Occurred. Error: [WinError 2] The system cannot find the file specified]

Install the BCP and SqlCmd software. https://go.microsoft.com/fwlink/?linkid=2142258

## reference material
- Swagger: https://github.com/flasgger/flasgger