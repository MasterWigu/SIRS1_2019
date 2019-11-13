<html>
<head>
	<title>PHP Test</title>
</head>
<body>
	<?php echo '<p>Hello World</p>';

	$servername = "localhost";
	$username = "root";
	$password = "toor";

	$conn = mysqli_connect($servername, $username, $password);

	if (!$conn) {
		die('<p>Connection rip: </p>' . mysqli_connect_error());
	}
	echo '<p>Connection yesyes</p>'
	?>

</body>
</html>