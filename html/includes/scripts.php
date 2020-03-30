<script type="text/javascript" src="/vendor/jquery/jquery.min.js"></script>
  <script type="text/javascript" src="/vendor/bootstrap/js/bootstrap.bundle.min.js"></script>
  <script type="text/javascript" src="/vendor/jquery-easing/jquery.easing.min.js"></script>
  <script type="text/javascript" src="/vendor/jquery.growl/javascripts/jquery.growl.js"></script> 
  <script type="text/javascript">  
   $(document).ready(function(){     
    var resultmmsg = '<?=$result?>'; 
	if (resultmmsg != '' && resultmmsg != 'Logged Out!') {
      $.growl.error({ message: resultmmsg });
	} 	                         
   });
  </script> 	  