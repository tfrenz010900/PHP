<?php include_once "../includes/functions_inc.php"; ?>
<?php

$db = ConnecttoDB();
$id= $_GET['row_id'];

$sql2 = "SELECT * FROM LocalPitchTable where id=$id";
$sqlQuery = $db->query($sql2);
$result1 = $sqlQuery->fetchAll();
$result2 = $result1[0];

print_r(json_encode($result2));


/*$sql = "SELECT * FROM LocalPitchTable";
$sqlQuery = $db->query($sql);
$result = $sqlQuery->fetchAll();
echo $result;*/