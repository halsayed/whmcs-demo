<?php

function pythonClient($value) {

    $python_file= dirname(__FILE__) . DIRECTORY_SEPARATOR . 'client.py';
    $command = "python3 $python_file $value 2>&1";
    $pid = popen( $command,"r");
    $output = "";

    while( !feof( $pid ) )
    {
        $output .= fread($pid, 256);
        flush();
//    ob_flush();
        usleep(100000);
    }
    pclose($pid);
    return $output;
}