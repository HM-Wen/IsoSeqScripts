#! /usr/env python

# Script to demultiplex barcoded full-length isoseq reads into their own 
# individual fasta files (barcodes are referred to as primers in the sequence
# files because they are technically custom primers. Will use primer/barcode
# interchangably)

import re
import sys
import os
import argparse
import textwrap
from Bio import SeqIO  # 
from tqdm import *

FILE_NAME_REGEXP = r'(.+)\..+'
PRIMER_REGEXP = r"primer\=(\d+)"

def mkFastaFolder():
    """Makes a new folder for parsed data, returns newfolder path for use"""
    currPath = os.getcwd()  # grab path to current working directory
    newFolderPath = os.path.join(currPath, "demultiplexed")
    
    # If the folder isn't there, make it.
    if not os.path.exists(newFolderPath):
        os.makedirs(newFolderPath)

    return newFolderPath

def checkInputFile(inputFileArg):
    """Make sure the file exists"""
    if not os.path.exists(inputFileArg):
        print "Input fasta file not found. Check path."
        sys.exit(1)

def rmEmptyFiles(newFolderPath):
    """Clean up any empty files that did not contain any sequences"""
    
    # Get the list of files to check
    onlyFiles = []
    if os.path.exists(newFolderPath): # Check if folder exists first
        for item in os.listdir(newFolderPath): 
            itemFullPath = os.path.join(newFolderPath, item) # get full path
            if os.path.isfile(itemFullPath):  # check, file or other (e.g dir)
                onlyFiles.append(itemFullPath)
    
    # Remove any files with no sequences
    for file in onlyFiles:
        statinfo = os.stat(file)  # get info on files
        if statinfo.st_size == 0:  # if filesize is 0 bytes
            os.remove(file)

def parseInput():
    """Use argparse to handle user input for program"""
    
    # Create a parser object
    parser = argparse.ArgumentParser(
        prog="DemultiplexFlncFasta.py",
        
        formatter_class=argparse.RawDescriptionHelpFormatter,
        
        description="""Demultiplexes the 'isoseq_flnc.fasta' input file 
        according to the custom primer (barcode) number in each fasta header.
        The 6 possible barcodes are numbered 0-5. Fastas are output to a new 
        folder called 'demultiplexed' in the run directory.""")
    parser.add_argument("input", help="name of or path to isoseq_flnc.fasta")
    
    parser.add_argument("-v", "--version", action="version",
                        version=textwrap.dedent("""\
        %(prog)s
        -----------------------   
        Version:    0.2 
        Updated:    01/23/2015
        By:         Prech Uapinyoying   
        Website:    https://github.com/puapinyoying"""))

    args = parser.parse_args()
    
    return args.input

args_input = parseInput()

if args_input:
    inputFileArg = args_input  # first argument should be path to fasta file
    checkInputFile(inputFileArg) # make sure file exists
    newFolderPath = mkFastaFolder()  # make a new folder for fastas

    # make some new file names and add their full path
    bar0 = os.path.join(newFolderPath, "barcode0_isoseq_flnc.fasta")
    bar1 = os.path.join(newFolderPath, "barcode1_isoseq_flnc.fasta")
    bar2 = os.path.join(newFolderPath, "barcode2_isoseq_flnc.fasta")
    bar3 = os.path.join(newFolderPath, "barcode3_isoseq_flnc.fasta")
    bar4 = os.path.join(newFolderPath, "barcode4_isoseq_flnc.fasta")
    bar5 = os.path.join(newFolderPath, "barcode5_isoseq_flnc.fasta")

    # Open all 6 barcode files
    bar0_writer = open(bar0, "a")
    bar1_writer = open(bar1, "a")
    bar2_writer = open(bar2, "a")
    bar3_writer = open(bar3, "a")
    bar4_writer = open(bar4, "a")
    bar5_writer = open(bar5, "a")

    # Loop thorugh each sequence header in the input file, if primer # in header
    # matches one of the barcodes, output the whole record to its respective file
    for seq_record in tqdm(SeqIO.parse(inputFileArg, "fasta")):
        # seq_record.description gets complete fasta header
        searchObj = re.search(PRIMER_REGEXP, seq_record.description)
        primerNum = searchObj.group(1) # grabs just primer number

        # Output each barcode's sequence records to their own fasta file
        if primerNum == '0':
            SeqIO.write(seq_record, bar0_writer, "fasta")

        elif primerNum == '1':
            SeqIO.write(seq_record, bar1_writer, "fasta")

        elif primerNum == '2':
            SeqIO.write(seq_record, bar2_writer, "fasta")

        elif primerNum == '3':
            SeqIO.write(seq_record, bar3_writer, "fasta")

        elif primerNum == '4':
            SeqIO.write(seq_record, bar4_writer, "fasta")

        elif primerNum == '5':
            SeqIO.write(seq_record, bar5_writer, "fasta")

        else:
            print "That was unexpected! This script can only parse 6 barcodes"
            print seq_record.description
            print "Are you sure barcode{} exists?".format(primerNum)

    # Close all files
    bar0_writer.closed
    bar1_writer.closed
    bar2_writer.closed
    bar3_writer.closed
    bar4_writer.closed
    bar5_writer.closed

    # Clean up any files with no sequences
    rmEmptyFiles(newFolderPath)