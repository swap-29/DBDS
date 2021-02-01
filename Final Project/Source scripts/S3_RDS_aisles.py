#encoding=utf-8

import pymysql
import boto3
import sys

''' connect to s3 '''
s3 = boto3.resource('s3')
bucket = s3.Bucket('dbds-s3-s20')

''' connect to RDS '''
host = "instacart.ciegm3vmldwh.us-east-1.rds.amazonaws.com"
port = 3306
user = "admin"
password = "password_123"
conn = pymysql.connect(host, user=user,
        port=port, passwd=password, use_unicode=True, charset='utf8')
''' instacartdb database '''
cur = conn.cursor()
cur.execute('DROP DATABASE IF EXISTS instacartdb')
cur.execute('''CREATE DATABASE instacartdb''')
cur.execute('USE instacartdb')

for obj in bucket.objects.all():
    key = obj.key
    ''' aisles table '''
    if key == 'aisles.csv':
        cur.execute('DROP TABLE IF EXISTS aisles')
        cur.execute('''CREATE TABLE aisles (aisle_id INT NOT NULL ,aisle VARCHAR(256) NOT NULL ,PRIMARY KEY (aisle_id));''')
        body = obj.get()['Body'].read()
        content = str(body)
        lines = content.split("\\r\\n");
        print('Copying '+ str(len(lines)-2) + ' lines...')
        for num in range(len(lines)-1):
            if num == 0:
                continue
            item = lines[num].split(',')
            
            cur.execute('''INSERT INTO aisles (aisle_id, aisle)
                        VALUES (%s,%s)''', (item[0],item[1]))
            conn.commit()
        print('Copy successfully!')
cur.close()