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
                <div><h3>Jenova Mist W23 P60</h3></div>
		<div><h5>Tuesdays &amp; Wednesdays</h5></div>
		<div><h5>9pm to 1am CST</h5></div>
		<div><h5>7pm to 11pm PST</h5></div>
                <div><h5>3am to 7am GMT</h5></div>
	    </div>
            <div class="card-body d-none" id="applicationCardBody">
                <div><h1 class="card-title">Club Spectrum Application</h1></div>
		<div><h2 class="card-text">Show us your true colors!</h2></div>
		<div><p>Thank you for your interest in Club Spectrum! This application is to assist us in sifting through all interested parties to find those most suitable to fit our venue. To ensure a speedy reply, check that every necessary and applicable field is filled out to the best of your ability. We look forward to receiving your application.</p></div>
                <form action="/post/application.php" method="post">
                    <label for="question1">What drew you to apply at Club Spectrum? *</label><br>
                    <textarea type="text" id="question1" name="question1"></textarea><br><br>

                    <label for="question2">How did you hear about us? *</label><br>
                    <textarea type="text" id="question2" name="question2"></textarea><br><br>

                    <label for="question3">Are you available to work 9pm to 2am, Tues and Wed? *</label>
                    <div id="question3">
                        <input type="radio" id="question3Radio1" name="question3" value="Yes">
			<label for="question3Radio1">Yes</label>
                        <input type="radio" id="question3Radio2" name="question3" value="No">
			<label for="question3Radio2">No</label>
                        <input type="radio" id="question3Radio3" name="question3" value="Maybe">
			<label for="question3Radio3">Maybe</label>
                    </div>

                    <label for="question4">If No or Maybe, what hours can you work and why?</label><br>
                    <textarea type="text" id="question4" name="question4"></textarea><br><br>

                    <label for="question5">Are you available to work 9pm to 2am, Tues and Wed? *</label>
                    <div id="question5">
                        <input type="radio" id="question5Radio1" name="question5" value="Straight">
			<label for="question5Radio1">Straight</label>
                        <input type="radio" id="question5Radio2" name="question5" value="Gay">
			<label for="question5Radio2">Gay</label>
                        <input type="radio" id="question5Radio3" name="question5" value="Lesbian">
			<label for="question5Radio3">Lesbian</label>
                        <input type="radio" id="question5Radio4" name="question5" value="Bisexual">
			<label for="question5Radio4">Bisexual</label>
                        <input type="radio" id="question5Radio5" name="question5" value="Pansexual">
			<label for="question5Radio5">Pansexual</label>
                        <input type="radio" id="question5Radio6" name="question5" value="Asexual">
			<label for="question5Radio6">Asexual</label>
                        <input type="radio" id="question5Radio6" name="question5" value="Other">
			<label for="question5Radio6">Other</label>
                    </div>

                    <label for="question6">If other, could you specify?</label>
                    <input type="text" id="question6" name="question6"><br><br>

                    <label for="question7">What position are you interested in? *</label>
                    <div>
                       <input type="checkbox" id="question7Check1" name="question7Check1">
                       <label for="question7Check1">Dancer</label>
                       <input type="checkbox" id="question7Check2" name="question7Check2">
                       <label for="question7Check2">Courtesan</label>
                       <input type="checkbox" id="question7Check3" name="question7Check3">
                       <label for="question7Check3">Bartender</label>
                       <input type="checkbox" id="question7Check4" name="question7Check4">
                       <label for="question7Check4">Host/Hostess</label>
                       <input type="checkbox" id="question7Check5" name="question7Check5">
                       <label for="question7Check5">Bard (or Bard Group)</label>
                       <input type="checkbox" id="question7Check6" name="question7Check6">
                       <label for="question7Check6">Security</label>
                    </div><br>

                    <label for="question8">If working as a courtesan, would you be opposed to clients of the same or opposite sex? *</label>
                    <div id="question8">
                        <input type="radio" id="question8Radio1" name="question8" value="I will do same sex, but not opposite sex">
			<label for="question8Radio1">I will do same sex, but not opposite sex</label>
                        <input type="radio" id="question8Radio2" name="question8" value="I will do opposite sex, but not same sex">
			<label for="question8Radio2">I will do opposite sex, but not same sex</label>
                        <input type="radio" id="question8Radio3" name="question8" value="I can do both">
			<label for="question8Radio3">I can do both</label>
                        <input type="radio" id="question8Radio4" name="question8" value="Not applying as courtesan">
			<label for="question8Radio4">Not applying as courtesan</label>
                    </div><br>

                    <label for="question9">If working as a courtesan, would you be opposed to clients of the same or opposite sex? *</label>
                    <div id="question9">
                        <input type="radio" id="question9Radio1" name="question9" value="Yes">
			<label for="question9Radio1">Yes</label>
                        <input type="radio" id="question9Radio2" name="question9" value="No">
			<label for="question9Radio2">No</label>
                        <input type="radio" id="question9Radio3" name="question9" value="Not applying as Courtesan">
			<label for="question9Radio3">Not applying as Courtesan</label>
                    </div><br>

                    <label for="question10">What server are you on? *</label>
                    <div id="question10">
                        <input type="radio" id="question10Radio1" name="question10" value="Gilgamesh">
			<label for="question10Radio1">Gilgamesh</label>
                        <input type="radio" id="question10Radio2" name="question10" value="Adamantoise">
			<label for="question10Radio2">Adamantoise</label>
                        <input type="radio" id="question10Radio3" name="question10" value="Jenova">
			<label for="question10Radio3">Jenova</label>
                        <input type="radio" id="question10Radio4" name="question10" value="Faerie">
	        	<label for="question10Radio4">Faerie</label>
                        <input type="radio" id="question10Radio5" name="question10" value="Sargatanas">
			<label for="question10Radio5">Sargatanas</label>
                        <input type="radio" id="question10Radio6" name="question10" value="Midgardsormr">
			<label for="question10Radio6">Midgardsormr</label>
                        <input type="radio" id="question10Radio7" name="question10" value="Cactuar">
			<label for="question10Radio7">Cactuar</label>
                        <input type="radio" id="question10Radio8" name="question10" value="Siren">
        		<label for="question10Radio8">Siren</label>
                    </div><br>

                    <label for="question11">What is your Discord ID? Are you a member of our Discord? *</label>
                    <input type="text" id="question11" name="question11"><br><br>

                    <label for="question12">Speaking of Discord, even if you cannot communicate in voice chat, will you agree to have a presence in voice chat so you can listen to instructions when given? *</label>
                    <div id="question12">
                        <input type="radio" id="question12Radio1" name="question12" value="Yes">
			<label for="question12Radio1">Yes</label>
                        <input type="radio" id="question12Radio2" name="question12" value="No">
			<label for="question12Radio2">No</label>
                    </div><br>

                    <label for="question13">Give us a closing statement to make yourself stand out. Tell us a little about you. *</label><br>
                    <textarea type="text" id="question13" name="question13"></textarea><br><br>

                    <input type="submit" value="Submit">
                </form>
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
