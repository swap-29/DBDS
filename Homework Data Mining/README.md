1. From your wide dataset select the target and the top 10 probes and transfer that subset to your RDBMS. Let's call that table "Genome". Instead of RDBMS you can MongoDB as you wish.

2. KNN Classification model
    Build a stored procedure called usp_knn for the Genome table. usp_knn accepts 10 values for 10 probes as input and returns the nearest neighbor (1NN) target using Euclidean distance.

3. K-Means Clustering model
    Build a stored procedure called usp_kmeans for the Genome table. usp_kmeans accepts @k as input (number of clusters) and returns k centroids (one centroid for each cluster).

4. Recommendation System using Instacart tables
    Build a lookup table called MarketBasket (ProductA varchar(100), ProductB varchar(100), Frq int).
    Fill the MarketBasket table using the list of products by order. For example, if an order has three product (B,C,E) then (B,C,1), (B,E,1) and (C,E,1) are the associated itemsets and the lookup table should be updated for each itemset.
    Write a stored procedure called usp_recommender that accepts a product name as the input and then recommends three (associated) products as the output.
