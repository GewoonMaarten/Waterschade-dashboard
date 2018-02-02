#!/usr/bin/env perl

# Copyright (c) 2017, Chris Smeele
# Console for output-only monitoring of a Bluetooth LE device.

# Find the device MAC address as follows:
#
# % sudo hcitool lescan
# LE Scan ...
# D4:36:39:9C:C1:E9 (unknown)
# D4:36:39:9C:C1:E9 Wair-001
#
# Test the connection as follows:
#
# % gatttool -I -b D4:36:39:9C:C1:E9
# [D4:36:39:9C:C1:E9][LE]> connect
# Attempting to connect to D4:36:39:9C:C1:E9
# Connection successful
# Notification handle = 0x0012 value: 7b 22 75 70 74 69 6d ...
#
# If you get output similar to the above you should be able to use this script
# to receive decoded messages.

use 5.12.0;
use warnings;

use IPC::Open2;

my $addr = (@ARGV
            ? (shift)
            : q(D4:36:39:9C:BE:FF));

sub slurp{
  open(my $fh, '<', shift) or die $!;
  <$fh>
}

system("python3 WifiService.py");
#system("cd ../../\npython3 WifiService.py");

my @rawding = slurp "application_logic/sensor_controller/test.txt";

my $text0 = substr $rawding[0], 0, -1;
my $text1 = substr $rawding[1], 0, -1;

my $precmd = "sudo sh -c 'echo \"ctrl_interface=/var/run/wpa_supplicant\n\" > /etc/wpa_supplicant/wpa_supplicant.conf'";
system($precmd);

my $cmd = "sudo sh -c 'wpa_passphrase $text0 $text1 >> /etc/wpa_supplicant/wpa_supplicant.conf'";
system($cmd);

my $ding = (join '', @rawding);
say $ding;


# Note: This is completely silent on error, so run the command
# manually if you need to debug your connection.

my $gatt_pid = open2(my $gatt_out,
                     my $gatt_in,
                     qw(gatttool -I),
                     -b => $addr);


my $really_kill = 0;
$SIG{INT} = sub {
    if ($really_kill) {
        say STDERR "\rACK!";
        kill KILL => $gatt_pid;
    } else {
       say STDERR "\rInterrupt again to force quit.";
        $really_kill = 1;
        close $gatt_in;
    }
};

my @hex_ding = map unpack("H*"), split(//, $ding);

say $gatt_in "connect";

sleep(1);

for (@hex_ding){
  say $gatt_in "char-write-cmd 0x0012 $_";
}

# for @ding -> $letter{
#   say
# }


#$| = 1;

# while (<$gatt_out>) {
#     chomp;
#     if (/Notification handle = \S+ value:\s*(.*?)$/i) {
#         # Hex decode...
#         print pack "H*", ($1 =~ s/\s//gr);
#     }
# }
sleep(2);
say $gatt_in "quit";
close $gatt_out;
close $gatt_in;
kill "KILL" => $gatt_pid;
waitpid $gatt_pid, 0;
