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

          if ($stmt = $connection->prepare('SELECT permissions FROM user')) {
            if (!$stmt->execute()) {
              echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
            }
            $result = $stmt->get_result();
            $perm = $result->fetch_row()['permissions'];

          echo '<div id="header" style="overflow: hidden; padding: 20px 10px; background-color: #f1f1f1;">';
          echo '<div id="header-left" style="background-color: #f1f1f1; float: left; color: #23a9cf;">';
          echo '<h1 style="text-align:center;">' . $_SESSION['username'] .'</h1>';
          echo '</div>';

          echo '<div id="header-right" style="background-color: #f1f1f1; float: right; text-align:center">';
          echo '<a href="logout.php" style="padding: 20px 0px; text-decoration:none; color:#7d1e1e; margin-top:auto; margin-bottom:auto">Logout</a>';
          echo '</div>';
          echo '</div>';

          echo '<p><form action="loginRedirect.php" method="POST"><input type="submit" value="Back"></form>';
          if ($name == $_SESSION['username'] || $perm === 0) {
            echo '<h2 style="text-align:center;color: olivedrab"> Submitted vulnerabilities </h2>';

            if ($stmt = $connection->prepare('SELECT * FROM user')) {
              if (!$stmt->execute()) {
                echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
              }
              $result = $stmt->get_result();
              echo '<table border="5" style="width:70%; margin-left:auto;margin-right:auto;">';
              echo '<tr>';
              echo '<th> Fingerprint </th>';
              echo '<th> Explanation </th>';
              echo '</tr>';
              while($row = $result->fetch_assoc()){
                $fp      = $row['fingerprint'];
                $explain = $row['explanation'];
                echo '<tr data-href="url://userInfo.php/">';
                echo '<th>' . $fp . '</th>';
                echo '<th>' . $explain . '</th>';
                echo '</tr>';
              }
            } else {
                echo "Prepare failed: (" . $mysqli->errno . ") " . $mysqli->error;
            }

            $connection->close();
          }
          else {
            echo "You don't have the permissions to see this data.";
          }
        }
      } else {
        echo "You have to login first!";
      }
    ?>

  </body>
</html>
