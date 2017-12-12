<?php
/**
 * Created by PhpStorm.
 * User: Grégory
 * Date: 02-12-17
 * Time: 11:24
 */

//variable de base nécéssaire pour la db !
$serverName = "51.255.167.206";
$userName = "kwapp";
$password = "P@ssw0rd";
$dbName = "Kwapp_Projet";
global $dbh;

$dbh = new PDO("mysql:host=$serverName;dbname=$dbName", $userName, $password);


try {
    //echo "réussi";
    // set the PDO error mode to exception
    $dbh->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch(PDOException $e) {  echo "Error: " . $e->getMessage(). "</br>"; }

