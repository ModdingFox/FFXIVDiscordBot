<nav class="navbar navbar-expand-md bg-dark navbar-dark">
    <img class="rounded-circle" src="/img/logo.png" style="width:40px;">
    <a class="navbar-brand" href="#">Agito</a>
    <button class="navbar-toggler" data-target="#collapsibleNavbar" data-toggle="collapse" type="button"> 
        <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="collapsibleNavbar">
        <ul class="navbar-nav">
            <?php require("Static.php"); ?>
        </ul>
        <ul class="navbar-nav ml-auto">
            <?php require('userAuthentication.php'); ?>
        </ul>
    </div>
</nav>
