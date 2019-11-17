<!DOCTYPE html>
<html>
  <head>
  </head>
  <body>
    <?php
        session_start();
        $DB_HOST = 'localhost';
        $DB_USER = 'root';
        $DB_PASS = 'toor';
        $DB_NAME = 'AVD_SCORE';
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

                echo '<div id="header" style="overflow: hidden; padding: 20px 10px; background-color: #f1f1f1;">';
                echo '<div id="header-left" style="background-color: #f1f1f1; float: left; color: #23a9cf;">';
                echo '<h1 style="text-align:center;"> Welcome ' . $_SESSION['username'] . '! </h1>';
                echo '</div>';

                echo '<div id="header-right" style="background-color: #f1f1f1; float: right; text-align:center">';
                echo '<a href="logout.php" style="padding: 20px 0px; text-decoration:none; color:#7d1e1e; margin-top:auto; margin-bottom:auto">Logout</a>';
                echo '</div>';
                echo '</div>';

                echo '<h2 style="text-align:center;color: olivedrab"> Team users </h2>';

                if ($stmt = $connection->prepare('SELECT * FROM user')) {
                  if (!$stmt->execute()) {
                      echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
                  }
                  $result = $stmt->get_result();
                  echo '<table border="5" style="width:70%; margin-left:auto;margin-right:auto;">';
                  echo '<tr>';
                  echo '<th> Username </th>';
                  echo '<th> Points </th>';
                  echo '</tr>';
                  while($row = $result->fetch_assoc()){
                      $name   = $row['username'];
                      $points = $row['points'];
                      $_SESSION['name'] = $name; # this doesnt work overwrite
                      echo '<tr>';
                      echo '<a href="userInfo.php"><th>' . $name . '</th>';
                      echo '</a>';
                      echo '<th>' . $points . '</th>';
                      echo '</tr>';
                  }
                }
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
