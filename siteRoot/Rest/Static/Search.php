<?php
require('../../DB_Connection.php');
$json_result = json_decode('{}');

if ($conn->connect_error)
{
    $json_result->status = 'Error';
    $json_result->error = $conn->connect_error;
}
else
{
    if ($_SERVER['REQUEST_METHOD'] === 'POST' && $_POST['Method'] === 'searchPlayer')
    {
        $json_payload = json_decode($_POST['JSON'], true);
            
        $select_playerInfo = 'SELECT CONCAT(pC.characterFirstName, \' \', pC.characterLastName) AS characterName, ' .
            '    CASE WHEN pR.hasSavageExperience = true THEN \'Yes\' ELSE \'No\' END AS hasSavageExperience, ' .
            '    CASE WHEN pR.hasRaidExperience = true THEN \'Yes\' ELSE \'No\' END AS hasRaidExperience, ' .
            '    CONCAT_WS( ' .
            '        \', \', ' .
            '        CASE WHEN pR.sunday = true THEN \'Sun\' ELSE NULL END, ' .
            '        CASE WHEN pR.monday = true THEN \'Mon\' ELSE NULL END, ' .
            '        CASE WHEN pR.tuesday = true THEN \'Tu\' ELSE NULL END, ' .
            '        CASE WHEN pR.wednesday = true THEN \'Wed\' ELSE NULL END, ' .
            '        CASE WHEN pR.thursday = true THEN \'Th\' ELSE NULL END, ' .
            '        CASE WHEN pR.friday = true THEN \'Fri\' ELSE NULL END, ' .
            '        CASE WHEN pR.saturday = true THEN \'Sat\' ELSE NULL END ' .
            '    ) AS playerAvaliablilty, ' .
            '    cC.currentLevel, cC.averageILevel, ' .
            '    CASE WHEN cC.hasMeldsCheckbox = true  THEN \'Yes\' ELSE \'No\' END AS hasMeldsCheckbox, ' .
            '    c.name ' .
            'FROM ffxivPlayers.playerCharacters pC ' .
            'JOIN ffxivStatic.playerRegistrationStatic pR ON pC.userCN = pR.userCN ' .
            'JOIN ffxivPlayers.characterClasses cC ON pC.id = cC.playerCharacterId ' .
            'JOIN ffxivReference.classes c ON cC.classId = c.id ';
            
            $select_playerInfo_where = [];
            $select_playerInfo_where_bind_types = [];
            $select_playerInfo_where_bind_values = [];

            if(isset($json_payload['Body-Static_Search-classSelect']) && !empty($json_payload['Body-Static_Search-classSelect']))
            {
                $arraySize = sizeof($json_payload['Body-Static_Search-classSelect']);
                $select_playerInfo_where_placeholders = join(', ', array_fill(0, $arraySize, '?'));
                array_push($select_playerInfo_where, 'c.id IN (' . $select_playerInfo_where_placeholders . ')');
                array_push($select_playerInfo_where_bind_types, str_repeat('s', $arraySize));
                $select_playerInfo_where_bind_values = array_merge($select_playerInfo_where_bind_values, $json_payload['Body-Static_Search-classSelect']);
            }
            
            if(isset($json_payload['Body-Static_Search-levelSelect']) && !empty($json_payload['Body-Static_Search-levelSelect']))
            {
                $arraySize = sizeof($json_payload['Body-Static_Search-levelSelect']);
                $select_playerInfo_where_placeholders = join(', ', array_fill(0, $arraySize, '?'));
                array_push($select_playerInfo_where, 'cC.currentLevel IN (' . $select_playerInfo_where_placeholders . ')');
                array_push($select_playerInfo_where_bind_types, str_repeat('i', $arraySize));
                $select_playerInfo_where_bind_values = array_merge($select_playerInfo_where_bind_values, $json_payload['Body-Static_Search-levelSelect']);
            }
            
            if(isset($json_payload['Body-Static_Search-iLevelSelect']) && !empty($json_payload['Body-Static_Search-iLevelSelect']))
            {
                $arraySize = sizeof($json_payload['Body-Static_Search-iLevelSelect']);
                $select_playerInfo_where_placeholders = join(', ', array_fill(0, $arraySize, '?'));
                array_push($select_playerInfo_where, 'cC.averageILevel IN (' . $select_playerInfo_where_placeholders . ')');
                array_push($select_playerInfo_where_bind_types, str_repeat('i', $arraySize));
                $select_playerInfo_where_bind_values = array_merge($select_playerInfo_where_bind_values, $json_payload['Body-Static_Search-iLevelSelect']);
            }
            
            if(isset($json_payload['Body-Static_Search-daySelect']) && !empty($json_payload['Body-Static_Search-daySelect']))
            {
                $select_playerInfo_dayOfWeek_where = [];
                
                foreach ($json_payload['Body-Static_Search-daySelect'] as &$value)
                {
                    $dayOfWeek = '';
                    
                    switch ($value)
                    {
                        case 0:
                            $dayOfWeek = 'sunday';
                            break;
                        case 1:
                            $dayOfWeek = 'monday';
                            break;
                        case 2:
                            $dayOfWeek = 'tuesday';
                            break;
                        case 3:
                            $dayOfWeek = 'wednesday';
                            break;
                        case 4:
                            $dayOfWeek = 'thursday';
                            break;
                        case 5:
                            $dayOfWeek = 'friday';
                            break;
                        case 6:
                            $dayOfWeek = 'saturday';
                            break;
                    }
                    array_push($select_playerInfo_dayOfWeek_where, 'pR.' . $dayOfWeek . ' = 1');
                }
                
                array_push($select_playerInfo_where, '(' . join(' OR ', $select_playerInfo_dayOfWeek_where) . ')');
            }
            
            if(isset($json_payload['Body-Static_Search-hasSavageExperience']) && !empty($json_payload['Body-Static_Search-hasSavageExperience']))
            {
                $arraySize = sizeof($json_payload['Body-Static_Search-hasSavageExperience']);
                $select_playerInfo_where_placeholders = join(', ', array_fill(0, $arraySize, '?'));
                array_push($select_playerInfo_where, 'pR.hasSavageExperience in (' . $select_playerInfo_where_placeholders . ')');
                array_push($select_playerInfo_where_bind_types, str_repeat('i', $arraySize));
                $select_playerInfo_where_bind_values = array_merge($select_playerInfo_where_bind_values, $json_payload['Body-Static_Search-hasSavageExperience']);
            }
            
            if(isset($json_payload['Body-Static_Search-hasRaidExperience']) && !empty($json_payload['Body-Static_Search-hasRaidExperience']))
            {
                $arraySize = sizeof($json_payload['Body-Static_Search-hasRaidExperience']);
                $select_playerInfo_where_placeholders = join(', ', array_fill(0, $arraySize, '?'));
                array_push($select_playerInfo_where, 'pR.hasRaidExperience in (' . $select_playerInfo_where_placeholders . ')');
                array_push($select_playerInfo_where_bind_types, str_repeat('i', $arraySize));
                $select_playerInfo_where_bind_values = array_merge($select_playerInfo_where_bind_values, $json_payload['Body-Static_Search-hasRaidExperience']);
            }
            
            if(isset($json_payload['Body-Static_Search-hasMeldsCheckbox']) && !empty($json_payload['Body-Static_Search-hasMeldsCheckbox']))
            {
                $arraySize = sizeof($json_payload['Body-Static_Search-hasMeldsCheckbox']);
                $select_playerInfo_where_placeholders = join(', ', array_fill(0, $arraySize, '?'));
                array_push($select_playerInfo_where, 'cC.hasMeldsCheckbox in (' . $select_playerInfo_where_placeholders . ')');
                array_push($select_playerInfo_where_bind_types, str_repeat('i', $arraySize));
                $select_playerInfo_where_bind_values = array_merge($select_playerInfo_where_bind_values, $json_payload['Body-Static_Search-hasMeldsCheckbox']);
            }
            
            $select_playerInfo_stmt = $conn->prepare($select_playerInfo);
            
            if(!empty($select_playerInfo_where))
            {
                $select_playerInfo = $select_playerInfo . ' WHERE ' . join(' AND ', $select_playerInfo_where);
                $select_playerInfo_stmt = $conn->prepare($select_playerInfo);
                
                if(!empty($select_playerInfo_where_bind_types))
                {
                    $select_playerInfo_stmt->bind_param(join('',$select_playerInfo_where_bind_types), ...$select_playerInfo_where_bind_values);
                }
            }
            
            $json_result->result = [];
            
            if($select_playerInfo_stmt->execute() === TRUE)
            {
                $result = $select_playerInfo_stmt->get_result();
                while($row = $result->fetch_assoc())
                {
                    array_push($json_result->result, $row);
                }
                $json_result->status = 'Success';
            }
            else
            {
                $json_result->status = 'Error';
                $json_result->error = $conn->error;
            }

    }
    else
    {
        $json_result->status = 'Error';
        $json_result->error = 'No meathod for request found';
    }
}

    echo json_encode($json_result);
?>
