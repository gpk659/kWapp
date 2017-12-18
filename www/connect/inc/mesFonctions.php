<?php
/**
 * Created by PhpStorm.
 * User: Grégory
 * Date: 18-12-17
 * Time: 09:39
 */

//fonctions
function monPrint_r($table){
    $customPre = "<pre>";
    $customPre .= print_r($table, true); // true, retourne le résultat de print_r
    $customPre .= "</pre>";
    return $customPre;
}

//fonction pour gerer la connexion et la session utilisateur

