<?php
    require('Utility/login.php');
    
    if($isLoggedIn)
    {
        echo '<li class="nav-item dropdown text-light">';
        echo '    <a class="nav-link dropdown-toggle text-light" data-toggle="dropdown" href="#">Static</a>';
        echo '    <ul class="dropdown-menu bg-dark">';
        echo '        <li>';
        echo '            <a class="nav-link text-light" data-target="#Modal-playerRegistrationStatic-modal" data-toggle="modal" href="#">Registration</a>';
        echo '        </li>';
        echo '        <li>';
        echo '            <a class="nav-link text-light" href="?Page_Name=StaticSearch">Character Search</a>';
        echo '        </li>';
        echo '    </ul>';
        echo '</li>';
    }
?>

