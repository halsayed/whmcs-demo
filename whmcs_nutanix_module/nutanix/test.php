<?php

include 'lib/wrapper.php';

$payload = [
    'serverip' => '10.38.11.9',
    'serverusername' => 'admin',
    'serverpassword' => 'nx2Tech911!',
    'configoption4' => 'Ubuntu 20 - Small',
    'userid' => '121',
    'accountid' => '33',
    'packageid' => '44',
    'password' => 'nutanix/4u'
];

print_r(python_call('blueprint.launch', $payload));
