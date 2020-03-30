<?php 
  include_once $_SERVER['DOCUMENT_ROOT']."/includes/header.php"; 
  if(!IsSuperAdmin()) {
	header("Location: /?result=Unauthorized");  
  } 
 ?>
 <!-- Breadcrumbs-->
 <ol class="breadcrumb">
   <li class="breadcrumb-item">
     <a href="/admin.php">Dashboard</a>
   </li>
   <li class="breadcrumb-item active">admin/Targets</li>
 </ol>
<style>
.rowwidth {
  min-width: 10px;   	
}
.rowheight {
  min-height: 10px;   	
}
</style> 
<script type="text/javascript"> 
  var chosencolor = "f00000";
  var pixelcolorstring = '';
  var isMouseDown = false;
  var isHighlighted = false; 
  var totalleds = <?=$totalleds?>; 
  var matrixrefresh = <?=$matrixrefreshrate?>; 	
  $(document).ready(function(){	
     $(document)
       .on("mousedown",".cellpixel",function () {
         isMouseDown = true;
         $(this).toggleClass("highlighted");
         isHighlighted = $(this).hasClass("highlighted");
	       if(isHighlighted) {
		     $(this).css('background-color',"#"+chosencolor);
		     $(this).data('bgcolor',chosencolor);
	       } else {
		     $(this).css('background-color',"#ffffff");
		     $(this).data('bgcolor',"000000");  
	       }          
         return false;
       })
       .on("mouseover",".cellpixel",function () {
         if (isMouseDown) {
           $(this).toggleClass("highlighted", isHighlighted);	         
	       if(isHighlighted) {
		     $(this).css('background-color',"#"+chosencolor);
		     $(this).data('bgcolor',chosencolor); 		     
	       } else {
		     $(this).css('background-color',"#ffffff");
		     $(this).data('bgcolor',"000000"); 
	       }  	                 
         }
      });
  
    $(document).mouseup(function () {
      isMouseDown = false;      
    });    
    
    $(".pixelcolor").on("click", function(event) {
	   $(".pixelcolor").removeClass('activecell');
	   $(this).addClass('activecell');
	   chosencolor = $(this).data('colorchip');
	           
    });
    
    $("#defaulttarget").on("change", function(event) {
     $("#pixeldata").val($(this).val());
     PaintLedGrid($("#pixeldata").val());	           
    });  
    
    $("#serializematrix").on("click", function(event) {
      SerializePixelMap(); 
    });
    
	$("#paintgrid").on("click", function(event) {
		event.preventDefault();
		PaintLedGrid($("#pixeldata").val());       		 
	 });     

	$("#postspeed").on("click", function(event) {
		event.preventDefault();
		PaintLedGrid("speed="+$("#chosenspeed").val());       		 
	 });       

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
    $("#chosenspeed").val("10");
    $("#chosenspeed_txt").text("10 Mph");    
     
     PaintLedGrid('load'); 
     var screenrendertimer = setInterval(function(){ PaintLedGrid('load');  }, matrixrefresh);
  });
  
  
 function SerializePixelMap() {
   pixelcolorstring = '';
   for (i = 0; i <= totalleds; i++) {
    pixelcolorstring += $("#cell_"+i).data('bgcolor');
   } 
   $("#pixeldata_out").val(pixelcolorstring); 		 
 }
 
 function PaintLedGrid(inpixdata) {
   $.ajax({
       method: "POST",
       async: true,
       url: '/screen/render_ledmatrix.php',
       data: ({'pixeldata' : inpixdata}),
       cache:false,		
       success: function (data) {
        $("#ledgrid").html(data);
       }
   });	 	 
 } 
</script> 
  <table class="PixelTable">
	<tbody>
	 <tr>
	  <td class="pixelcolor activecell" data-colorchip="f00000" style="background-color:#f00000"></td>
	  <td class="pixelcolor" data-colorchip="900000" style="background-color:#900000"></td>
	  <td class="pixelcolor" data-colorchip="400000" style="background-color:#400000"></td>	  
	  <td class="pixelcolor" data-colorchip="00f000" style="background-color:#00f000"></td>	  
	  <td class="pixelcolor" data-colorchip="009000" style="background-color:#009000"></td>	  
	  <td class="pixelcolor" data-colorchip="004000" style="background-color:#004000"></td>	  
	  <td class="pixelcolor" data-colorchip="0000f0" style="background-color:#0000f0"></td>	  
	  <td class="pixelcolor" data-colorchip="000090" style="background-color:#000090"></td>	  
	  <td class="pixelcolor" data-colorchip="000040" style="background-color:#000040"></td>	  
	  <td class="pixelcolor" data-colorchip="f0f000" style="background-color:#f0f000"></td>	  
	  <td class="pixelcolor" data-colorchip="909000" style="background-color:#909000"></td>	  
	  <td class="pixelcolor" data-colorchip="404000" style="background-color:#404000"></td>	  
	  <td class="pixelcolor" data-colorchip="f0f0f0" style="background-color:#f0f0f0"></td>	  
	  <td class="pixelcolor" data-colorchip="909090" style="background-color:#909090"></td>	  
	  <td class="pixelcolor" data-colorchip="404040" style="background-color:#404040"></td>	
	  <td class="pixelcolor" data-colorchip="000000" style="background-color:#000000"></td>
	  <td style="width:50px;"><button id="serializematrix" type="button" class="btn btn-primary btn-sm">Serialize</button></td>
	  <td style="width:150px;">
		 <select class="form-control" name="defaulttarget" id="defaulttarget">
			 <option value="1,1|30,26|000000">Clear</option>
			 <option value="target1">EarlyDev</option>			 
			 <option value="target2">Intermediate</option>			 
			 <option value="target3">Select Develop</option>
			 <option value="target4">Pitch Advantage</option>
			 <option value="3,1|28,26|f00000">All Red</option>	
			 <option value="3,1|28,26|00f000">All Green</option>				 
			 <option value="3,1|28,26|0000f0">All Blue</option>
			 <option value="3,1|28,26|f0f0f0">All White</option>
			 <option value="speed=77">77 Mph</option>				 
			 <option value="speed=68">68 Mph</option>				 
			 <option value="speed=59">59 Mph</option>				 				 				 		 			 			 
		 </select>
	  </td>
	  <td style="width:160px;"><input class="form-control" type="text" name="pixeldata" id="pixeldata" value="1,1|26,26|000000"></td>	
	  <td style="width:50px;"><button id="paintgrid" type="button" class="btn btn-primary btn-sm">Paint</button></td>		   	  
	 </tr>
	 <tr>
	   <td colspan="19"><div id="slider"></div></td>
       <td style="width:50px;">
	     <input type="hidden" name="chosenspeed" id="chosenspeed" value="10">
	     <button id="postspeed" type="button" class="btn btn-primary btn-sm"><span id="chosenspeed_txt">Paint Speed</span></button>
	   </td>
	 </tr>
	 <tr>
	   <td colspan="20"><textarea class="form-control"  name="pixeldata_out" id="pixeldata_out"></textarea></td>
	 </tr>	 	 
	</tbody>
  </table>
  <div id="ledgrid"></div>
<?php include_once $_SERVER['DOCUMENT_ROOT']."/includes/footer.php"; ?>