<?php
/**
 * Created by PhpStorm.
 * User: Grégory
 * Date: 02-12-17
 * Time: 11:24
 */
session_start();
$_SESSION['idUtilisateur']='';
$_SESSION['NameUser']='';

require '../test.php';
require 'inc/requetes-sql.php';

//variable de base nécéssaire pour la db !
$user_name='lala'; /*$_POST["user_name"]*/
$user_pass='azerty'; /*$_POST["password"]*/

$dbh = new PDO("mysql:host=$serverName;dbname=$dbName", $userName, $password);



//requete sql
$sth = $dbh->prepare('SELECT idUser,Pseudo 
      FROM Projet_kwapp.User
      WHERE Pseudo = :pseudo and Mot_de_passe = :mdp');
//parametres
$sth->bindParam(':pseudo', $user_name, PDO::PARAM_STR, 15);
$sth->bindParam(':mdp', $user_pass, PDO::PARAM_STR, 15);
$sth->execute();

/*---------------------------------------------------------------*/

$sqlGetUser="SELECT idUser,Pseudo 
      FROM Projet_kwapp.User
      WHERE Pseudo='$user_name' and Mot_de_passe='$user_pass'";

//test login si login existe
if($sth->fetch() == true) {
    //echo "Connexion reussie";
    $getIdUser = $dbh->query($sqlGetUser);
    foreach($getIdUser->fetchAll(PDO::FETCH_ASSOC) as $row){
        /*echo "Id : ".$row['idUser']."\n";
        echo " Pseudo : ".$row['Pseudo'];*/
        $_SESSION['idUser']=$row['idUser'];
        $_SESSION['NameUser']=$row['Pseudo'];
        echo "Session idUser is : ".$_SESSION['idUser'];
        echo " Session User Name is : ".$_SESSION['NameUser'];
    }
}
else {echo "ERROR - Mot de passe et/ou login incorrect...";}





//$getIdUser->closeCursor(); // Termine le traitement de la requête

