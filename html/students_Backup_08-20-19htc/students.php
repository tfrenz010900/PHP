<?php include_once $_SERVER['DOCUMENT_ROOT']."/includes/header.php"; ?>
      <!-- Breadcrumbs-->
      <ol class="breadcrumb">
        <li class="breadcrumb-item">
          <a href="#">Dashboard</a>
        </li>
        <li class="breadcrumb-item active">My Dashboard</li>
      </ol>
    <div class="container" id="practice-options">
        <div class="row">
            <div class="col-sm-12 text-center">
                <h2>Select a Session</h2>
            </div>
        </div>
		<div class="row">
			<div class="col-sm-6">
				<div class="card">
					<div class="card-body text-center bg-success">
						<h3 class="card-title text-light">Standard Session</h3>
						<p class="card-text text-light">Standard pre-defined targets.</p><a href="targets.php"><i class="fas fa-baseball-ball text-light mbt-40" style="font-size:172px;"></i></a><br>
						<a class="btn btn-outline-light mb-20" href="standard.php">Start a Standard Session</a>
					</div>
				</div>
			</div>
			<div class="col-sm-6">
				<div class="card">
					<div class="card-body text-center bg-danger">
						<h3 class="card-title text-light">Practice Session</h3>
						<p class="card-text text-light">Custom targets defined by your coach.</p><a href="#"><i class="fas fa-baseball-ball text-light mbt-40" style="font-size:172px;"></i></a><br>
						<a class="btn btn-outline-light mb-20" href="practice.php">Start a Practice Session</a>
					</div>
				</div>
			</div>
		</div>
	</div>

	
<?php
 $db = ConnecttoDB();
$AccountID = $_COOKIE["AccountID"];
        
        $sql1 = "SELECT Status, id FROM sessions WHERE AccountID='$AccountID' ORDER BY id DESC LIMIT 1";
    $sqlQuery = $db->query($sql1);
    $result = $sqlQuery->fetchAll();
    $last_status = $result['0']['Status'];
$last_id= $result['0']['id'];

if(($last_status == 'SUSPENDED' || $last_status == 'NEW' || $last_status == 'OPEN' ) && $_GET['logout'] == '') {
    ?>
    <script>
        $(document).ready(function() {
             $("#stopmodal").modal('show');
        });
       
    </script>
    <?php
}

?>
	

<!--Stop Modal-->

<div class="modal fade show" id="stopmodal" tabindex="-1" role="dialog" aria-labelledby="stopModalLabel">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="stopModalLabel">Your last session was suspended. Please choose your action from below options.</h5>
            <button class="close" type="button" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">×</span>
            </button>
          </div>
          <div class="modal-body">
              <div class="form-group">
                <select class="form-control" name="stop-option" id="stop-option-select">
                  <option value="CONTINUE">Resume</option>
                  <option value="ABORT">Cancel</option>
                  <option value="COMPLETED">Close/Update Session</option>
                </select>
                <input type="hidden" value="<?php echo $_COOKIE["AccountID"]; ?>" id="account_id" />
              </div>
              <button type="submit" class="float-right" id="stop-action-submit">SUBMIT</submit>
          </div>
        </div>
      </div>
</div>	
	

<script>

$('#stop-action-submit').click(function(){
    var check = false;
    var select_val = $('#stop-option-select').val();
    var account_id = $("#account_id").val();
    $('#stopmodal').modal('hide');
    if(select_val == 'ABORT'){
        var con = confirm('Are you sure again for abort session.');
        if(con){
            check = true;
        }
    }else{
        check = true;
    }
    
    if(check){
    $.ajax({
      type: "POST",
      url: "write_log.php",
      data: { val : select_val},
       success: function(response) {  
//alert(response);             
           if(response == 'ok'){
              /*location.reload();*/
              window.location.href = '/students/students.php';
           }
	else if(response == 'CONTINUE') {
	window.location.href = '/students/pitches.php';
}
		else{
               alert('Some error occured please try again');
           }
           
       }              
      });
    }
    
});
</script>

<?php include_once $_SERVER['DOCUMENT_ROOT']."/includes/footer.php"; ?>
