<?php include_once $_SERVER['DOCUMENT_ROOT']."/includes/functions_inc.php"; ?>

<?php
$sessionType = $_POST["session_type"];
$targetType = $_POST["target_guid"];
$AccountID = $_COOKIE["AccountID"];

BeginSession(0, $sessionType, $targetType);
?>
