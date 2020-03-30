
<?php include_once "../includes/header.php"; ?>
<?php


//$command = escapeshellcmd("python /home/pi/SmMain.py");


//$output = shell_exec("cd ../../../../ SmMain.py");



//system("cd ../../../../../home/pi && sudo python SmMain.py");

if(isset($_POST['speed']))
{
	
    $result = BeginSessionnew($_POST);
    
    if($result != 'error')
    {   
   //      $output = CallPython("SmMain.py");

    // $command = escapeshellcmd("python /home/pi/" . $ScriptName);
         //echo "Calling SmMain.py ";
   // $command = escapeshellcmd("python /home/pi/SmMain.py");
    //$command = escapeshellcmd("python /var/www/html/students/SmMain.py");
   //     /var/www/html/students
    //	shell_exec("sudo python /home/pi/SmMain.py");
     //    echo "Called SmMain.py ".$command;


// 9-22-18 htc - this is where the SmMain.py is called, in home folder, /var/www/html/students 
//               I added $result below which is the session number just created by the PHP script in the MySql DB.

// $command = escapeshellcmd("python SmMain.py " . $result);
//  $output = shell_exec($command . " >/dev/null 2>/dev/null &");
 //shell_exec("python -i SmMain.py " . $result);

     //    echo "hello ".$output;
//$file = file_get_contents('../../../../../home/pi/SmMain.py', true);
//echo $file;


//	$command = escapeshellcmd("python ../../../../../home/pi/SmMain.py");
//    	$output = shell_exec($command);
//die('here');


$old_path = getcwd();
chdir("/var/www/html/students/");
// 10-07-18 htc - this is Kris' working code  $output = shell_exec("./SmMain.sh >/dev/null 2>/dev/null &");
// I tried to add the session ID no as a parameter similar to the code above - ". $result
$output = shell_exec("./SmMain.sh ". $result ." >/dev/null 2>/dev/null &");
chdir($old_path);

       header("Location: /students/pitches.php"); 
	
	}else{ echo "Something went wrong!!"; }

}
?>

      <!-- Breadcrumbs-->
      <ol class="breadcrumb">
        <li class="breadcrumb-item">
          <a href="#">Dashboard</a>
        </li>
        <li class="breadcrumb-item active">My Dashboard</li>
      </ol>
    <div class="container" id="target-options">
        <div class="row">
            <div class="col-sm-12 text-center">
                <div class="row">
                  <div class="col-sm-12 text-center">
                    <div class="card">
            					<div class="card-body text-center bg-dark">
            					    <button style="display:none;" class="btn btn-danger float-right" id="stop_session" data-toggle="modal" data-target="#stopmodal"><i class="fa fa-stop-circle" aria-hidden="true"></i> Stop</button>
            					   <style>
            					   <style>
* {
  box-sizing: border-box;
}

body {
  background-color: #f1f1f1;
}

#regForm {
  background-color: #ffffff;
  margin: 100px auto;
  font-family: Raleway;
  padding: 40px;
  width: 70%;
  min-width: 300px;
}

h1 {
  text-align: center;  
}

input {
  padding: 10px;
  width: 100%;
  font-size: 17px;
  font-family: Raleway;
  border: 1px solid #aaaaaa;
}

/* Mark input boxes that gets an error on validation: */
input.invalid {
  background-color: #ffdddd;
}

/* Hide all steps by default: */
.tab {
  display: none;
}

button {
  background-color: #4CAF50;
  color: #ffffff;
  border: none;
  padding: 10px 20px;
  font-size: 17px;
  font-family: Raleway;
  cursor: pointer;
}

button:hover {
  opacity: 0.8;
}

#prevBtn {
  background-color: #bbbbbb;
}

/* Make circles that indicate the steps of the form: */
.step {
  height: 15px;
  width: 15px;
  margin: 0 2px;
  background-color: #bbbbbb;
  border: none;  
  border-radius: 50%;
  display: inline-block;
  opacity: 0.5;
}

.step.active {
  opacity: 1;
}

/* Mark the steps that are finished and valid: */
.step.finish {
  background-color: #4CAF50;
}
</style>
<?php

  $db = ConnecttoDB();

  $AccountID = $_COOKIE["AccountID"];
  //exit();
  $sql1 = "SELECT * FROM sessions where AccountID='$AccountID' ORDER BY SeqSessionNumber DESC LIMIT 1";
  $sqlQuery1 = $db->query($sql1);
  $result = $sqlQuery1->fetchAll();
  $PracticeGUID = $result['0']['PracticeGUID'];

  $DisplaySpeedForSeconds = $result['0']['DisplaySpeedForSeconds'];
  $DisplayImpactForSeconds = $result['0']['DisplayImpactForSeconds'];
  $PitchingDistanceFeet = $result['0']['PitchingDistanceFeet'];
  $SuspendTimeOutSeconds = $result['0']['SuspendTimeOutSeconds'];
  $DisplayPitchCountBarsYN = $result['0']['DisplayPitchCountBarsYN'];
  $YverticalOffsetDeltaValue = $result['0']['YverticalOffsetDeltaValue'];
  $PracticeRepetitions = $result['0']['PracticeRepetitions'];

