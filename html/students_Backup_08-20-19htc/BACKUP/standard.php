<?php include_once "../includes/header.php"; ?>
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
                <h2>Select a Target</h2>
            </div>
        </div>
		<div class="row">
		    
		    <?php
              $db = ConnecttoDB();
              $sql = "SELECT DisplayTargetName, TargetGUID, JpgFileName FROM StandardTargetsForDropDownSelection";
              $sqlQuery = $db->query($sql);
              $result = $sqlQuery->fetchAll();

                foreach ($result as $row)
                {
                    ?>
                <div class="col-sm-6">
    				<div class="card">
    					<div class="card-body text-center bg-dark">
    						<h3 class="card-title text-light"><?php echo $row['DisplayTargetName']; ?></h3>
    						<img class="responsive mbt-40" src="../img/<?php echo $row['JpgFileName']; ?>"><br>
    						<a class="btn btn-outline-light mb-20" href="target_form.php?target=<?php echo $row['TargetGUID']; ?>">Select This Target</a>
    					</div>
    				</div>
			    </div>
                    <?php
                }
            ?>
		    
			<!--<div class="col-sm-6">
				<div class="card">
					<div class="card-body text-center bg-dark">
						<h3 class="card-title text-light">Target One</h3>
						<img class="responsive mbt-40" src="../img/ED%20Target.jpg"><br>
						<a class="btn btn-outline-light mb-20" href="#">Select This Target</a>
					</div>
				</div>
			</div>
			<div class="col-sm-6">
				<div class="card">
					<div class="card-body text-center bg-dark">
						<h3 class="card-title text-light">Target Two</h3>
						<img class="responsive mbt-40" src="../img/IM_Target.jpg"><br>
						<a class="btn btn-outline-light mb-20" href="#">Select This Target</a>
					</div>
				</div>
			</div>
		</div>
        <div class="row">
			<div class="col-sm-6">
				<div class="card">
					<div class="card-body text-center bg-dark">
						<h3 class="card-title text-light">Target Three</h3>
						<img class="responsive mbt-40" src="../img/PA_Target.jpg"><br>
						<a class="btn btn-outline-light mb-20" href="#">Select This Target</a>
					</div>
				</div>
			</div>
			<div class="col-sm-6">
				<div class="card">
					<div class="card-body text-center bg-dark">
						<h3 class="card-title text-light">Target Four</h3>
						<img class="responsive mbt-40" src="../img/SL_Target.jpg"><br>
						<a class="btn btn-outline-light mb-20" href="#">Select This Target</a>
					</div>
				</div>
			</div>
		</div>-->
	</div>


<?php include_once "../includes/footer.php"; ?>
