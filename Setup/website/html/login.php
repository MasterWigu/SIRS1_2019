<?php
  session_start();
?>
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
        if ($_POST['username'] === '') {
          echo "You have to login first!";
          die(0);
        }

        $connection = new mysqli($DB_HOST, $DB_USER, $DB_PASS, $DB_NAME);
        if ( !$connection ) {
            die ('Connection failed: ' . mysqli_connect_error());
        }

        if ($stmt = $connection->prepare('SELECT password FROM user WHERE username = ?')) {
          if (!$stmt->bind_param("s", $username)) {
               echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
          }
          $username = $_POST['username'];
          $password = $_POST['password'];

          if (!$stmt->execute()) {
              echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
          }

          $result = $stmt->get_result();
          if ($result->num_rows > 0) {
            while($row = $result->fetch_assoc()) {
              if (!password_verify($password, $row['password'])) {
                echo 'Wrong password, try again.';
                echo '<br><br><input type="button" value="Back" onclick="history.back(-1)"/>';
              } else {
                $_SESSION['loggedin'] = TRUE;
                $_SESSION['username'] = $username;
                header('location: loginRedirect.php');
              }
              break;
            }
          } else {
            echo 'Invalid username, try again.';
            echo '<br><br><input type="button" value="Back" onclick="history.back(-1)"/>';
          }
        } else {
            echo "Prepare failed: (" . $mysqli->errno . ") " . $mysqli->error;
        }

        $connection->close();
     ?>

    </body>
</html>
