'''
FindInternetDownloads v0.1
Source: https://github.com/dnlongen/FindInternetDownloads
Author: David Longenecker
Author email: david@securityforrealpeople.com 
Author Twitter: @dnlongen
Uses pyADS library written by David Robin, source https://github.com/RobinDavid/pyADS
'''

import sys, os, argparse
from pyADS import ADS

# Define supported parameters and default values
parser = argparse.ArgumentParser(description='View the alternate data streams of a file. Specifically look for the Zone.Identifier ADS and identify files downloaded from the Internet.')
parser.add_argument('rootdir', help='Root directory; will scan all files and folders beneath this location')
parser.add_argument('-f', '--fullscan', dest='fullscan', action='store_true', help='Scan all files. By default, will ignore any files in Temporary Internet Files (which one would expect to come from the Internet)')
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Verbose output')
parser.set_defaults(fullscan=False,verbose=False)
args=parser.parse_args()
rootdir=args.rootdir
fullscan=args.fullscan
verbose=args.verbose

# Define excluded directories. The loop will exclude EVERYTHING below each directory listed.
excludes=['c:\\users']

if __name__ == '__main__':
  print("Files downloaded from the Internet:")
  for subdir, dirs, files in os.walk(rootdir, topdown=True):
    if not fullscan: 
      if subdir.lower() in excludes: dirs[:] = []
    for file in files:
      filename=os.path.join(subdir, file)
      handler = ADS(filename)
      try:
        if handler.getStreamContent("Zone.Identifier") == b'[ZoneTransfer]\r\nZoneId=3\r\n': print (filename)
      except:
        if verbose:
          print("[NOT INTERNET]" + filename)
  print("---------------------------------")
