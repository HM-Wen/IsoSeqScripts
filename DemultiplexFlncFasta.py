#! /usr/env python

# Script to demultiplex barcoded full-length isoseq reads into their own 
# individual fasta files (barcodes are referred to as primers in the sequence
# files because they are technically custom primers. Will use primer/barcode
# interchangably)

# http://biopython.org/DIST/docs/tutorial/Tutorial.html
from Bio import SeqIO
from tqdm import *
import re
import sys
import os

USAGE = """
### DemultiplexFlncFasta.py ###
v0.1 
01/06/2015
by Prech Uapinyoying

USAGE: 
---------------------------------------------------------

> DemultiplexFlncFasta.py [/path/to/isoseq_flnc.fasta]

Demultiplexes the 'isoseq_flnc.fasta' file according to the custom primer 
(barcode) number in the header.  Barcodes are numbered 0-5. Fastas are
output to a new folder called 'demultiplexed' in the run directory.

"""

FILE_NAME_REGEXP = r'(.+)\..+'
PRIMER_REGEXP = r"primer\=(\d+)"

def mkFastaFolder(newFolderName="demultiplexed"):
    """Makes a new folder for parsed data"""
    currPath = os.getcwd()
    newFolderPath = os.path.join(currPath, newFolderName)
    if not os.path.exists(newFolderPath):
        os.makedirs(newFolderPath)
    return newFolderPath

def checkInputFile(inputFileArg):
    if not os.path.exists(inputFileArg):
        print "Input fasta file not found. Check path."
        sys.exit(0)

numArgs = len(sys.argv)

# If no input, display usage info
if numArgs == 2:

    inputFileArg = sys.argv[1]  # first argument should be path to fasta file
    checkInputFile(inputFileArg) # make sure file exists
    newFolderPath = mkFastaFolder()  # make a new folder for fastas

    # make some new file names
    bar0 = os.path.join(newFolderPath, "barcode0_isoseq_flnc.fasta")
    bar1 = os.path.join(newFolderPath, "barcode1_isoseq_flnc.fasta")
    bar2 = os.path.join(newFolderPath, "barcode2_isoseq_flnc.fasta")
    bar3 = os.path.join(newFolderPath, "barcode3_isoseq_flnc.fasta")
    bar4 = os.path.join(newFolderPath, "barcode4_isoseq_flnc.fasta")
    bar5 = os.path.join(newFolderPath, "barcode5_isoseq_flnc.fasta")

    # Loop thorugh each sequence header, if primer # in header matches one of
    # the barcodes, output the whole record to its respective file
    for seq_record in tqdm(SeqIO.parse(inputFileArg, "fasta")):
        
        # seq_record.description gets complete fasta header
        searchObj = re.search(PRIMER_REGEXP, seq_record.description)
        primerNum = searchObj.group(1) # grabs just primer number

        # Output each barcode's sequence records to their own fasta file
        if primerNum == '0':
            output_handle = open(bar0, "a") # a is for append
            SeqIO.write(seq_record, output_handle, "fasta")
            output_handle.close()

        elif primerNum == '1':
            output_handle = open(bar1, "a")
            SeqIO.write(seq_record, output_handle, "fasta")
            output_handle.close()

        elif primerNum == '2':
            output_handle = open(bar2, "a")
            SeqIO.write(seq_record, output_handle, "fasta")
            output_handle.close()

        elif primerNum == '3':
            output_handle = open(bar3, "a")
            SeqIO.write(seq_record, output_handle, "fasta")
            output_handle.close()

        elif primerNum == '4':
            output_handle = open(bar4, "a")
            SeqIO.write(seq_record, output_handle, "fasta")
            output_handle.close()

        elif primerNum == '5':
            output_handle = open(bar5, "a")
            SeqIO.write(seq_record, output_handle, "fasta")
            output_handle.close()

        else:
            print "That was unexpected! This script can only parse 6 barcodes"
            print seq_record.description
            print "Are you sure barcode{} exists?".format(primerNum)

else:
    print USAGE