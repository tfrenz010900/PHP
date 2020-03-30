<?php include_once "../includes/functions_inc.php"; ?>
<?php

$db = ConnecttoDB();

$sql1 = "SELECT SeqSessionNumber FROM sessions ORDER BY SeqSessionNumber DESC LIMIT 1";
$sqlQuery = $db->query($sql1);
$result = $sqlQuery->fetchAll();
$last_squ_ID = $result['0']['SeqSessionNumber'];


$sql3 = "SELECT count(*) FROM LocalPitchTable where SessionNumber=$last_squ_ID";
$number_of_rows = $db->query($sql3)->fetchColumn();


$sql4 = "SELECT count(*) FROM LocalPitchTable where SessionNumber=$last_squ_ID && PitchCall='MISS'";
$number_of_miss_rows = $db->query($sql4)->fetchColumn();

$sql5 = "SELECT count(*) FROM LocalPitchTable where SessionNumber=$last_squ_ID && PitchCall='SUCCESS'";
$number_of_success_rows = $db->query($sql5)->fetchColumn();


$sql2 = "SELECT * FROM LocalPitchTable where SessionNumber=$last_squ_ID order by id ASC";
$sqlQuery = $db->query($sql2);
$result1 = $sqlQuery->fetchAll();


$result2 = $result1;
$result2['number_of_rows'] = $number_of_rows;
$result2['number_of_miss_rows'] = $number_of_miss_rows;

$result2['number_of_success_rows'] = $number_of_success_rows;
//$result2['audio_url'] = $result2['AudioFileToPlayOnceFullLocalPath'];
//$result2['audio_url'] = 'GoCrazyFolksOzzieShort.wav';


print_r(json_encode($result2));



/*

echo "<pre>";
print_r($result1);
echo "</pre>";




*/






/*$sql = "SELECT * FROM LocalPitchTable";
$sqlQuery = $db->query($sql);
$result = $sqlQuery->fetchAll();
echo $result;*/