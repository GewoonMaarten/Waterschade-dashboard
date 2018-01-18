#!/usr/bin/env perl

# Copyright (c) 2017, Chris Smeele
# Simple readline wrapper for serial I/O.
# Made because the HM-10's AT parser is buggy, which makes direct keyboard input impossible.
# See SteveQuinn's comment on http://www.instructables.com/id/How-to-Use-Bluetooth-40-HM10/

use 5.12.0;
use warnings;

use Term::ReadLine;
use Device::SerialPort;

my $term = Term::ReadLine->new($0 =~ s@.*/@@r);
$term->Attribs->ornaments(0);

my $dev_path = (@ARGV
                ? (shift)
                : sub { my @x = grep { -e } map "/dev/ttyUSB$_", 0..7;
                        die "usage: $0 [device]\n" unless @x;
                        shift @x }->());

say "Using $dev_path";

my $dev = Device::SerialPort->new($dev_path);
$dev->read_char_time(0);
$dev->read_const_time(10);
$dev->databits(8);
$dev->baudrate(9600);
$dev->parity("none");
$dev->stopbits(1);
$dev->write_settings or die "$!";

sub read_stuff {
    # Per https://metacpan.org/pod/Device::SerialPort#EXAMPLE
    my $data;

    for (1..10) {
        my ($n, $d) = $dev->read(255);
        $n and $data .= $d;
    }

    $data
}

while (1) {
    local $_ = $term->readline("hm10> ");
    last unless defined;

    $dev->write($_);
    say read_stuff() // "";
}
