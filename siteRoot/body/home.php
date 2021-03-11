<div class="container h-100">
    <div class="row h-100 justify-content-center align-items-center">
        <div class="card container text-center bg-dark text-light">
            <div class="card-header row justify-content-center">
                <ul class="nav nav-pills card-header-pills">
                    <li class="nav-item">
                        <a class="nav-link mr-4" id="homeButton" href="#home">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link mr-4" id="menuButton" href="#menu">Menu</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link mr-4" id="biosButton" href="#bios">Bios</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link mr-4" id="venuButton" href="#venu">Venu</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link mr-4" id="contactButton" href="#contact">Contact</a>
                    </li>
                </ul>
            </div>
            <div class="card-body d-none" id="homeCardBody">
                <div><h1 class="card-title">Club Spectrum</h1></div>
                <div><h2 class="card-text">Show us your true colors!</h2></div>
                <div id="carouselDiv" class="carousel slide" data-ride="carousel">
		    <ol class="carousel-indicators">
                        <?php
                            $files = preg_grep('/^([^.])/', scandir($_SERVER['DOCUMENT_ROOT'] . "/img/home"));
                            $filesCount = count($files);
                            for ($x = 0; $x <= $filesCount; $x++) {
                            if ($x == 0) {
                                    echo '                        <li data-target="#carouselDiv" data-slide-to="0" class="active"></li>';
                                } else {
                                    echo '<li data-target="#carouselDiv" data-slide-to="' . $x . '"></li>';
                                }
			    }
			?>
                    </ol>
		    <div class="carousel-inner">
                        <?php
                            $files = preg_grep('/^([^.])/', scandir($_SERVER['DOCUMENT_ROOT'] . "/img/home"));
                            $isFirst = True;
			    foreach ($files as &$file) {
				if ($isFirst == True) {
				    echo '                        <div class="carousel-item active">';
				    $isFirst = False;
				} else {
                                    echo '                        <div class="carousel-item">';
				}
                                echo '                            <img class="d-block w-100" src="/img/home/' . $file . '" alt="">';
                                echo '                        </div>';
                            }
                        ?>
                    </div>
                    <a class="carousel-control-prev" href="#carouselDiv" role="button" data-slide="prev">
                        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                        <span class="sr-only">Previous</span>
                    </a>
                    <a class="carousel-control-next" href="#carouselDiv" role="button" data-slide="next">
                        <span class="carousel-control-next-icon" aria-hidden="true"></span>
                        <span class="sr-only">Next</span>
                    </a>
                </div>
	    </div>
	    <div class="card-body d-none" id="menuCardBody">
                <div><h1>Menu</h1></div>
		<div><h3>~(DRINKS)~</h3></div>
		<div id="drinkMenu"></div>
		</br>
                <div><h3>~(DRINK SPECIALS)~</h3></div>
                <div id="drinkSpecialMenu"></div>
                </br>
		<div><h3>~(SNACKS & APPS)~</h3></div>
                <div id="foodMenu"></div>
	    </div>
	    <div class="card-body d-none" id="biosCardBody">
                <div><h1>Bios</h1></div>
                <div class="row justify-content-center mb-4">
                    <ul class="nav nav-pills card-header-pills">
                        <li class="nav-item">
                            <a class="nav-link mr-4 biosButton 816834122541432852" id="biosStaffButton" href="#bios" onclick="displayBiosByChannelId('816834122541432852')">Staff</a>
			</li>
                        <li class="nav-item">
                            <a class="nav-link mr-4 biosButton 817184637629497374" id="biosBartenderButton" href="#bios" onclick="displayBiosByChannelId('817184637629497374')">Bartender</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link mr-4 biosButton 817223071274500126" id="biosDancerButton" href="#bios" onclick="displayBiosByChannelId('817223071274500126')">Dancer</a>
                        </li>
                        <li class="nav-item">
                             <a class="nav-link mr-4 biosButton 817222909340549140" id="biosManagementButton" href="#bios" onclick="displayBiosByChannelId('817222909340549140')">Management</a>
			</li>
                        <li class="nav-item">
                            <a class="nav-link mr-4 biosButton 817223031142481921" id="biosMusiciansButton" href="#bios" onclick="displayBiosByChannelId('817223031142481921')">Musicians</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link mr-4 biosButton 817222979679158282" id="biosSecurityButton" href="#bios" onclick="displayBiosByChannelId('817222979679158282')">Security</a>
                        </li>
                    </ul>
                </div>
                <div class="card-deck justify-content-center align-items-center" id="biosCardDeck"></div>
	    </div>
	    <div class="card-body d-none" id="venuCardBody">
                <div><h1>Venu</h1></div>
                <div><h3>Jenova Lavender Beds W13 P5</h3></div>
		<div><h5>Tuesdays &amp; Wednesdays</h5></div>
		<div><h5>9pm to 1am CST</h5></div>
		<div><h5>7pm to 11pm PST</h5></div>
                <div><h5>3am to 7am GMT</h5></div>
	    </div>
	    <div class="card-body d-none" id="contactCardBody">
                <div><h1>Contact Us</h1>
                <p>Join our Discord</p>
		<p>Looking to join our staff?</p>
		<p>Send a tell to "Erys Inverse@Jenova" or "Brialla Inverse@Jenova" or DM Erys#8227 via discord</p>
                <a href="#discord"><img class="rounded-circle w-25" src="/img/discord.png"></img></a>
            </div>
        </div>
    </div>
</div>
