<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <script src="/npm/jquery/jquery.min.js"></script>
        <script src="/npm/popper.js/dist/umd/popper.min.js"></script>
        <script src="/npm/bootstrap/js/bootstrap.min.js"></script>
        <link href="/npm/bootstrap/css/bootstrap.min.css" rel="stylesheet">
        <script src="/npm/datatables.net/jquery.dataTables.min.js"></script>
        <link href="/css/jquery.dataTables.css" rel="stylesheet">
        <script src="/npm/underscore/underscore-min.js"></script>
        <script src="/npm/validate.js/validate.min.js"></script>
        <script src="/npm/jquery.cookie/jquery.cookie.js"></script>
        <link href="/css/modal.css" rel="stylesheet">
        <script src="/js/URL_Param.js"></script>
        <script src="/js/confirmAction.js"></script>
        <script src="/js/formValidation.js"></script>
        <?php
            require('Utility/login.php');
            $Target_Page="";

            switch($_GET["Page_Name"]) {
                default:
                    $Target_Page="Head/Home.php";
                    break;
            }

            if($isLoggedIn)
            {
                switch($_GET["Page_Name"]) {
                    case "StaticSearch":
                        $Target_Page="Head/Static/Search.php";
                    default:
                        $Target_Page=$Target_Page;
                        break;
                }
               
               require("Head/Static/Registration.php");
               require("Head/userMenu.php");
            }
            else { require("Head/userAuthentication.php"); }
            
            if($Target_Page != "") { require($Target_Page); }
        ?>
    </head>
    <body class="bg-dark text-light">
        <?php require('Navbar/index.php'); ?>
        <?php
            require('Utility/login.php');
            $Target_Page="";
            
            switch($_GET["Page_Name"]) {
                default:
                    $Target_Page="Body/Home.php";
                    break;
            }
            
            if($isLoggedIn)
            {
                switch($_GET["Page_Name"]) {
                    case "StaticSearch":
                        $Target_Page="Body/Static/Search.php";
                        break;
                    default:
                        $Target_Page=$Target_Page;
                        break;
                }
                
                require('Modal/accountSettings.php');
                require('Modal/Static/Registration.php');
                require('Modal/playerCharacter.php');
            }
            else { require("Modal/userAuthentication.php"); }

            require('Modal/confirmAction.php');
            
            if($Target_Page != "") { require($Target_Page); }
        ?>
    </body>
</html>
