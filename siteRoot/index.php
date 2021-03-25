<!DOCTYPE html>
<html lang="en">
    <head>
	<meta charset="utf-8">
	<script src="/npm/node_modules/jquery/dist/jquery.min.js"></script>
	<script src="/npm/node_modules/bootstrap/dist/js/bootstrap.min.js"></script>
	<link href="/npm/node_modules/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet">
	<script src="/npm/node_modules/parsleyjs/dist/parsley.min.js"></script>
        <script src="/js/application.js"></script>
	<script src="/js/urlParam.js"></script>
        
	<script src="/js/navigation.js"></script>
        <script src="/js/bios.js"></script>
        <script src="/js/menu.js"></script>
        <link href="/css/global.css" rel="stylesheet">
    </head>
    <body class="bg-dark text-light">
        <div class="container h-100">
            <div class="row h-100 justify-content-center align-items-center">
                <div class="card container text-center bg-dark text-light">
                    <?php
                        require("navigation/cardNavigation.php");
                        require("cards/application.php");
                        require("cards/bios.php");
                        require("cards/contact.php");
                        require("cards/home.php");
                        require("cards/menu.php");
                        require("cards/venue.php");
                    ?>
                </div>
            </div>
        </div>
    </body>
</html>
