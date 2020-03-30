<?php
ob_start();
$bypasslogin = true;
include_once $_SERVER['DOCUMENT_ROOT']."/includes/functions_inc.php";
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
<style>
table.PixelTable {
  border: 0px solid #f5f5f5;
  border-spacing: 3px 13px;
  border-collapse: separate;  
  background-color: #ffffff;
  text-align: center;
  padding: 0px 0px;
  width:100%;
}
table.PixelTable td, table.PixelTable th {
  border: 1px solid #cccccc;
  padding: 2px 0px;
  width: 20px;
  height: 20px;  
}
table.PixelTable tbody td {
  font-size: 10px;
}
table.PixelTable td.highlighted {

}
.activecell {
  border: 3px solid #000000 !important;   
}
.rowwidth {
  min-width: 20px;   	
}
.rowheight {
  min-height: 30px;   	
}	
</style>
</head>
<body class="bg-dark">    
  <div class="container">
   <div class="row">	
    <div class="col-12">	  
      <div id="ledgrid"></div>
    </div>
   </div>
  </div>
  <script type="text/javascript" src="/vendor/jquery/jquery.min.js"></script>
  <script type="text/javascript" src="/vendor/bootstrap/js/bootstrap.bundle.min.js"></script>
  <script type="text/javascript" src="/vendor/jquery-easing/jquery.easing.min.js"></script>
  <script type="text/javascript" src="/vendor/jquery.growl/javascripts/jquery.growl.js"></script> 
  <script type="text/javascript">  
  var matrixrefresh = <?=$matrixrefreshrate?>; 
  	  matrixrefresh = 1200; //Quicker override	   
 $(document).ready(function(){ 
     PaintLedGrid('load'); 
     var screenrendertimer = setInterval(function(){ PaintLedGrid('load');  }, matrixrefresh);         
 });
 function PaintLedGrid(inpixdata) {
   $.ajax({
       method: "POST",
       async: true,
       url: '/screen/render_ledmatrix.php',
       data: ({'pixeldata' : inpixdata,'showpixelcelltxt' : 0}),
       cache:false,		
       success: function (data) {
        $("#ledgrid").html(data);
       }
   });	 	 
 }    
  </script>      
</body>
</html>
