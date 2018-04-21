<?php

// connect to mysql
$con = mysqli_connect('localhost', 'root', '188113236');


// select db
mysqli_select_db($con, 'Plants');

$sql = "SELECT * FROM table1";

$records = mysqli_query($con, $sql);


?>

<html>

	<head>
	<title>Plants data</title>    
	</head>
	<body>

	<table width = "600" border = "1" cellspacing = "1">
	<tr>
	<th>ID</th>
	<th>Time</th>
	<th>Temperature</th>
	<th>Soil_humidity</th>
	<th>Environment_humidity</th>
	<th>Time_of_light</th>
	</tr>

	<?php

	while($Plants = mysqli_fetch_assoc($records)){
    
   		echo "<tr>";

   		echo "<td>".$Plants['id']."</td>";

    	echo "<td>".$Plants['time']."</td>";

    	echo "<td>".$Plants['temp']."</td>";

    	echo "<td>".$Plants['soil_humidity']."</td>";

    	echo "<td>".$Plants['humidity']."</td>";

    	echo "<td>".$Plants['light']."</td>";

    	echo "</tr>";
	}

	?>

	</table>    

	</body>
</html>
