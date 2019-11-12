<?php
    session_start();
    $DB_HOST = 'localhost';
    $DB_USER = 'root';
    $DB_PASS = 'toor';
    $DB_NAME = 'AVD_SCORE';
    $connection = mysqli_connect($DB_HOST, $DB_USER, $DB_PASS, $DB_NAME);
    if ( !$connection ) {
        die ('Connection failed: ' . mysqli_connect_error());
    }

    if ($stmt = $connection->prepare('SELECT username, password FROM user WHERE username = ?')) {
        if ($stmt->num_rows > 0) {
            if (!$stmt->bind_result($username, $password)) { // TODO if doent work try bindParam
                 echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
            }
            if (!$stmt->execute()) {
                echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
            }
            //$stmt->store_result(); // store to check if account exists in BD
            if (password_verify($POST['password'], $password)) {
                echo 'Welcome ' . $username . '!';
            } else {
                echo 'Incorrect password.';
            }
        } else {
            echo 'Incorrect username.';
        }
    } else {
        echo "Prepare failed: (" . $mysqli->errno . ") " . $mysqli->error;
    }
    $stmt->close();
?>

// *****************************************************************
