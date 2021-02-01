<?php
/*
$servername = "localhost";
$username = "root";
$password = "No";
*/
$username = "admin"; 
$password = "password_123";   
$host = "instacart.ciegm3vmldwh.us-east-1.rds.amazonaws.com";
$database="instacartdb";
$port = 3306;

/* We first connect to our database */
$connection = mysqli_connect($host,$username,$password,$database,$port);

/* Capture connection error if any */
if (mysqli_connect_errno($connection)) {
        echo "Failed to connect to DataBase: " . mysqli_connect_error();
    }
else {
  /* Usual SQL Queries */
    $query = $_GET["query"];
    $result = mysqli_query($connection, $query);

    if($result) {
        //Query is successful, do something
        $data = array();
    foreach ($result as $row) {
        $data[] = $row;
    }
    echo json_encode($data);
    /* Encode this array in JSON form */
    }
    else{
        echo json_encode("Error");
    }
    }
    mysqli_close($connection);
?>