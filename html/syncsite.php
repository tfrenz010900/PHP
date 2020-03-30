<?php
ob_start();
$bypasslogin = true;
include_once $_SERVER['DOCUMENT_ROOT']."/includes/functions_inc.php";

  $up = get_http_response_code($cloud_site); //Verify Access to EasyInsights, toggle local/remote login
  
  $up = false; //Temporary Override, validate EasyInsights API Process
  
  
  if($up) {
	$db = ConnecttoDB();
	$EasyInsightsUser = EasyInsightsUser('');
	$insightobj = json_decode($EasyInsightsUser);
	$collectedids = '';
	foreach ($insightobj as $easyuser) { 
     if(isset($easyuser->AccountID) && !empty($easyuser->StudentEmail)) { 
      $recid = 0;
      $isactive = ($easyuser->Active == 'Yes') ? 1 : 0;	      	                          
      $AccountID = $easyuser->AccountID;
      $StudentFirst = $easyuser->StudentFirst;
      $StudentLast = $easyuser->StudentLast;
      $StudentNickname =$easyuser->StudentNickname;
      $StudentEmail = $easyuser->StudentEmail;	
      $StudentPassword = md5($easyuser->StudentPassword);	
      $Sport = $easyuser->Sport;
      $CompLevel = $easyuser->{'Comp Level'};
      $rightleft = $easyuser->{'Right/Left'};
      $StudentGender = $easyuser->StudentGender;
      $StudentDOB = $easyuser->StudentDOB;	
        //Sync Users
        $sql = "SELECT * FROM users WHERE StudentEmail = '".$StudentEmail."' AND StudentPassword = '".$StudentPassword."' LIMIT 1;";   
        $sqlQuery = $db->query($sql);
        $result_user = $sqlQuery->fetchAll(); 
        $count = $sqlQuery->rowCount();
        if ($count == 0) { //Add New user to local db
         $sql_insert = "INSERT INTO users (AccountID,Active,rightleft,StudentFirst,StudentLast,StudentNickname,StudentDOB,StudentGender,StudentPassword,StudentEmail,Sport,Complevel) VALUES (:AccountID,:Active,:rightleft,:StudentFirst,:StudentLast,:StudentNickname,:StudentDOB,:StudentGender,:StudentPassword,:StudentEmail,:Sport,:Complevel)";
         $q = $db->prepare($sql_insert);      
         $q->execute(array(':AccountID'=>$AccountID,':Active'=>$isactive,':rightleft'=>$rightleft,':StudentFirst'=>$StudentFirst,':StudentLast'=>$StudentLast,':StudentNickname'=>$StudentNickname,':StudentDOB'=>$StudentDOB,':StudentGender'=>$StudentGender,':StudentPassword'=>$StudentPassword,':StudentEmail'=>$StudentEmail,':Sport'=>$Sport,':Complevel'=>$CompLevel));	        
	     $recid = $db->lastInsertId();
	    } else { //Update Records on local db from Easy-Insights
		 $recid = $result_user[0]['id'];
	     $q = $db->prepare("UPDATE users set AccountID=?,Active=?,rightleft=?,StudentFirst=?,StudentLast=?,StudentNickname=?,StudentDOB=?,StudentGender=?,StudentPassword=?,StudentEmail=?,Sport=?,Complevel=? WHERE id=?");
	     $q->execute(array($AccountID,$isactive,$rightleft,$StudentFirst,$StudentLast,$StudentNickname,$StudentDOB,$StudentGender,$StudentPassword,$StudentEmail,$Sport,$CompLevel,$recid));		    
	    }
	    $collectedids .=  $recid.',';
     }  				
    }
    //Remove Records not in Cloud DB but present in local DB
    $collectedids = rtrim($collectedids,",");
    $sql = "DELETE FROM users WHERE id NOT IN(".$collectedids.");";   
    $sqlQuery = $db->query($sql);	  	  
  }
?>