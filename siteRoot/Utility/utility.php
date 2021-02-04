<?php
    function random_salt($length)
    {
        $possible = '0123456789'.
            'abcdefghijklmnopqrstuvwxyz'.
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.
            './';
        $str = '';
        mt_srand((double)microtime() * 1000000);

        while (strlen($str) < $length)
            $str .= substr($possible,(rand()%strlen($possible)),1);

        return $str;
    }
    
    function uuid(){
        $data = random_bytes(16);
        $data[6] = chr(ord($data[6]) & 0x0f | 0x40);
        $data[8] = chr(ord($data[8]) & 0x3f | 0x80);
        return vsprintf('%s%s-%s-%s-%s-%s%s%s', str_split(bin2hex($data), 4));
    }
?>
