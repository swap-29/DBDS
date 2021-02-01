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
    ''' order_products table '''
    if key == 'order_products.csv':
        cur.execute('DROP TABLE IF EXISTS order_products')
        cur.execute('''CREATE TABLE order_products(
        reordered INT NOT NULL,
        add_to_cart_order INT NOT NULL,
        product_id INT NOT NULL,
        order_id INT NOT NULL,
        PRIMARY KEY (product_id, order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id),
        FOREIGN KEY (order_id) REFERENCES orders(order_id));''')
        body = obj.get()['Body'].read()
        content = str(body)
        lines = content.split("\\r\\n");
        print('Copying '+ str(len(lines)-2) + ' lines...')
        for num in range(len(lines)-1):
            if num == 0:
                continue
            item = lines[num].split(',')
            
            cur.execute('''INSERT INTO order_products (order_id, product_id,add_to_cart_order,reordered)
                        VALUES (%s,%s,%s,%s)''', (item[0],item[1],item[2],item[3]))
            conn.commit()
        print('Copy successfully!')
   
cur.close()
