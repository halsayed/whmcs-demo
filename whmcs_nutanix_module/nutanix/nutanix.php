<?php
include 'lib/nutanix_client.php';
include "lib/wrapper.php";

if (!defined("WHMCS")) {
    die("This file cannot be accessed directly");
}


function nutanix_MetaData()
{
    return array(
        'DisplayName' => 'Nutanix VM',
        'APIVersion' => '1.1', // Use API Version 1.1
        'RequiresServer' => true, // Set true if module requires a server to work
        'ServiceSingleSignOnLabel' => 'Login to Panel as User',
        'AdminSingleSignOnLabel' => 'Login to Panel as Admin',
    );
}


function nutanix_ConfigOptions()
{
    return [
        "username" => [
            "FriendlyName" => "UserName",
            "Type" => "text",
            "Size" => "25",
            "Description" => "Textbox",
            "Default" => "admin"
        ],
        "password" => [
            "FriendlyName" => "Password",
            "Type" => "password",
            "Size" => "25",
            "Description" => "Password",
            "Default" => "Example"
        ],
        "cluster" => [
            "FriendlyName" => "Project",
            "Type" => "dropdown",
            "Description" => "Calm Project (not used)",
            "Options" => "Default,Windows,Linux",
            "Default" => "Default"
        ],
        "package" => [
            "FriendlyName" => "Package Name",
            "Type" => "dropdown", # Dropdown Choice of Options
            "Options" => "Windows 2016 - Medium,Windows 2016 - Large,Ubuntu 20 - Small,Ubuntu 20 - Medium,CentOS 7 - Small,CentOS 7 - Medium",
            "Description" => "OS and Profile size",
            "Default" => "Windows 2016 - Medium",
        ],
    ];
}

function nutanix_CreateAccount(array $params)
{
    try {
        $result = python_call('blueprint.launch', $params);
        logModuleCall('nutanix', __FUNCTION__, $params, $result);
    } catch (Exception $e) {
        // Record the error in WHMCS's module log.
        logModuleCall(
            'nutanix', __FUNCTION__, $params, $e->getMessage(), $e->getTraceAsString());
        return $e->getMessage();
    }

    return 'success';
}

function nutanix_SuspendAccount(array $params)
{
    try {
        $result = python_call('application.stop', $params);
        logModuleCall('nutanix', __FUNCTION__, $params, $result);
    } catch (Exception $e) {
        // Record the error in WHMCS's module log.
        logModuleCall('nutanix', __FUNCTION__, $params, $e->getMessage(), $e->getTraceAsString());
        return $e->getMessage();
    }

    return 'success';
}

function nutanix_UnsuspendAccount(array $params)
{
    try {
        $result = python_call('application.start', $params);
        logModuleCall('nutanix', __FUNCTION__, $params, $result);
    } catch (Exception $e) {
        // Record the error in WHMCS's module log.
        logModuleCall('nutanix', __FUNCTION__, $params, $e->getMessage(), $e->getTraceAsString());
        return $e->getMessage();
    }

    return 'success';
}

function nutanix_TerminateAccount(array $params)
{
    try {
        $result = python_call('application.delete', $params);
        logModuleCall('nutanix', __FUNCTION__, $params, $result);
    } catch (Exception $e) {
        // Record the error in WHMCS's module log.
        logModuleCall('nutanix', __FUNCTION__, $params, $e->getMessage(), $e->getTraceAsString());
        return $e->getMessage();
    }

    return 'success';
}

function nutanix_ChangePassword(array $params)
{
    try {
        $result = python_call('application.update_password', $params);
        logModuleCall('nutanix', __FUNCTION__, $params, $result);
    } catch (Exception $e) {
        // Record the error in WHMCS's module log.
        logModuleCall('nutanix', __FUNCTION__, $params, $e->getMessage(), $e->getTraceAsString());
        return $e->getMessage();
    }

    return 'success';
}



