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
        
        $msg = $_GET['message'];
        if ($msg == 'true')
          echo 'User added successfully';
        if ($msg == 'true_')
          echo 'User removed successfully';

        echo '<div id="header" style="overflow: hidden; padding: 20px 10px; background-color: #f1f1f1;">';
        echo '<div id="header-left" style="background-color: #f1f1f1; float: left; color: #23a9cf;">';
        echo '<h1 style="text-align:center;"> Welcome ' . htmlspecialchars($_SESSION['username']) . '! </h1>';
        echo '</div>';

        echo '<div id="header-right" style="background-color: #f1f1f1; float: right; text-align:center">';
        echo '<a href="logout.php" style="padding: 20px 0px; text-decoration:none; color:#7d1e1e; margin-top:auto; margin-bottom:auto">Logout</a>';
        echo '</div>';
        echo '</div>';

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
            echo '<a href="promote.php" style="background-color:#2f66a1; color: white; float:right">Promote leaders</a>';
          }
        }


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
            echo '<tr>';
            echo '<th><a href="/userInfo.php?name='.htmlspecialchars($name).'">'. htmlspecialchars($name) . '</a></th>';
            echo '<th>' . $points . '</th>';
            echo '</tr>';
          }
        } else {
            echo "Prepare failed: (" . $mysqli->errno . ") " . $mysqli->error;
        }
        $connection->close();
     ?>

    </body>
</html>