if($PracticeRepetitions == '') {
  $PracticeRepetitions = '0';
}

if($DisplaySpeedForSeconds != '') {
  $speed = $DisplaySpeedForSeconds;
}
else {
 $speed = '4'; 
}

if($DisplayImpactForSeconds != '') {
  $impact_speed = $DisplayImpactForSeconds;
}
else {
 $impact_speed = '4'; 
}

if($SuspendTimeOutSeconds != '') {
  $time_out = $SuspendTimeOutSeconds;
}
else {
 $time_out = '15'; 
}

if($YverticalOffsetDeltaValue != '') {
  $voffset = $YverticalOffsetDeltaValue;
}
else {
  $voffset = '0';
}

?>

<form id="regForm" action="" method="post">

	<input type="hidden" name="guid" value="<?php echo $_GET['target']; ?>" />

  <div class="col-md-12 session_input">Time to Show Speed Display (Secs):
    <p><input type="number" min="0" value="<?php echo $speed; ?>" max="20" name="speed"></p>
  </div>
  <div class="col-md-12 session_input">Time to Show Impact Location (Secs):
    <p><input type="number" min="0" value="<?php echo $impact_speed; ?>" max="20" name="impact_location"></p>
  </div>
  <div class="col-md-12 session_input">Vertical Target Adjustment +/- LED Rows (2.5” each):
    <p><input type="number" min="-3" value="0" max="<?php echo $voffset; ?>" name="led_rows"></p>
  </div>
  <div class="col-md-12 session_input" style="display:none;">Show the River on selected target Y/N:
    <p>
        <label class="radio-inline">
            <input type="radio" name="river_target">Yes
        </label>
        <label class="radio-inline">
           <input type="radio" name="river_target" checked="checked">No
        </label>
    </p>
  </div>
  <div class="col-md-12 session_input">Display Pitch Count Side Bars on LED Y/N:
    <p>
        <label class="radio-inline">
            <input type="radio" value="Y" name="pitch_count" <?php if($DisplayPitchCountBarsYN == 'Y') {echo 'checked="checked"'; }?>>Yes
        </label>
        <label class="radio-inline">
           <input type="radio" value="N" name="pitch_count" <?php if($DisplayPitchCountBarsYN == 'N') {echo 'checked="checked"'; }?>>No
        </label>
    </p>
  </div>
  <div class="col-md-12 session_input">No Pitch Time-Out for Auto-Suspend Session (mins):
    <p><input type="number" min="0" value="<?php echo $time_out; ?>" max="90" name="suspend_session"></p>
  </div>
  <div class="col-md-12 session_input">Pitching Distance in feet:
   <p>
        <label class="radio-inline">
            <input type="radio" name="piching_distance" <?php if($PitchingDistanceFeet == '30') {echo 'checked="checked"'; }?> value="30">30
        </label>
        <label class="radio-inline">
           <input type="radio" name="piching_distance" value="35" <?php if($PitchingDistanceFeet == '35') {echo 'checked="checked"'; }?>>35
        </label>
         <label class="radio-inline">
           <input type="radio" name="piching_distance" value="38" <?php if($PitchingDistanceFeet == '38') {echo 'checked="checked"'; }?>>38
        </label>
         <label class="radio-inline">
           <input type="radio" name="piching_distance" value="40" <?php if($PitchingDistanceFeet == '40') {echo 'checked="checked"'; }?>>40
        </label>
         <label class="radio-inline">
           <input type="radio" name="piching_distance" value="43" <?php if($PitchingDistanceFeet == '43') {echo 'checked="checked"'; }?>>43
        </label>
         <label class="radio-inline">
           <input type="radio" name="piching_distance" value="44" <?php if($PitchingDistanceFeet == '44') {echo 'checked="checked"'; }?>>44
        </label>
         <label class="radio-inline">
           <input type="radio" name="piching_distance" value="45" <?php if($PitchingDistanceFeet == '45') {echo 'checked="checked"'; }?>>45
        </label>
         <label class="radio-inline">
           <input type="radio" name="piching_distance" value="46" <?php if($PitchingDistanceFeet == '46') {echo 'checked="checked"'; }?>>46
        </label>
         <label class="radio-inline">
           <input type="radio" name="piching_distance" value="50" <?php if($PitchingDistanceFeet == '50') {echo 'checked="checked"'; }?>>50
        </label>
        <label class="radio-inline">
           <input type="radio" name="piching_distance" value="54" <?php if($PitchingDistanceFeet == '54') {echo 'checked="checked"'; }?>>54
        </label>
        <label class="radio-inline">
           <input type="radio" name="piching_distance" value="60" <?php if($PitchingDistanceFeet == '60') {echo 'checked="checked"'; }?>>60
        </label>
    </p>
  </div>

 <div class="col-md-12 session_input" style="display:none;">Number of Times to Repeat :
   <p>
        <label class="radio-inline">
            <input type="radio" name="PracticeRepetitions" value="1" <?php if($PracticeRepetitions == '1' || $PracticeRepetitions == '0') {echo 'checked="checked"'; }?>>1
        </label>
        <label class="radio-inline">
           <input type="radio" name="PracticeRepetitions" value="2" <?php if($PracticeRepetitions == '2') {echo 'checked="checked"'; }?>>2
        </label>
         <label class="radio-inline">
           <input type="radio" name="PracticeRepetitions" value="3" <?php if($PracticeRepetitions == '3') {echo 'checked="checked"'; }?>>3
        </label>
         <label class="radio-inline">
           <input type="radio" name="PracticeRepetitions" value="4" <?php if($PracticeRepetitions == '4') {echo 'checked="checked"'; }?>>4
        </label>
         <label class="radio-inline">
           <input type="radio" name="PracticeRepetitions" value="5" <?php if($PracticeRepetitions == '5') {echo 'checked="checked"'; }?>>5
        </label>
         <label class="radio-inline">
           <input type="radio" name="PracticeRepetitions" value="6" <?php if($PracticeRepetitions == '6') {echo 'checked="checked"'; }?>>6
        </label>
         <label class="radio-inline">
           <input type="radio" name="PracticeRepetitions" value="7" <?php if($PracticeRepetitions == '7') {echo 'checked="checked"'; }?>>7
        </label>
         <label class="radio-inline">
           <input type="radio" name="PracticeRepetitions" value="8" <?php if($PracticeRepetitions == '8') {echo 'checked="checked"'; }?>>8
        </label>
         <label class="radio-inline">
           <input type="radio" name="PracticeRepetitions" value="9" <?php if($PracticeRepetitions == '9') {echo 'checked="checked"'; }?>>9
        </label>
        <label class="radio-inline">
           <input type="radio" name="PracticeRepetitions" value="10" <?php if($PracticeRepetitions == '10') {echo 'checked="checked"'; }?>>10
        </label>
    </p>
  </div>






    <div style="overflow:auto;">
    <div class="regform_buttons">
      <button type="submit" id="nextBtn">START PITCHING</button> <span class='or-span'>OR</span> 
      <button type="button" id="backBtn" onclick="window.history.back()">BACK</button> <span class='or-span'>OR</span>
      <button type="button" id="cancleBtn" data-toggle="modal" data-target="#exampleModal">CANCEL/LOGOUT</button>
    </div>
  </div>
