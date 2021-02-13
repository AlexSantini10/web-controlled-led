<?php
    require_once "./conn.db.php";

    $table = 'ledtable';
    $myDB=new mysqli($host, $user, $pass, $db);
	
	$result = $myDB->query("SELECT ledState FROM $table");

	$row = $result->fetch_assoc();
		
	
	echo json_encode($row,  JSON_HEX_TAG | JSON_HEX_APOS | JSON_HEX_QUOT | JSON_HEX_AMP | JSON_UNESCAPED_UNICODE );
 