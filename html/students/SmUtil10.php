<?php
$old_path = getcwd();
chdir("/var/www/html/students/");
echo 'SmUtil10.sh ADMIN utility #10 running, PLEASE CLICK THE BACK BUTTON ON YOUR BROWSER.';
$result = 'SmUtil10';
// 10-07-18 htc - this is Kris' working code  $output = shell_exec("./SmMain.sh >/dev/null 2>/dev/null &");
// I tried to add the session ID no as a parameter similar to the code above - ". $result
$output = shell_exec("./SmUtil10.sh ". $result ." >/dev/null 2>/dev/null &");
chdir($old_path);

?>