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
        <?php
            $Target_Page="body/home.php";
            
            switch($_GET["Page_Name"]) {
                default:
                    break;
            }
            
            if($Target_Page != "") { require($Target_Page); }
        ?>
    </body>
</html>
