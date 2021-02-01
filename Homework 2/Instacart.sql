CREATE TABLE aisles
(
  aisle_id INT NOT NULL,
  aisle VARCHAR NOT NULL,
  PRIMARY KEY (aisle_id)
);

CREATE TABLE department
(
  department_id INT NOT NULL,
  department VARCHAR NOT NULL,
  PRIMARY KEY (department_id)
);

CREATE TABLE products
(
  product_id INT NOT NULL,
  product_name VARCHAR NOT NULL,
  aisle_id INT NOT NULL,
  department_id INT NOT NULL,
  department_id INT NOT NULL,
  aisle_id INT NOT NULL,
  PRIMARY KEY (product_id),
  FOREIGN KEY (department_id) REFERENCES department(department_id),
  FOREIGN KEY (aisle_id) REFERENCES aisles(aisle_id)
);

CREATE TABLE orders
(
  order_id INT NOT NULL,
  user_id INT NOT NULL,
  order_number INT NOT NULL,
  order_dow INT NOT NULL,
  order_hour_of_day INT NOT NULL,
  days_since_prior_order INT NOT NULL,
  PRIMARY KEY (order_id)
);

CREATE TABLE order_products
(
  reordered INT NOT NULL,
  add_to_cart_order INT NOT NULL,
  product_id INT NOT NULL,
  order_id INT NOT NULL,
  product_id INT NOT NULL,
  order_id INT NOT NULL,
  PRIMARY KEY (product_id, order_id),
  FOREIGN KEY (product_id) REFERENCES products(product_id),
  FOREIGN KEY (order_id) REFERENCES orders(order_id)
);