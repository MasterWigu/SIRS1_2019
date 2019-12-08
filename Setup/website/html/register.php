<!DOCTYPE html>
<html>
  <head>
  </head>
  <body>
    <?php
        $DB_HOST = 'localhost';
        $DB_USER = 'root';
        $DB_PASS = 'toor';
        $DB_NAME = 'AVD_SCORE';
        $connection = new mysqli($DB_HOST, $DB_USER, $DB_PASS, $DB_NAME);
        if ( !$connection ) {
            die ('Connection failed: ' . mysqli_connect_error());
        }


        if ($stmt = $connection->prepare('INSERT INTO user (username, password)  VALUES (?, ?)')) {
          if (!$stmt->bind_param("ss", $username, $password)) {
            echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
          }
          $username = $_POST['username'];
          $password = password_hash($_POST['password'] , PASSWORD_BCRYPT);

          if (!$stmt->execute()) {
            echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
          }
        } else {
            echo "Prepare failed: (" . $mysqli->errno . ") " . $mysqli->error;
        }
        echo 'User added.';
        $connection->close();
    ?>
    <br>
    <br>
    <input type="button" value="Back" onclick="history.back(-1)" />
  </body>
<html>
