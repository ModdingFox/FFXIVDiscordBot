<?php
    require('Utility/login.php');
    
    if($isLoggedIn)
    {
        echo '<li class="nav-item dropdown text-light">';
        echo '    <a class="nav-link dropdown-toggle text-light" data-toggle="dropdown" href="#">' . $userName . '</a>';
        echo '    <ul class="dropdown-menu bg-dark">';
        require('userMenu.php');
        echo '        <li>';
        echo '            <a id="Navbar-userMenu-a" class="nav-link text-light" href="#">Logout</a>';
        echo '        </li>';
        echo '    </ul>';
        echo '</li>';
    }
    else
    {
        echo '<li class="nav-item">';
        echo '    <a class="nav-link text-light" data-target="#Modal-userLogin-modal" data-toggle="modal" href="#">Login</a>';
        echo '</li>';
        echo '<li class="nav-item">';
        echo '<li class="nav-item">';
        echo '    <a class="nav-link text-light" data-target="#Modal-userRegistration-modal" data-toggle="modal" href="#">Register</a>';
        echo '</li>';
    }
?>
