<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "DTD/xhtml1-transitional.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf8" />
<title>Echolink QSO Log</title>
</head>
<body>
<?php

function getval($val,$default)
{
	$string=$_GET[$val];

	if (empty($string)) 
	{
		$string = $default;
	}
	return $string;
}

/**
 * StartsWith
 * Tests if a text starts with an given string.
 *
 * @param     string
 * @param     string
 * @return    bool
 */
function StartsWith($Haystack, $Needle){
    // Recommended version, using strpos
    return strpos($Haystack, $Needle) === 0;
}

#information from browser
$count = getval('count','200');

// set path of database file
//$_SERVER['DOCUMENT_ROOT']
$db = "/var/www/EcholinkQsoLog.sqlite";


//don't tuch the constants! For they posess a terrable curse
$action = "ACTION";

// open database file
// create a SQLite3 database file with PDO and return a database handle (Object Oriented)
try{
$dbHandle = new PDO('sqlite:'. $db);
}catch( PDOException $exception ){
die($exception->getMessage());
}
//end create

// generate query string
$query = "SELECT * FROM qso ORDER BY id DESC LIMIT 0 , " . $count;

// execute query

$result = $dbHandle->query($query);

// if rows exist

    // get each row as an array
    // print values
    echo "<table cellpadding=5 border=0>";

    while($row = $result->fetch()) {
      
	$timestamp = "<td><font color='red'>[". date("Y/m/d H:i:s",$row[5])."]</font> ";
	$CS = $row[0];
	$TCS = explode('-', $CS, 2);
        echo "<tr>";        
        echo $timestamp . "<font color='red'>&lt;<a href=" . "http://www.qrz.com/db/" .$TCS[0] . " >" .$CS . "</a>&gt;</font> "  . htmlentities($row[3] . " has " . $row[4]."ed" ,ENT_QUOTES,"UTF-8");
	echo "</td></tr>\n";
    }
    echo "</table>";


// all done
// close database file

?>
</body>
</html>
