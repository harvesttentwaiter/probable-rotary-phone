<?php

$dns=$_REQUEST["dns"];
echo "$dns is dns to check<br>\n";
if (0 == preg_match("/^[a-z0-9\\-.]+$/", $dns)) {
    echo "bad dns\n";
} else
{   
    echo "<pre>";
    system("(echo GET / HTTP/1.1;echo User-Agent: CheckCert;echo)|openssl s_client -connect $dns:443 -showcerts|sed -e '/^Verification/,\$d' | gpg --homedir=~/chkcrt-gpg --clearsign 2>&1");
    echo "</pre>done\n";
}
/*
gpg2 --batch --homedir=~/chkcrt-gpg --gen-key <<EOF
%no-protection
Key-Type:1
Key-Length:2048
Name-Real: chkcrt
Expire-Date:44y
EOF
*/
?>

