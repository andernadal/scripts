#!/usr/bin/expect -f
set timeout 10
set host [lindex $argv 0]

#SSH connection using a jump server, change if it's necessary
spawn ssh -o StrictHostKeyChecking=no admin@$host

expect {
  timeout { send_user "\nFailed to get password prompt\n"; exit 1 }
  eof { send_user "\nSSH failure for $hostname\n"; exit 1 }
  "*assword: " {
    send "Password_must_be_changed\r"
  }
}
#Check if it's necessary or not
#expect "*?assword: "
#send -- "MY_PASS\r"
sleep 2
expect "*?assword:*"
send -- "Password_must_be_changed\r"
sleep 1
expect "*#"
send -- "term leng 0\r"
expect "*#"
sleep 1
send -- "show inventory\r"
sleep 1
expect "*#"
send -- " admin show inventory\r"
sleep 1
expect "*#"
send -- "exit\r"
expect eof

