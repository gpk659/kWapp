<?php
/**
 * Created by PhpStorm.
 * User: Grégory
 * Date: 18-12-17
 * Time: 12:37
 */

session_start();

require '../test.php';

$user_id=$_SESSION['idUtilisateur'];
//echo "ID : ".$user_id.". ";

$CaptureUserDate=$_POST['lundi'];

//fonctions
function monPrint_r($table){
    $customPre = "<pre>";
    $customPre .= print_r($table, true); // true, retourne le résultat de print_r
    $customPre .= "</pre>";
    return $customPre;
}

$dbh = new PDO("mysql:host=$serverName;dbname=$dbName", $userName, $password);

$sqlCompteur ="SELECT Capture, DateCapture FROM Projet_kwapp.Compteur 
                WHERE Projet_kwapp.Compteur.DateCapture='$CaptureUserDate'
                ORDER BY Projet_kwapp.Compteur.DateCapture";
//$sql->execute();

/*
 * afficher le resultat
*/

$resultCompteur= $dbh->query($sqlCompteur);

foreach($resultCompteur->fetchAll(PDO::FETCH_ASSOC) as $row){
    echo $row['Capture'];
}
