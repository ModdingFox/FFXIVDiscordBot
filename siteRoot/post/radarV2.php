<?php
    require($_SERVER['DOCUMENT_ROOT'] . "/zookeeper.php");
    
    if ($_SERVER['REQUEST_METHOD'] === 'POST')
    {
        $json = file_get_contents('php://input');
	$data = json_decode($json);
	$players = $data->players;
	foreach($players as $player)
	{
            $playerPath = '/radar/players/' . $player;
	    $zookeeper->set($playerPath, '');
        }
    }
?>
