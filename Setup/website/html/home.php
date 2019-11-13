<?php
  session_start();
  if (!isset($_SESSION['loggedin'])) {
	   header('Location: index.html');
	exit();
  }
  $DB_HOST = 'localhost';
  $DB_USER = 'root';
  $DB_PASS = 'toor';
  $DB_NAME = 'AVD_SCORE';
  $connection = mysqli_connect($DB_HOST, $DB_USER, $DB_PASS, $DB_NAME);
  if ( !$connection ) {
      die ('Connection failed: ' . mysqli_connect_error());
  }
?>
