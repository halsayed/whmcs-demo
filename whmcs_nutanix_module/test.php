<?php
$value = "testHello";

$command = "python3 client.py $value 2>&1";
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
echo $output;
