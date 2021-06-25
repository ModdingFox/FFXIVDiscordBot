<div class="card-header row justify-content-center">
    <ul class="nav nav-pills card-header-pills">
        <li class="nav-item">
            <a class="nav-link mr-4" id="homeButton" href="#home">Home</a>
        </li>
        <li class="nav-item">
            <a class="nav-link mr-4" id="menuButton" href="#menu">Menu</a>
	</li>
        <?php
            if (basename($_SERVER['PHP_SELF']) == "indexVIP.php") {
                echo '        <li class="nav-item">';
	        echo '            <a class="nav-link mr-4" id="menuButton" href="#vipMenu">VIP Menu</a>';
   	        echo '        </li>';
	    }
        ?>
        <li class="nav-item">
            <a class="nav-link mr-4" id="biosButton" href="#bios">Bios</a>
        </li>
        <li class="nav-item">
            <a class="nav-link mr-4" id="venueButton" href="#venue">Venue</a>
        </li>
        <li class="nav-item">
            <a class="nav-link mr-4" id="applicationButton" href="#application">Hiring Application</a>
        </li>
        <li class="nav-item">
            <a class="nav-link mr-4" id="contactButton" href="#contact">Contact</a>
        </li>
    </ul>
</div>