</form>


            						<!--<h3 class="card-title text-light targetTitle"></h3>
            						<img class="responsive img-fluid mbt-40 targetImage" src="" ><br>-->
            						<!--<a class="btn btn-outline-light mb-20" id="beginSession" href="#">Begin Session</a>-->
            					</div>
            				</div>
                    <!-- <button class="btn btn-primary" id="beginSession" style="margin-top:10px;">Begin Session</button> -->
                  </div>
                </div>
            </div>
        </div>
	</div>

<!--Stop Modal-->
<div class="modal fade show" id="stopmodal" tabindex="-1" role="dialog" aria-labelledby="stopModalLabel">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="stopModalLabel">Please choose below action.</h5>
            <button class="close" type="button" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">×</span>
            </button>
          </div>
          <div class="modal-body">
              <div class="form-group">
                <select class="form-control" name="stop-option" id="stop-option-select">
                  <option value="SUSPENDED">Suspend for Later</option>
                  <option value="COMPLETED">Save and Upload Pitch Data</option>
                  <option value="CANCELLED">Cancel/Delete Data</option>
                </select>
              </div>
              <button type="submit" class="float-right" id="stop-action-submit">SUBMIT</submit>
          </div>
        </div>
      </div>
</div>

<?php include_once "../includes/footer.php"; ?>
<script>

$('#stop-action-submit').click(function(){
    var check = false;
    var select_val = $('#stop-option-select').val();
    $('#stopmodal').modal('hide');
    /*if(select_val == 'delete'){
        var con = confirm('Are you sure again for cancel/delete.');
        if(con){
            check = true;
        }
    }else{
        check = true;
    }
    
    if(check){*/
    $.ajax({
      type: "POST",
      url: "write_log.php",
      data: { val : select_val },
       success: function(response) { 
       var response = $.trim(response);              
           if(response == 'ok'){
              /*location.reload();*/
              window.location.href = '/students/standard.php';
           }else{
               alert('Some error occured please try again');
           }
           
       }              
      });
    //}
    
});
</script>