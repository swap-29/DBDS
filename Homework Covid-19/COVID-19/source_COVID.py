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

cur.execute('USE covid19db')

for obj in bucket.objects.all():
    key = obj.key
    ''' COVID-19 table '''
    if key == 'COVID-19.csv':
        cur.execute('DROP TABLE IF EXISTS covid19')
        cur.execute('''create table covid19 (Id int Not null PRIMARY KEY, Province_State Varchar(256),	Country_Region Varchar(256), Date Date, ConfirmedCases int not null, Fatalities int not null)''')
        body = obj.get()['Body'].read()
        content = str(body)
        lines = content.split("\\n")
        # print(lines[1])
        print('Copying '+ str(len(lines)-2) + ' lines...')
        for num in range(len(lines)-1):
            if num == 0:
                continue
            item = lines[num].split(',')
            
            cur.execute('''INSERT INTO covid19 (Id,Province_State,Country_Region,Date,ConfirmedCases,Fatalities )
                        VALUES (%s,%s,%s,%s,%s,%s)''', (item[0],item[1],item[2],item[3],item[4],item[5]))
            conn.commit()
        print('Copy successfully!')
    
cur.close()
