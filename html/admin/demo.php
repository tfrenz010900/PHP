<?php 
  include_once $_SERVER['DOCUMENT_ROOT']."/includes/header.php"; 
  if(!IsSuperAdmin()) {
	header("Location: /?result=Unauthorized"); 
	
	//loop process, forked from cron or boot
	  //Look for speed.txt file, if found spawn run function
	  //Run fucntion opens speed.txt, parses speed and http calls the render_ledmatrix.php
	  //Wait 4 seconds, look for file function(Locatefile) to see cam1.cam2 image files. when found call the analysis function
	  //look for impact text file, when found, open parse and pass to impact display function
	  //impact display function will call render_ledmatrix.php file
	  //archive cam files, impact file, reset function
	  //NoPitch file resets function






	
//	do {
//     if (file_exists("test.txt")) {
//
//        break;
//     }
//    } while(true);
//	$cam1_file = Locatefile($home_dir,$cam1_file_string);
//	$cam2_file = Locatefile($home_dir,$cam2_file_string);
//	
//	if(file_exists($cam1_file && $cam2_file)) {  
//      if (file_exists($leddriverscript_file)) {
//        $output = exec($analysis_script);
//      }
//    }
//    $impact_file = Locatefile($home_dir,$impact_file_string);
	
	 
  } 
 ?>
 <!-- Breadcrumbs-->
 <ol class="breadcrumb">
   <li class="breadcrumb-item">
     <a href="/admin.php">Dashboard</a>
   </li>
   <li class="breadcrumb-item active">admin/Demo</li>
 </ol> 
<script type="text/javascript"> 
  $(document).ready(function(){	    
     $("#slider").slider({
      value:10,
      min: 10,
      max: 110,
      step: 1,
      slide: function( event, ui ) {
        $("#chosenspeed").val(ui.value);
        $("#chosenspeed_txt").text(ui.value+" Mph");
      }
    });

  });
</script>
  <input type="hidden" name="chosenspeed" id="chosenspeed" value="10">
   <div class="row">	
    <div class="col-2">Step 1 (Target)</div>  
    <div class="col-10">
		 <select class="form-control" name="defaulttarget" id="defaulttarget" style="margin-bottom:20px;">
			 <option value="1,1|30,26|000000">Clear</option>
			 <option value="target1">EarlyDev</option>			 
			 <option value="target2">Intermediate</option>			 
			 <option value="target3">Select Develop</option>
			 <option value="target4">Pitch Advantage</option>		 				 				 		 			 			 
		 </select>	    	    
    </div>  
   </div>
   <div class="row">	
    <div class="col-2">Step 2 (Ball Speed)</div>  
    <div class="col-8"><div id="slider"></div></div> 
    <div class="col-1"><span id="chosenspeed_txt"></span></div>  
   </div>   
   <div class="row">	
    <div class="col-2">Step 3 (Hit/Miss)</div>  
    <div class="col-10">
		 <select class="form-control" name="misshit" id="misshit" style="margin-bottom:20px;">
			 <option value="1">Hit (random)</option>
			 <option value="2">Hit (choose)</option>			 
			 <option value="3">Miss (random)</option>			 
			 <option value="4">Miss (choose)</option>				 				 		 			 			 
		 </select>	  	    
	</div>  
   </div> 
   <div class="row">	
    <div class="col-2">Step 4 (Pitch)</div>  
    <div class="col-10 text-left"><button id="pitch_btn" type="button" class="btn btn-success">Pitch!</button></div>  
   </div>         
   <div class="row">	
    <div class="col-2"><br/>Results</div>  
    <div class="col-10 text-left"><br/><textarea class="form-control"  name="results_out" id="results_out"></textarea></div>  
   </div>       
<?php include_once $_SERVER['DOCUMENT_ROOT']."/includes/footer.php"; ?>