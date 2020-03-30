<?php include_once "../includes/header.php"; ?>
<?php
if(isset($_POST['speed']))
{
    $result = BeginSessionnewPractice($_POST);

    if($result != 'error')
    {   

//echo $_SERVER['DOCUMENT_ROOT'];    
        
    //$command = escapeshellcmd('python  '.$_SERVER['DOCUMENT_ROOT'].'/scripts/whatever.py '.$result);
    //$output = shell_exec($command);
        //echo $d = CallPython("whaterver.py" . $result);

//$command = escapeshellcmd("sudo python SmMain.py " . $result);
  // $output = shell_exec($command . " >/dev/null 2>/dev/null &");


$command = escapeshellcmd("sudo SmMain.sh");
//chdir("/var/www/html/students/");
//putenv("PATH=/home/pi/:" .$_ENV["PATH"]."");

$old_path = getcwd();
chdir("/var/www/html/students/");
// 10-07-18 htc - this is Kris' working code  $output = shell_exec("./SmMain.sh >/dev/null 2>/dev/null &");
// I tried to add the session ID no as a parameter similar to the code above - ". $result
$output = shell_exec("./SmMain.sh ". $result ." >/dev/null 2>/dev/null &");

chdir($old_path);


    header("Location: /students/pitches.php"); }else{ ?><script> alert('Something Went Wrong.'); </script><?php }
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
<form id="regForm" action="" method="post">
            <div class="col-sm-12 text-center">
                <h2>Practice Session Targets</h2>
                <div class="row">
                  <div class="col-md-4" style="margin: 0px auto;">
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

                      //$sql = "SELECT PracticeGUID, DisplayPracticeName FROM PracticeRoutinesForDropDownSelect";
		      $sql = "SELECT AccountID,CoachID1,CoachID2,CoachID3,CoachID4,CoachID5,CoachID6,CoachID7,CoachID8,CreatedByCoachID,DisplayPracticeName,PracticeGUID FROM smartmitt.LocalUsers INNER JOIN smartmitt.PracticeRoutinesForDropDownSelect on CoachID1=CreatedByCoachID or CoachID2=CreatedByCoachID or CoachID3=CreatedByCoachID or CoachID4=CreatedByCoachID or CoachID5=CreatedByCoachID or CoachID6=CreatedByCoachID or CoachID7=CreatedByCoachID or CoachID8=CreatedByCoachID where AccountID='$AccountID'";
                      $sqlQuery = $db->query($sql);
                      $result = $sqlQuery->fetchAll();
                      echo "<select id='practiceTarget' class='form-control mbt-20' name='practiceTarget'>";
                      echo "<option selected disabled hidden>Select a target...</option>";
                        foreach ($result as $row)
                        {
                          if($PracticeGUID == $row['PracticeGUID']) {
                            $selected = "selected='selected'";
                          }
                          else {
                           $selected = ""; 
                          }
                          echo "<option value='" . $row['PracticeGUID'] . "' ".$selected.">" . $row['DisplayPracticeName'] . "</option>";
                        }
                      echo "</select>";
                    ?>
                    </div>
                      </div>
                <div class="row">
                  <div class="col-sm-12 text-center choose_target">
                    <div class="card choose_target_card" style="display:none;">
            					<div class="card-body text-center bg-dark choose_target_card_body">
            					    <button style="display:none;" class="btn btn-danger float-right" id="stop_session" data-toggle="modal" data-target="#stopmodal"><i class="fa fa-stop-circle" aria-hidden="true"></i> Stop</button>
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
<!--<form id="regForm" action="" method="post">-->
<!--  <h1>Register:</h1>-->
  <!-- One "tab" for each step in the form: -->
  <!--<div class="tab">Time to Show Speed Display (Secs):
    <p><input type="number" min="0" value="4" max="20" oninput="this.className = ''" name="speed"></p>
  </div>
  <div class="tab">Time to Show Impact Location (Secs):
    <p><input type="number" min="0" value="4" max="20" oninput="this.className = ''" name="impact_location"></p>
  </div>
  <div class="tab">Vertical Target Adjustment +/- LED Rows (2.5” each):
    <p><input type="number" min="-3" value="0" max="3" oninput="this.className = ''" name="led_rows"></p>
  </div>
  <div class="tab">Show the River on selected target Y/N:
    <p>
        <label class="radio-inline">
            <input type="radio" oninput="this.className = ''" name="river_target">Yes
        </label>
        <label class="radio-inline">
           <input type="radio" oninput="this.className = ''" name="river_target" checked="checked">No
        </label>
    </p>
  </div>
  <div class="tab">Display Pitch Count Side Bars on LED Y/N:
    <p>
        <label class="radio-inline">
            <input type="radio" oninput="this.className = ''" name="pitch_count">Yes
        </label>
        <label class="radio-inline">
           <input type="radio" oninput="this.className = ''" name="pitch_count" checked="checked">No
        </label>
    </p>
  </div>
  <div class="tab">No Pitch Time-Out for Auto-Suspend Session (mins):
    <p><input type="number" min="0" value="15" max="90" oninput="this.className = ''" name="suspend_session"></p>
  </div>
  <div class="tab">Pitching Distance in feet:
   <p>
        <label class="radio-inline">
            <input type="radio" oninput="this.className = ''" name="piching_distance" checked="checked">30
        </label>
        <label class="radio-inline">
           <input type="radio" oninput="this.className = ''" name="piching_distance">60
        </label>
    </p>
  </div>
  <div style="overflow:auto;">
    <div style="float:right;">
      <button type="button" id="prevBtn" onclick="nextPrev(-1)">Previous</button>
      <button type="button" id="nextBtn" onclick="nextPrev(1)">Next</button>
    </div>
  </div>
  <!-- Circles which indicates the steps of the form: -->
<!--  <div style="text-align:center;margin-top:40px;">
    <span class="step"></span>
    <span class="step"></span>
    <span class="step"></span>
    <span class="step"></span>
    <span class="step"></span>
    <span class="step"></span>
    <span class="step"></span>
  </div>
</form>-->



  <div class="col-md-12 session_input">Time to Show Speed Display (Secs):
    <p><input type="number" min="0" value="<?php echo $speed; ?>" max="20" name="speed"></p>
  </div>
  <div class="col-md-12 session_input">Time to Show Impact Location (Secs):
    <p><input type="number" min="0" value="<?php echo $impact_speed; ?>" max="20" name="impact_location"></p>
  </div>
  <div class="col-md-12 session_input">Vertical Target Adjustment +/- LED Rows (2.5” each):
    <p><input type="number" min="-3" value="<?php echo $voffset; ?>" max="3" name="led_rows"></p>
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
 
 <div class="col-md-12 session_input">Number of Times to Repeat :
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



<script>
/*var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the crurrent tab

function showTab(n) {
  // This function will display the specified tab of the form...
  var x = document.getElementsByClassName("tab");
  x[n].style.display = "block";
  //... and fix the Previous/Next buttons:
  if (n == 0) {
    document.getElementById("prevBtn").style.display = "none";
  } else {
    document.getElementById("prevBtn").style.display = "inline";
  }
  if (n == (x.length - 1)) {
    document.getElementById("nextBtn").innerHTML = "START PITCHING";
  } else {
    document.getElementById("nextBtn").innerHTML = "Next";
  }
  //... and run a function that will display the correct step indicator:
  fixStepIndicator(n)
}

function nextPrev(n) {
  // This function will figure out which tab to display
  var x = document.getElementsByClassName("tab");
  // Exit the function if any field in the current tab is invalid:
  if (n == 1 && !validateForm()) return false;
  // Hide the current tab:
  x[currentTab].style.display = "none";
  // Increase or decrease the current tab by 1:
  currentTab = currentTab + n;
  // if you have reached the end of the form...
  if (currentTab >= x.length) {
    // ... the form gets submitted:
    document.getElementById("regForm").submit();
    return false;
  }
  // Otherwise, display the correct tab:
  showTab(currentTab);
}*/

function validateForm() {
  // This function deals with validation of the form fields
  var x, y, i, valid = true;
  x = document.getElementsByClassName("tab");
  y = x[currentTab].getElementsByTagName("input");
  // A loop that checks every input field in the current tab:
  for (i = 0; i < y.length; i++) {
    // If a field is empty...
    if (y[i].value == "") {
      // add an "invalid" class to the field:
      y[i].className += " invalid";
      // and set the current valid status to false
      valid = false;
    }
  }
  // If the valid status is true, mark the step as finished and valid:
  if (valid) {
    document.getElementsByClassName("step")[currentTab].className += " finish";
  }
  return valid; // return the valid status
}

function fixStepIndicator(n) {
  // This function removes the "active" class of all steps...
  var i, x = document.getElementsByClassName("step");
  for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(" active", "");
  }
  //... and adds the "active" class on the current step:
  x[n].className += " active";
}
</script>
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
<script>
  $('#beginSession').click(function() {
    $.ajax({
      type: "POST",
      url: "start-session.php",
      data: { session_type: "practice", target_guid: "1234" }
      }).success(function( msg ) {
      <?php
      $sessionId = msg;
      // launches the pitching workout session
      CallPython('whaterver.py ' . $sessionId)
      ?>;
      alert(msg);
     // window.location = 'pitches.php'
    });
  });


</script>
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
                <input type="hidden" value="<?php echo $_COOKIE["AccountID"]; ?>" id="account_id" />
              </div>
              <button type="submit" class="float-right" id="stop-action-submit">SUBMIT</submit>
          </div>
        </div>
      </div>
</div>

<?php include_once "../includes/footer.php"; ?>

<script>


  $('#practiceTarget').change(function() {
    $(".targetImage").attr("src","../img/practice/" + $(this).val() + ".jpg");
    $(".card").show();
  });




$('#stop-action-submit').click(function(){
    var check = false;
    var select_val = $('#stop-option-select').val();
    var account_id = $("#account_id").val();
    $('#stopmodal').modal('hide');
    /*if(select_val == 'delete'){
        var con = confirm('Are you sure again for cancel/delete.');
        if(con){
            check = true;
        }
    }else{
        check = true;
    }*/
    
    //if(check){
    $.ajax({
      type: "POST",
      url: "write_log.php",
      data: { val : select_val, account_id:account_id },
       success: function(response) {               
           if(response == 'ok'){
              location.reload();
           }else{
               alert('Some error occured please try again');
           }
           
       }              
      });
    //}
    
});
</script>