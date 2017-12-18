<?php
/**
 * Created by PhpStorm.
 * User: Grégory
 * Date: 07-12-17
 * Time: 14:20
 */

session_start();

echo "Déconnexion : ";
if (isset($_SESSION)) {
//remove all the session variables
    session_unset();
// destroy the session
    session_destroy();
    if($_SESSION['idUtilisateur']=='' && $_SESSION['NameUser']==''){
        echo "Session vide";
    }else{
        echo "Error";
    }
}else{
    echo "Erreur";
}