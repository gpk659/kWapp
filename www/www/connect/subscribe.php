<?php
/**
 * Created by PhpStorm.
 * User: Grégory
 * Date: 05-12-17
 * Time: 10:48
 */

require '../test.php';
//variable de base nécéssaire pour la db !
$pseudo = $_POST["pseudo"];
$nom = $_POST["nom"];
$prenom = $_POST["prenom"];
$mail = $_POST["email"];
$age = $_POST["age"];
$mdp = $_POST["password"];

$dbh = new PDO("mysql:host=$serverName;dbname=$dbName", $userName, $password);

//requete sql
$sth = $dbh->prepare('INSERT INTO Kwapp_Projet.User (Nom,Prenom,Pseudo,Email,Mot_de_passe,Age)
	VALUES (:nom,:prenom,:pseudo,:mail,:mdp,:age);');
//parametres
$sth->bindParam(':nom', $nom, PDO::PARAM_STR, 25);
$sth->bindParam(':prenom', $prenom, PDO::PARAM_STR, 25);
$sth->bindParam(':pseudo', $pseudo, PDO::PARAM_STR, 15);
$sth->bindParam(':email', $mail, PDO::PARAM_STR, 45);
$sth->bindParam(':password', $mdp, PDO::PARAM_STR, 15);
$sth->bindParam(':age', $age, PDO::PARAM_INT, 3);
$sth->execute();

//test login si login existe
if($sth->fetch() == false) {
    echo "Inscription réussi";
    $destinataire = 'gregpyck.ephec@gmail.com';
    $envoyeur	= 'contact@kwapp.eu';
    $sujet = 'Email de confirmation';
    $message = "Bonjour !\r\nCeci est un email de test.\r\n";
    $headers = 'From: '.$envoyeur . "\r\n" .
        'Reply-To: '.$envoyeur. "\r\n" .
        'X-Mailer: PHP/' . phpversion();
    $envoye = mail($destinataire, $sujet, $message, $headers);
    if ($envoye)
        echo "<br />Email envoyé.";
    else
        echo "<br />Email refusé.";
}else {echo "ERROR - Il manque peut-être un champ...";}
