<div class="card-body d-none" id="applicationCardBody">
    <div><h1 class="card-title">Club Spectrum Application</h1></div>
    <div><h2 class="card-text">Show us your true colors!</h2></div>
    <div><p>Thank you for your interest in Club Spectrum! This application is to assist us in sifting through all interested parties to find those most suitable to fit our venue. To ensure a speedy reply, check that every necessary and applicable field is filled out to the best of your ability. We look forward to receiving your application.</p></div>
    <div>Any question with a <span style="color:tomato;">*</span> is required</div><br>
    <form id="applicationForm" action="/post/application.php" method="post" data-parsley-validate="">
        <label for="question1">What drew you to apply at Club Spectrum? <span style="color:tomato;">*</span></label><br>
        <textarea type="text" id="question1" name="question1" required=""></textarea><br><br>
        
        <label for="question2">How did you hear about us? <span style="color:tomato;">*</span></label><br>
        <textarea type="text" id="question2" name="question2"  required=""></textarea><br><br>
        
        <label for="question3">Are you available to work 9pm to 2am, Tues and Wed? <span style="color:tomato;">*</span></label>
        <div id="question3">
            <label class="mr-4" for="question3Radio1"><input type="radio" id="question3Radio1" name="question3" value="Yes" required="" data-parsley-errors-container="#question3">Yes</label>
            <label class="mr-4" for="question3Radio2"><input type="radio" id="question3Radio2" name="question3" value="No">No</label>
            <label class="mr-4" for="question3Radio3"><input type="radio" id="question3Radio3" name="question3" value="Maybe">Maybe</label>
        </div>
        
        <label for="question4">If No or Maybe, what hours can you work and why?</label><br>
        <textarea type="text" id="question4" name="question4"></textarea><br><br>
        
        <label for="question5">What is your sexuality? <span style="color:tomato;">*</span></label>
        <div id="question5">
            <label class="mr-4" for="question5Radio1"><input type="radio" id="question5Radio1" name="question5" value="Straight" required=""  data-parsley-errors-container="#question5">Straight</label>
            <label class="mr-4" for="question5Radio2"><input type="radio" id="question5Radio2" name="question5" value="Gay">Gay</label>
            <label class="mr-4" for="question5Radio3"><input type="radio" id="question5Radio3" name="question5" value="Lesbian">Lesbian</label>
            <label class="mr-4" for="question5Radio4"><input type="radio" id="question5Radio4" name="question5" value="Bisexual">Bisexual</label>
            <label class="mr-4" for="question5Radio5"><input type="radio" id="question5Radio5" name="question5" value="Pansexual">Pansexual</label>
            <label class="mr-4" for="question5Radio6"><input type="radio" id="question5Radio6" name="question5" value="Asexual">Asexual</label>
            <label class="mr-4" for="question5Radio6"><input type="radio" id="question5Radio6" name="question5" value="Other">Other</label>
        </div>
        
        <label for="question6">If other, could you specify?</label>
        <input type="text" id="question6" name="question6"><br><br>
        
        <label for="question7">What position are you interested in? <span style="color:tomato;">*</span></label>
        <div id="question7">
            <label class="mr-4" for="question7Check1"><input type="checkbox" id="question7Check1" name="question7[]" value="Dancer" required="" data-parsley-mincheck="1"  data-parsley-errors-container="#question7">Dancer</label>
            <label class="mr-4" for="question7Check2"><input type="checkbox" id="question7Check2" name="question7[]" value="Courtesan">Courtesan</label>
            <label class="mr-4" for="question7Check3"><input type="checkbox" id="question7Check3" name="question7[]" value="Bartender">Bartender</label>
            <label class="mr-4" for="question7Check4"><input type="checkbox" id="question7Check4" name="question7[]" value="Host/Hostess">Host/Hostess</label>
            <label class="mr-4" for="question7Check5"><input type="checkbox" id="question7Check5" name="question7[]" value="Bard">Bard (or Bard Group)</label>
            <label class="mr-4" for="question7Check6"><input type="checkbox" id="question7Check6" name="question7[]" value="Security">Security</label>
        </div><br>
        
        <label for="question8">If working as a courtesan, would you be opposed to clients of the same or opposite sex? <span style="color:tomato;">*</span></label>
        <div id="question8">
            <label class="mr-4" for="question8Radio1"><input type="radio" id="question8Radio1" name="question8" value="I will do same sex, but not opposite sex" required="" data-parsley-errors-container="#question8">I will do same sex, but not opposite sex</label>
            <label class="mr-4" for="question8Radio2"><input type="radio" id="question8Radio2" name="question8" value="I will do opposite sex, but not same sex">I will do opposite sex, but not same sex</label>
            <label class="mr-4" for="question8Radio3"><input type="radio" id="question8Radio3" name="question8" value="I can do both">I can do both</label>
            <label for="question8Radio4"><input type="radio" id="question8Radio4" name="question8" value="Not applying as courtesan">Not applying as courtesan</label>
        </div><br>
        
        <label for="question9">If working as a courtesan, do you agree to have a test session to assess your skills? <span style="color:tomato;">*</span></label>
        <div id="question9">
            <label class="mr-4" for="question9Radio1"><input type="radio" id="question9Radio1" name="question9" value="Yes" required=""  data-parsley-errors-container="#question9">Yes</label>
            <label class="mr-4" for="question9Radio2"><input type="radio" id="question9Radio2" name="question9" value="No">No</label>
            <label class="mr-4" for="question9Radio3"><input type="radio" id="question9Radio3" name="question9" value="Not applying as Courtesan">Not applying as Courtesan</label>
        </div><br>
        
        <label for="question10">What server are you on? <span style="color:tomato;">*</span></label>
        <div id="question10">
            <label class="mr-4" for="question10Radio1"><input type="radio" id="question10Radio1" name="question10" value="Gilgamesh" required="" data-parsley-errors-container="#question10">Gilgamesh</label>
            <label class="mr-4" for="question10Radio2"><input type="radio" id="question10Radio2" name="question10" value="Adamantoise">Adamantoise</label>
            <label class="mr-4" for="question10Radio3"><input type="radio" id="question10Radio3" name="question10" value="Jenova">Jenova</label>
            <label class="mr-4" for="question10Radio4"><input type="radio" id="question10Radio4" name="question10" value="Faerie">Faerie</label>
            <label class="mr-4" for="question10Radio5"><input type="radio" id="question10Radio5" name="question10" value="Sargatanas">Sargatanas</label>
            <label class="mr-4" for="question10Radio6"><input type="radio" id="question10Radio6" name="question10" value="Midgardsormr">Midgardsormr</label>
            <label class="mr-4" for="question10Radio7"><input type="radio" id="question10Radio7" name="question10" value="Cactuar">Cactuar</label>
            <label for="question10Radio8"><input type="radio" id="question10Radio8" name="question10" value="Siren">Siren</label>
        </div><br>
        
        <label for="question11">What is your Discord ID? Are you a member of our Discord? <span style="color:tomato;">*</span></label>
        <input type="text" id="question11" name="question11"  required=""><br><br>
        
        <label for="question12">Speaking of Discord, even if you cannot communicate in voice chat, will you agree to have a presence in voice chat so you can listen to instructions when given? <span style="color:tomato;">*</span></label>
        <div id="question12" name="question12">
            <label class="mr-4" for="question12Radio1"><input type="radio" id="question12Radio1" name="question12" value="Yes" required="" data-parsley-errors-container="#question12">Yes</label>
            <label for="question12Radio2"><input type="radio" id="question12Radio2" name="question12" value="No">No</label>
        </div><br>
        
        <label for="question13">Give us a closing statement to make yourself stand out. Tell us a little about you. <span style="color:tomato;">*</span></label><br>
        <textarea type="text" id="question13" name="question13"  required=""></textarea><br><br>
        
        <input type="submit" value="Submit">
    </form>
</div>
