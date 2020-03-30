<?php
ob_start();
$bypasslogin = true;
include_once $_SERVER['DOCUMENT_ROOT']."/includes/functions_inc.php";
 $result = isset($_REQUEST['result']) ? $_REQUEST['result'] : ''; //Login Message
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta name="description" content="">
  <meta name="author" content="">
  <title>SmartMitt</title>
  <link rel="stylesheet" type="text/css" href="/vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" type="text/css" href="/vendor/font-awesome/css/font-awesome.min.css" rel="stylesheet" type="text/css">
  <link rel="stylesheet" type="text/css" href="/vendor/jquery.growl/stylesheets/jquery.growl.css">  
  <link href="/css/sb-admin.css" rel="stylesheet" type="text/css">
</head>
<body class="bg-dark">  	
  <div class="container">
    <div class="card card-login mx-auto mt-5">
      <div class="card-header text-center"><img src="/img/smartmitt.png" class="img-fluid"></div>
      <div class="card-body">
        <form action="/process_login.php" method="post" class="form-horizontal">
          <div class="form-group">
            <label for="emailaddress_input">Email address</label>
            <input class="form-control" name="emailaddress_input" id="emailaddress_input" type="email" aria-describedby="emailHelp" placeholder="Enter email">
          </div>
          <div class="form-group" id="password_entry">
            <label id="password_input_label" for="password_input">Password</label>
            <input class="form-control" name="password_input" id="password_input" type="password" placeholder="Password">
          </div>
          <button type="submit" name="Submit" class="btn btn-primary btn-block">Login</button>
        </form>
      </div>
    </div>
  </div>
  <?php
ob_start();
 include_once $_SERVER['DOCUMENT_ROOT']."/includes/scripts.php";
?> 
</body>
</html>
