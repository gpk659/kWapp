<?php
/**
 * Created by PhpStorm.
 * User: Grégory
 * Date: 18-12-17
 * Time: 18:03
 */


session_start();

require '../test.php';

$userOCR=$_SESSION['idUtilisateur'];
//echo "ID : ".$user_id.". ";

$DataCapture=$_POST['dataCaptureOCR'];
$CaptureUserDate=$_POST['timeCaptureOCR'];


//fonctions
function monPrint_r($table){
    $customPre = "<pre>";
    $customPre .= print_r($table, true); // true, retourne le résultat de print_r
    $customPre .= "</pre>";
    return $customPre;
}

$dbh = new PDO("mysql:host=$serverName;dbname=$dbName", $userName, $password);


$sqlInsertOCR = " INSERT INTO Projet_kwapp.Compteur(Capture,DateCapture,idUserCompteur) 
                  VALUES ('$DataCapture','$CaptureUserDate','$userOCR') ;";

$dbh->exec($sqlInsertOCR);
//$sql->execute();

