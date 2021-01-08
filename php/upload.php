<?php
$file = $_FILES['file'];
if ($file) {
    // 去除非法路径字符 &( )
    $name = str_replace('&', '', str_replace(')', '', str_replace('(', '', str_replace(' ', '', $_POST['file_name']))));
    $info = move_uploaded_file($_FILES['file']['tmp_name'], "/var/www/wx/files/" . $name);
    if ($info) {
        $res = ['errCode' => 0, 'errMsg' => 'upload ok.', 'file' => "/var/www/wx/files/" . $name];
        echo json_encode($res);
    }
}
?>
