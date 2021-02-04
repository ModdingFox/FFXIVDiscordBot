<?php
   require('../redis_Connection.php');
   echo 'SET test boop: ' . phpiredis_command($redis, 'SET test boop') . '</br>';
   echo 'GET test: ' . phpiredis_command($redis, 'GET test') . '</br>';
   echo 'DEL test: ' . phpiredis_command($redis, 'DEL test') . '</br>';

   echo 'SET test boop EX 5: ' . phpiredis_command($redis, 'SET test boop EX 5') . '</br>';
   echo 'GET test: ' . phpiredis_command($redis, 'GET test') . '</br>';
   sleep(10);
   echo 'GET test: ' . phpiredis_command($redis, 'GET test') . '</br>';
   echo 'DEL test: ' . phpiredis_command($redis, 'DEL test') . '</br>';
?>
