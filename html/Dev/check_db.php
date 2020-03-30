<?php
ob_start();
$bypasslogin = true;
include_once $_SERVER['DOCUMENT_ROOT']."/includes/functions_inc.php";

//$dbhost = '192.168.16.21';
//$dbup = ping('http://'.$dbhost);
//var_dump($dbup);


function is_connectable(string $host, int $port=80, int $timeout=3){
    if($fp = @fsockopen($host, $port, $errno, $errstr, $timeout)){
        return fclose($fp) || true;
    }
    return false;
}

if(is_connectable($host, 3306,1)){
    die("mysql server '$host' is UP");
} else {
    die("mysql server '$host' is down");
}

?>