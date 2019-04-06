#!bash
exec 3<>/dev/tcp/127.0.0.1/port # I can't remember port number.
read -r -u -n $MESSAGE <&3
echo $MESSAGE
