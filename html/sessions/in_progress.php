<?php include_once $_SERVER['DOCUMENT_ROOT']."/includes/header.php"; ?>
      <!-- Breadcrumbs-->
      <ol class="breadcrumb">
        <li class="breadcrumb-item">
          <a href="#">Dashboard</a>
        </li>
        <li class="breadcrumb-item active">My Dashboard</li>
      </ol>
    <div class="container" id="in-progresds-session">
        <div class="row">
            <div class="col-sm-12 text-center">
                <h2>In Progress</h2>
            </div>
        </div>
		<div class="row">
			<div class="col-sm-6">
				
			</div>
			<div class="col-sm-6">
			
			</div>
		</div>
	</div>

<?php include_once $_SERVER['DOCUMENT_ROOT']."/includes/footer.php"; ?>
<script>
    window.setInterval(function(){
    /// call php function to check for pitch here
    }, 5000);
</script>