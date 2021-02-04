<?php
    require('/var/www/html/email.php');
    echo json_encode(sendEmail("admin@foxtek.us", "Test Subject", "<p>This is the html body</p>", "This is the normal body"));
?>
