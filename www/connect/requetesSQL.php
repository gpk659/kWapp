<?php
/**
 * Created by PhpStorm.
 * User: Grégory
 * Date: 16-12-17
 * Time: 10:58
 */
session_start();

require '../test.php';


//fonctions
function monPrint_r($table){
    $customPre = "<pre>";
    $customPre .= print_r($table, true); // true, retourne le résultat de print_r
    $customPre .= "</pre>";
    return $customPre;
}

$dbh = new PDO("mysql:host=$serverName;dbname=$dbName", $userName, $password);

$sql ="Select idUser,Pseudo from Projet_kwapp.User";
//$sql->execute();

/*
 * afficher le resultat
*/

$result= $dbh ->query($sql);

foreach($result->fetch(PDO::FETCH_ASSOC) as $row){
    echo monPrint_r($row);
}
//echo "Name : ".$_SESSION['NameUser'];