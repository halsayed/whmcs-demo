<?php

function python_call($python_module, $payload) {

    $python= dirname(__FILE__).'/python/bin/python';
    $wrapper = dirname(__FILE__).'/wrapper.py';
    $payload_b64 = base64_encode(json_encode($payload));

    $command = "$python $wrapper $python_module $payload_b64 2>&1";
    $pid = popen( $command,"r");
    $output = "";

    while( !feof( $pid ) )
    {
        $output .= fread($pid, 256);
        flush();
        usleep(100000);
    }
    pclose($pid);

    $result_key = 'result=[';
    $closing_char = ']';
    $result_start = strpos($output, $result_key) + strlen($result_key);
    $result_end = strpos($output, $closing_char, $result_start);
    $result_b64 = substr($output, $result_start, $result_end-$result_start);
    $console = substr($output, 0, $result_start-strlen($result_key)).substr($output,$result_end+1);

    return [
        'console' => $console,
        'result' => json_decode(base64_decode($result_b64)),
    ];

}