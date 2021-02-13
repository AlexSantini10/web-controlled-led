<?php
    require_once "./conn.db.php";
        
    $table = 'ledtable';
    $myDB=new mysqli($host, $user, $pass, $db);
    
    $myDB->query("UPDATE $table SET toChange=1");
?>