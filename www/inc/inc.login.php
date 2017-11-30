<?php
/**
 * Created by PhpStorm.
 * User: Grégory
 * Date: 24-11-17
 * Time: 13:39
 * Formulaire de login page administration
 */
?>
<!DOCTYPE HTML>
<html>
<head>
    <title>kWapp</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <!--[if lte IE 8]><script src="assets/js/ie/html5shiv.js"></script><![endif]-->
    <link rel="stylesheet" href="/assets/css/style_login.css" />
    <!--[if lte IE 8]><link rel="stylesheet" href="assets/css/ie8.css" /><![endif]-->
    <!--[if lte IE 9]><link rel="stylesheet" href="assets/css/ie9.css" /><![endif]-->
</head>
<script>
    $('.message a').click(function(){
        $('form').animate({height: "toggle", opacity: "toggle"}, "slow");
    });
</script>
<body class="index">
<!-- Header -->
<header id="header" class="alt">
    <h1 id="logo"><a href="index.html">kWapp</a></h1>
    <nav id="nav">
        <ul>
            <li class="current"><a href="index.html">kWapp.eu</a></li>
        </ul>
    </nav>
</header>


<div class="login-page">
    <div class="form">
        <form class="login-form">
            <h2>Login kWapp</h2><br>
            <input type="text" placeholder="username"/>
            <input type="password" placeholder="password"/>
            <button>login</button>
        </form>
    </div>
</div>

<!-- Scripts -->
<script src="assets/js/jquery.min.js"></script>
<script src="assets/js/jquery.dropotron.min.js"></script>
<script src="assets/js/jquery.scrolly.min.js"></script>
<script src="assets/js/jquery.scrollgress.min.js"></script>
<script src="assets/js/skel.min.js"></script>
<script src="assets/js/util.js"></script>
<!--[if lte IE 8]><script src="assets/js/ie/respond.min.js"></script><![endif]-->
<script src="assets/js/main.js"></script>

</body>
</html>