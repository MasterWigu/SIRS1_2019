<?php
    echo "string0 <br>";
    session_start();
    $DB_HOST = 'localhost';
    $DB_USER = 'root';
    $DB_PASS = 'toor';
    $DB_NAME = 'AVD_SCORE';
    $connection = new mysqli($DB_HOST, $DB_USER, $DB_PASS, $DB_NAME);
    if ( !$connection ) {
        die ('Connection failed: ' . mysqli_connect_error());
    }

    //******

    echo "string1 <br>";
    $arr = [];
    $stmt0 = $mysqli->prepare("SELECT * FROM user");
    echo "hi";
    if (!$stmt0) echo 'failed to run';
    $stmt0->execute();
    $result = $stmt0->get_result();
    while($row = $result->fetch_assoc()) {
      $arr[] = $row;
    }
    if(!$arr) exit('No rows');
    var_export($arr);
    $stmt0->close();

    //**********
    echo "string2";
    if ($stmt = $connection->prepare('SELECT username, password FROM user WHERE username = ? and password = ?')) {
        if ($stmt->num_rows > 0) {
          if (!$stmt->bind_result($username, $password)) {
               echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
          }
          if (!$stmt->execute()) {
              echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
          }
          $_SESSION['loggedin'] = TRUE;
		      $_SESSION['username'] = $username;
          echo 'Welcome ' . $_SESSION['name'] . '!';
        } else {
            echo 'Incorrect, try again.';
        }
    } else {
        echo "Prepare failed: (" . $mysqli->errno . ") " . $mysqli->error;
    }
    session_close();
    $stmt->close();
?>

// *****************************************************************
