<?php

   $auth = base64_encode("CvFEXgmPXnweNZsomBiD:knJwDJjedPHfONhycQDi");
   $auth = "Q3ZGRVhnbVBYbndlTlpzb21CaUQ6a25Kd0RKamVkUEhmT05oeWNRRGk=";
   $opts = array('http' =>array('header'  => "Authorization: Basic ".$auth));
   $context  = stream_context_create($opts);
   $result = file_get_contents('http://www.easy-insight.com/app/reports/MBXGZApSwiCEKayGLfGS/basic.json', false, $context);  


//$ch = curl_init();
//curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
//curl_setopt($ch,CURLOPT_URL,"https://www.easy-insight.com/app/reports/MBXGZApSwiCEKayGLfGS/basic.json");
//curl_setopt($ch, CURLOPT_USERPWD, "CvFEXgmPXnweNZsomBiD" . ":" . "knJwDJjedPHfONhycQDi");
//curl_setopt($ch,CURLOPT_RETURNTRANSFER,1);
//$result = curl_exec($ch);
//curl_close($ch);



echo($result);


?>