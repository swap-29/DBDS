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

cur.execute('USE instacartdb')

for obj in bucket.objects.all():
    key = obj.key
    ''' orders table '''
    if key == 'orders.csv':
        cur.execute('DROP TABLE IF EXISTS orders')
        cur.execute('''CREATE TABLE orders(
        order_id INT NOT NULL,
        user_id INT NOT NULL,
        order_number INT NOT NULL,
        order_dow INT NOT NULL,
        order_hour_of_day INT NOT NULL,
        days_since_prior_order INT NOT NULL,
        PRIMARY KEY (order_id));''')
        body = obj.get()['Body'].read()
        content = str(body)
        lines = content.split("\\r\\n");
        print('Copying '+ str(len(lines)-2) + ' lines...')
        for num in range(len(lines)-1):
            if num == 0:
                continue
            item = lines[num].split(',')
            
            cur.execute('''INSERT INTO orders (order_id, user_id, order_number,order_dow,order_hour_of_day,days_since_prior_order)
                        VALUES (%s,%s,%s,%s,%s,%s)''', (item[0],item[1],item[2],item[3],item[4],item[5]))
            conn.commit()
        print('Copy successfully!')
  
cur.close()
