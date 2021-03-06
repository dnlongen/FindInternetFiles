FindInternetFiles
=============

Recurse through a Windows directory, looking for any files originally downloaded from the Internet.

* Written by David Longenecker
* Twitter: @dnlongen
* Email: david (at) securityforrealpeople.com

Windows Vista and newer automatically attach an Alternate Data Stream, or ADS, to all Internet downloads. This ADS is titled "Zone.Identifier" and contains a single value: ZoneID=3. Files from other origins may have a Zone Identifier as well; Microsoft defines the following zones:

* 0 = URLZONE_LOCAL_MACHINE
* 1 = URLZONE_INTRANET
* 2 = URLZONE_TRUSTED
* 3 = URLZONE_INTERNET
* 4 = URLZONE_UNTRUSTED

I wrote this script on the following premise: most malware comes from the Internet rather than being compiled locally or copied from another device on the local network. On the other hand, most Windows system files and legitimate programs (even if they come via an Internet update) are not tagged with the URLZONE_INTERNET zone identifier. Thus, recursively scanning a local hard drive for anything that originated on the Internet might reveal potentially suspicious files. 

In particular, anything in *c:\windows,* *c:\program files(x86)*, or *c:\program files* that comes from the Internet might be suspicious.

By default the script excludes everything under c:\users - browser history, downloaded documents, and other such user-specific content will in many cases be overwhelming. The --fullscan parameter disables this exclusion and will look for ANYTHING downloaded from the Internet.

Caveat: in my testing it appears downloaded archives (.zip, etc.) are themselves tagged with a zone identifier, but the extracted contents are not.

Hat tip to David Robin, whose pyADS library (https://github.com/RobinDavid/pyADS) is used by this script.

Requirements:
=============

* Currently written for **Python 3**
* requires argparse, sys, os
* requires pyADS (included here, source https://github.com/RobinDavid/pyADS)
* Uses the Windows API to recurse through a live local Windows directory tree

Usage:
=============

```
FindInternetFiles.py [-h] [-f] [-v] rootdir

View the alternate data streams of a file. Specifically look for the
Zone.Identifier ADS and identify files downloaded from the Internet.

positional arguments:
  rootdir         Root directory; will scan all files and folders beneath th
                  location

optional arguments:
  -h, --help      show this help message and exit
  -f, --fullscan  Scan all files. By default, will ignore any files in
                  Temporary Internet Files (which one would expect to come
                  from the Internet)
  -v, --verbose   Verbose output
```

Findings:
=============
In some testing among a handful of systems I have, %systemroot% and %programfiles% have very few if any files with an ADS of ZoneID=3. However, Windows 7 and newer make it harder for an adversary to put files here. %AppData and %Temp% are available to an attacker without privileged escalation - and they also rarely have non-malicious Internet-downloaded files. Scanning those four locations could be useful.

As long as you have a mapped file share, FindInternetFiles will just as happily scan a remote system (FindInternetFiles.py \\hostname\share) as scan a local filesystem. Useful for scripting scans across a range of systems.

Change Log:
=============

* v0.1 Original release.
