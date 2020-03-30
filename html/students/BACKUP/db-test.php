

<?php include_once $_SERVER['DOCUMENT_ROOT']."/includes/functions_inc.php"; ?>
<?php
  $db = ConnecttoDB();
//   var_dump($db);
  $AccountID = '1234';
//   var_dump($AccountID);
  $WasOverride = true;
  $SessionType = 'John';
  $TargetGUID = '1234';
  $t = date('Y-d-m H:i:s');
  try {
     $sql = "INSERT INTO sessions (AccountID, WasOverride, CreatedAt, UpdatedAt, Status, SessionType, TargetGUID) VALUES ('$AccountID', '$WasOverride', '$t', '$t', 'New', '$SessionType', '$TargetGUID')";
     var_dump($sql);
     $q = $db->prepare($sql);
     $q->execute(array(':AccountID'=>$AccountID,':Action'=>$Action));
     $lastId = $db->lastInsertId();
   } catch(PDOException $ex) {
    $lastId = "error";
   }
    echo $lastId;

?>