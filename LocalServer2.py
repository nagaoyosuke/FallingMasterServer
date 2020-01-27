import os
import psycopg2
from static.FlaskServer import app,Set_DBPass

if __name__ == '__main__':
  Set_DBPass('postgresql://hw17a124:@localhost:5432/ukemimasterdatabase')
  app.run(host=os.getenv('APP_ADDRESS', 'localhost'), port=8000)
