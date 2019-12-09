<?php
session_start();
?>
<!DOCTYPE html>
<html>
  <head>
  </head>
  <body>
    <?php
        if($_SESSION['loggedin']) {
          $DB_HOST = 'localhost';
          $DB_USER = 'root';
          $DB_PASS = 'toor';
          $DB_NAME = 'AVD_SCORE';
          $connection = new mysqli($DB_HOST, $DB_USER, $DB_PASS, $DB_NAME);
          if ( !$connection ) {
              die ('Connection failed: ' . mysqli_connect_error());
          }
          $name = $_GET['name'];

          if ($stmt = $connection->prepare('SELECT permissions FROM user WHERE username=?')) {
            if (!$stmt->bind_param('s', $userHandler)){
              echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
            }
            $userHandler = $_SESSION['username'];
            if (!$stmt->execute()) {
              echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
            }
            $result = $stmt->get_result();
            $row = $result->fetch_assoc();
            $perm = $row['permissions'];
            
          /* Check true leader's password ?*/
          if ($perm == 0) {
            print_r($name);

            if ($stmt = $connection->prepare('UPDATE user SET permissions=? WHERE username=?')) {
              if(!$stmt->bind_param('is', $aux = 1, $nameHandler)){
                echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
              }
              $nameHandler = $_GET['name'];
              if (!$stmt->execute()) {
                echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
              }
              $result = $stmt->get_result();
              header('location: loginRedirect.php?message=true_');
              $connection->close();
            } else {
                echo "Prepare failed: (" . $mysqli->errno . ") " . $mysqli->error;
            }
          }
          else {
            echo "You don't have the permissions to change this data.";
          }
        }
      }
    ?>

  </body>
</html>
