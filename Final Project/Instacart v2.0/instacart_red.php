<?php
    
    $user = "awsuser"; 
    $password = "Password_123";
    $ODBCConnection = odbc_connect("Driver={Amazon Redshift (x64)}; Server=dbds-redshift-cluster-1.c3gtomffqqm8.us-east-1.redshift.amazonaws.com; Database=instacart;Port=5439",$user,$password);
    $query = $_GET["query"];
    $RecordSet = odbc_exec($ODBCConnection, $query);

    if($RecordSet === FALSE){
        echo json_encode("Error");
    }else{
        $data = array();
        $i=0;
        while( $row = odbc_fetch_array($RecordSet)) {
            $data[$i] = $row;
            $i++;
        }
        echo json_encode($data);
    }
    
    odbc_close($ODBCConnection);

?>
