#!/usr/bin/perl

# Perl trim function to remove whitespace from the start and end of the string
sub trim($) {
	my $string = shift;
	$string =~ s/^\s+//;
	$string =~ s/\s+$//;
	#$string =~ s/\,//;
	return $string;
}


sub pretrim($) {
	my $string = shift;
	#$string =~ s/^\s+//;
	#$string =~ s/\s+$//;
	$string =~ s/supply, 6000/supply 6000/;
	$string =~ s/SFP.{2},/SFP /;
	$string =~ s/Cisco Systems, Inc./Cisco Sys Inc/;
	return $string;
}

# Left trim function to remove leading whitespace
sub ltrim($) {
	my $string = shift;
	$string =~ s/^\s+//;
	return $string;
}
# Right trim function to remove trailing whitespace
sub rtrim($) {
	my $string = shift;
	$string =~ s/\s+$//;
	return $string;
}
# Remove everything that's not a letter, numeral, or a "_" (underscore)
sub strip($) {
	my $string = shift;
	$string =~ s/[^\w\d]//g;
	return $string;
}



$dirname = '.';
opendir(DIR, $dirname) or die "Could not open $dirname\n";

$resultfile = "result.csv";
open (RESULT, ">>$resultfile");




while ($filename = readdir(DIR)) {

		if ($filename =~ /^*.txt/i) {
			#print "$filename\n";


			# write >, read <, append >>
			open (FILE, "<$filename");

			while (<FILE>) {
				chomp;
				#print $_ . "\n";
				#print RESULT $_ . "\n";
				$_ = pretrim($_);
				if ($_ =~ /^NAME/) {
					print RESULT "\"$filename\",";
					print "$filename\t";

					@nameCOMAsplit = split (',',$_);
					$nameCOMA = @nameCOMAsplit[0];
					@namesplit = split(':',$nameCOMA);
					$name = @namesplit[1];
					$Cname = trim($name);
					print RESULT $Cname . ",";
					print $Cname . "\t";

					$descCOMA = @nameCOMAsplit[1];
					@descsplit = split(':',$descCOMA);
					$desc = @descsplit[1];
					$Cdesc = trim($desc);
					print RESULT $Cdesc . ",";
					print $Cdesc . "\t";

				}

				if ($_ =~ /^PID/) {

					@pidCOMAsplit = split (',',$_);
					$pidCOMA = @pidCOMAsplit[0];
					@pidsplit = split(':',$pidCOMA);
					$pid = @pidsplit[1];
					$Cpid = trim($pid);
					print RESULT "\"" . $Cpid . "\",";
					print $Cpid . "\t";


					$serialCOMA = @pidCOMAsplit[2];
					@serialsplit = split(':',$serialCOMA);
					$serial = @serialsplit[1];
					if ($serial =~ /([A-Qa-z0-9]+)/) {
					} else {
						$serial = "null";
					}


					$Cserial = trim($serial);
					print RESULT "\"" . $Cserial . "\"\n";
					print $Cserial . "\n";

				}

				if ($_ =~ /^UPOE/) {

					print RESULT "\"$filename\",";
					print RESULT "\"UPOE\",\"Null\",";
					print  "\"UPOE\"\t";
				}

			}

			close (FILE);
		}

}

closedir(DIR);
close (RESULT);
