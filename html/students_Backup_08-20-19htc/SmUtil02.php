<?php
$old_path = getcwd();
chdir("/var/www/html/students/");
//echo 'SmUtil02.sh ADMIN utility #2 running, PLEASE CLICK THE BACK BUTTON ON YOUR BROWSER.';

echo 'You can close this window, the update will continue to run.  You should see your latest changes in Practice Modes within 5 minutes';


$result = 'SmUtil02';
// 10-07-18 htc - this is Kris' working code  $output = shell_exec("./SmMain.sh >/dev/null 2>/dev/null &");
// I tried to add the session ID no as a parameter similar to the code above - ". $result
$output = shell_exec("./SmUtil02.sh ". $result ." >/dev/null 2>/dev/null &");
chdir($old_path);



?>