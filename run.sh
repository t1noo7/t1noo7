#!/bin/bash
printf "\033c"
rm -rf writer.sh

# Nhận username và id từ biến môi trường thay vì nhập tay
username=${USERNAME:-"default_username"}
id=${ID:-"default_id"}

# Tạo script writer.sh
echo 'echo "Now just go and relax, you will be notified when the process is completed"; sleep 5' > writer.sh

if  ls components/main.py >/dev/null 2>/dev/null ; then
    python components/main.py --username "$username" --id "$id"   # Chạy script với username và id
    echo 'notify-send "Github Name Writer Process completed" 2>/dev/null' >> writer.sh
    echo 'Task Completed...'
else
    echo 'Make sure you have all the files at correct places'
fi
