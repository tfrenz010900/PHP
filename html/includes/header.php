<?php
ob_start();
 include_once "../includes/functions_inc.php";
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
  <?php
    $site_url = "http://10.0.0.200";
  ?>
  <link href="<?php echo $site_url; ?>/vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">
  <link href="<?php echo $site_url; ?>/vendor/font-awesome/css/font-awesome.min.css" rel="stylesheet" type="text/css">
  <link href="<?php echo $site_url; ?>/vendor/font-awesome-five/css/all.min.css" rel="stylesheet" type="text/css">
  <link href="<?php echo $site_url; ?>/vendor/datatables/dataTables.bootstrap4.css" rel="stylesheet">
  <link href="<?php echo $site_url; ?>/vendor/jquery.growl/stylesheets/jquery.growl.css">  
  <link href="<?php echo $site_url; ?>/vendor/jquery.ui/jquery-ui.css" rel="stylesheet" type="text/css"> 
  <link href="<?php echo $site_url; ?>/vendor/jquery.ui/jquery-ui.structure.css" rel="stylesheet" type="text/css">        
  <link href="<?php echo $site_url; ?>/css/sb-admin.css" rel="stylesheet" type="text/css" >

    <!-- Bootstrap core JavaScript-->
    <script type="text/javascript" src="<?php echo $site_url; ?>/vendor/jquery/jquery.min.js"></script>
    <script type="text/javascript" src="<?php echo $site_url; ?>/vendor/bootstrap/js/bootstrap.bundle.min.js"></script>
    <script type="text/javascript" src="<?php echo $site_url; ?>/vendor/jquery-easing/jquery.easing.min.js"></script>
    <script type="text/javascript" src="<?php echo $site_url; ?>/vendor/datatables/jquery.dataTables.js"></script>
    <script type="text/javascript" src="<?php echo $site_url; ?>/vendor/datatables/dataTables.bootstrap4.js"></script>
    <script type="text/javascript" src="<?php echo $site_url; ?>/vendor/jquery.growl/javascripts/jquery.growl.js"></script>    
    <script type="text/javascript" src="<?php echo $site_url; ?>/js/sb-admin-datatables.js"></script> 
    <script type="text/javascript" src="<?php echo $site_url; ?>/vendor/jquery.ui/jquery-ui.js"></script>   
    <?php  //Log out Back
        header("Cache-Control: no-cache, no-store, must-revalidate"); // HTTP 1.1.
        header("Pragma: no-cache"); // HTTP 1.0.
        header("Expires: 0"); // Proxies.
       
    ?>
</head>

<body class="fixed-nav sticky-footer bg-dark" id="page-top">
  <!-- Navigation-->
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top" id="mainNav">
    <a class="navbar-brand" href="<?php echo $site_url; ?>/admin/demo.php">Smart Mitt <img src="<?php echo $site_url; ?>/img/smartmitt.png" height="30"></a>
    <button class="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span> 
    </button>
    <div class="collapse navbar-collapse" id="navbarResponsive">
      <ul class="navbar-nav navbar-sidenav" id="smartmittAccordion">
        
<!--
<li class="nav-item" data-toggle="tooltip" data-placement="right" title="Dashboard">
          <a class="nav-link" href="<?php echo $site_url; ?>/admin/demo.php">
            <i class="fa fa-fw fa-tachometer-alt"></i>
            <span class="nav-link-text">Dashboard</span>
          </a>
        </li>
        <li class="nav-item" data-toggle="tooltip" data-placement="right" title="Charts">
          <a class="nav-link" href="<?php echo $site_url; ?>/admin/demo.php">
            <i class="fa fa-fw fa-area-chart"></i>
            <span class="nav-link-text">Pitch History</span>
          </a>
        </li>
        <li class="nav-item" data-toggle="tooltip" data-placement="right" title="Tables">
          <a class="nav-link" href="<?php echo $site_url; ?>/admin/demo.php">
            <i class="fa fa-fw fa-table"></i>
            <span class="nav-link-text">Profile</span>
          </a>
        </li>
        <li class="nav-item" data-toggle="tooltip" data-placement="right" title="Tables">
          <a class="nav-link" href="<?php echo $site_url; ?>/admin/demo.php">
            <i class="fa fa-fw fa-table"></i>
            <span class="nav-link-text">Config</span>
          </a>
        </li> 

-->
        
        <li class="nav-item" data-toggle="tooltip" data-placement="right" title="Tables">
          <a class="nav-link" href="<?php echo $site_url; ?>/students/students.php">
            <i class="fa fa-fw fa-table"></i>
            <span class="nav-link-text">Student Section</span>
          </a>
        </li> 
        
        <?php if(IsSuperAdmin()) { ?>        
        <li class="nav-item" data-toggle="tooltip" data-placement="right">
          <a class="nav-link nav-link-collapse collapsed" data-toggle="collapse" href="#collapseMulti" data-parent="#smartmittAccordion">
            <i class="fa fa-fw fa-sitemap"></i>
            <span class="nav-link-text">Administration</span>
          </a>
          <ul class="sidenav-second-level collapse" id="collapseMulti">
            <li>
              <a href="../admin/targets.php">Targets</a>
            </li>
            <li>
              <a href="../admin/demo.php">Demo Session</a>
            </li>
			<li>
              <a href="../students/SmUtil01.php">Self-Test LED/NDB</a>
            </li>
			<li>
              <a href="../students/SmUtil02.php">Update Local Practice Modes- Inet Conn Reqd!</a>
            </li>
			<li>
              <a href="../students/SmUtil03.php">Upload ALL COMPLETED Sessions- Inet Conn Reqd!</a>
            </li>
			<li>
              <a href="../students/SmUtil04.php">Camera Background View Refresh.</a>
            </li>
			<li>
              <a href="../students/SmUtil05.php">FUTURE: Set Camera Exposure (10-100)</a>
            </li>
			<li>
              <a href="../students/SmUtil06.php">Menu 6</a>
            </li>
			<li>
              <a href="../students/SmUtil07.php">Menu 7</a>
            </li>
			<li>
              <a href="../students/SmUtil08.php">Menu 8</a>
            </li>
			<li>
              <a href="../students/SmUtil09.php">Menu 9</a>
            </li>
			<li>
              <a href="../students/SmUtil10.php">Menu 10</a>
            </li>
          </ul>
        </li>
		
        <?php } ?>                       
      </ul>
      <ul class="navbar-nav sidenav-toggler">
        <li class="nav-item">
          <a class="nav-link text-left" id="sidenavToggler">
            <i class="fa fa-fw fa-angle-left"></i>
          </a>
        </li>
      </ul>
      <ul class="navbar-nav ml-auto">
        <li class="nav-item">
          <a class="nav-link"><?=GetStudentFirst().' '.GetStudentLast()?></a>
        </li>	      
        <li class="nav-item">
          <a class="nav-link" data-toggle="modal" data-target="#exampleModal">
            <i class="fa fa-fw fa-sign-out-alt"></i>Logout</a>
        </li>
      </ul>
    </div>
  </nav>
  <div class="content-wrapper">
    <div class="container-fluid">
        