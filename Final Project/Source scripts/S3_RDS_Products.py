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
    ''' products table '''
    if key == 'products.csv':
        cur.execute('DROP TABLE IF EXISTS products')
        cur.execute('''CREATE TABLE products(  product_id INT NOT NULL,product_name VARCHAR (256) NOT NULL,aisle_id INT NOT NULL,
        department_id INT NOT NULL,PRIMARY KEY (product_id), FOREIGN KEY (department_id) REFERENCES departments(department_id),
        FOREIGN KEY (aisle_id) REFERENCES aisles(aisle_id));''')
        body = obj.get()['Body'].read()
        content = str(body)
        lines = content.split("\\r\\n");
        print('Copying '+ str(len(lines)-2) + ' lines...')
        for num in range(len(lines)-1):
            if num == 0:
                continue
            item = lines[num].split(',')
            
            cur.execute('''INSERT INTO products (product_id, product_name,aisle_id,department_id)
                        VALUES (%s,%s,%s,%s)''', (item[0],item[1],item[2],item[3]))
            conn.commit()
        print('Copy successfully!')
    
cur.close()
