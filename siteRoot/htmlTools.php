<?php

    function fixSpecialCharacters($string)
    {
        $string = str_replace("&", "&amp;", $string);
        $string = str_replace("/", "&sol;", $string);
        $string = str_replace("<", "&lt;", $string);
        $string = str_replace(">", "&gt;", $string);
        return $string;
    }
?>
