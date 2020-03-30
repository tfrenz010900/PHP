<?php
include_once $_SERVER['DOCUMENT_ROOT']."/includes/functions_inc.php";
  
  //Uset Cookies
  unset($_COOKIE['isvalid']); 
  unset($_COOKIE['user']);     
  unset($_COOKIE['recid']);    
  unset($_COOKIE['AccountID']);    
  unset($_COOKIE['StudentFirst']);
  unset($_COOKIE['StudentLast']);   
  unset($_COOKIE['StudentNickname']);    
  unset($_COOKIE['StudentEmail']);   

  header("Location: /?result=Logged+Out!");
?>