<?php
/**
 * Created by PhpStorm.
 * User: Grégory
 * Date: 02-12-17
 * Time: 11:24
 */
session_start();
require '../test.php';
//variable de base nécéssaire pour la db !
$user_name = $_POST["user_name"];
$user_pass = $_POST["password"];
$dbh = new PDO("mysql:host=$serverName;dbname=$dbName", $userName, $password);

//fonctions
function monPrint_r($table){
    $customPre = "<pre>";
    $customPre .= print_r($table, true); // true, retourne le résultat de print_r
    $customPre .= "</pre>";
    return $customPre;
}
//requete sql
$sth = $dbh->prepare('SELECT * 
      FROM Kwapp_Projet.User
      WHERE Pseudo = :pseudo and Mot_de_passe = :mdp');
//parametres
$sth->bindParam(':pseudo', $user_name, PDO::PARAM_STR, 15);
$sth->bindParam(':mdp', $user_pass, PDO::PARAM_STR, 15);
$sth->execute();

/**
 * Requete qui renvoine uniquement l'id
 **/
/*
$iduser= $dbh->prepare('SELECT idUser 
                        FROM Kwapp_Projet.User 
                        WHERE Pseudo= :pseudo and Mot_de_passe= :mdp');
$iduser->bindParam(':pseudo', $user_name, PDO::PARAM_STR, 15);
$iduser->bindParam(':mdp', $user_pass, PDO::PARAM_STR, 15);
$iduser->execute();
*/

//test login si login existe
if($sth->fetch() == true) {
    echo "Connexion reussie";/*
    $donnees = $iduser->fetch();
    echo $donnees;*/
}
else {echo "ERROR - Mot de passe et/ou login incorrect...";}





