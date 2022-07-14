<?php
    switch($_GET["path"]) {
        case "dj":
            header("Location: https://www.twitch.tv/synclayr");
	    exit();
	case "discord":
            header("Location: https://discord.gg/32WZHSyxws");
            exit();
        default:
            require("indexHome.php");
    }
?>
