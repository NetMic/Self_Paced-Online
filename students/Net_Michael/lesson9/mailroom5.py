#!/usr/bin/env python
# coding: utf-8
import os
import io
import pathlib
import shutil
import re
import string
from collections import defaultdict

'''
 Assumptions
    Given setup of donor information with
       filename
          firstname_lastname.txt(first_name_lastname_suffix.txt)
       foldersetup
          ~/foldername2/foldername1/filename
       file content
          vector - sequence of donations accross time
                 Eg. filename Paul_Allen.txt
                     300.00, 4858.00, 433.00, 7.23, 343.00
                     where latest donation = 343.00 and
                           first donation = 300.00
# objective
    fileLocDonor - searchs accross filepaths
# input
    last two folders containing the filenames in the machine
# output
    from directory_path
        the entire path where the filename is located
        ~//foldername2//foldername1//filename
    from open_donor_file
        list of donations (sorted by time as the assumption)
'''

class dirLocDonor:
    def __init__(self, foldername1, foldername2, all_dir_list):
        self.foldername1 = foldername1
        self.foldername2 = foldername2
        #
        if isinstance(all_dir_list, list):
            self.all_dir_list = all_dir_list
        else:
            self.all_dir_list = [all_dir_list]
            #
    def pathdirectory(self):
        for j in range(len(self.all_dir_list)):
            if self.all_dir_list[j][0] in self.foldername1 and '.pytest_cache' not in self.all_dir_list[j][1] and self.foldername2 in self.all_dir_list[j][1] :
                sel_dirct = self.all_dir_list[j][1]
        donation_directory = os.path.join(sel_dirct, self.foldername1)
        return(donation_directory)


''' updates list of donors and donation
    donor_name is the name of donor
    donation is the amount of donation
'''

class oneDonor:
    #
    def __init__(self, donor_name, donation):
        self.donor_name = donor_name
        self.donation = donation
        #
        if isinstance(donation, list):
            self.donation = donation
        else:
            self.donation = [donation]
    #
    @property
    def total_gift(self):
        return sum(self.donation)
    @property
    def num_gifts(self):
        return len(self.donation)
    @property
    def avg_gift(self):
        return (self.total_gift / self.num_gifts)
    @property
    def last_donation(self):
        return(self.donation[-1])
    @property
    def list_donations(self):
        print(self.donor_name  + ': ' + ', '.join('{}'.format(d)
                  for d in self.donation))
    @property
    def letter_format(self):
        print('''
              Dear {},
              Thank you for your very kind donation of ${:,.2f}.
              It will be put to very good use.
                                    Sincerely,
                                      -The Team'''.format(self.donor_name,self.last_donation))
    #
    def one_report(self):
        print ('{:23}'.format( self.donor_name),
               '${:^6,.2f}'.format( self.total_gift),
               '{:20}'.format(self.num_gifts),
               '{:14}'.format(""),
               '${:^6,.2f}'.format( self.avg_gift))

# list all files in the given drive of the machine... c:\

def list_dir_path():
    root = os.path.dirname( os.getcwd())
    root = "\\".join(root.split("\\")[:2])
    for path, subdir, file in os.walk(root):
        for dirname in subdir:
            dir_info = str(os.path.join(dirname))
            yield dir_info, path


# donor's file Paul_Allen.txt

def donor_filename(suffix = ""):
    firstname = input("Donor's firstname " )
    lastname = input("Donor's lastname ")
    suffix = input("Donor's suffix ")
    print("donor's filename ")
    if suffix == "" :
        file_name = "".join([firstname, "_", lastname, ".txt"])
    else:
        file_name = "".join([firstname, "_", lastname,"_", suffix, ".txt"])
    print(file_name)
    return(file_name)

''' given filename and directory path
    output - list of donations made across time
    donation[0] is first donation
'''

def donorPathname(all_dir_list):
    foldername1 = input(" \n Please enter the folder names in your directory \n"
                         " containing the list of donors.  \n"
                         "setup ~foldername2\\foldername1\\filename"
                          "\n"
                         " foldername1 = ")
    foldername2 = input(" foldername2 = ")
    donors_path = dirLocDonor( foldername1 = foldername1,
                              foldername2 = foldername2,
                             all_dir_list = all_dir_list)
    #
    path_folder = donors_path.pathdirectory()
    return(path_folder)

def Donations_amts(directory_path, filename):
    file_path = "\\".join([directory_path, filename])
    donor_lists = open(file_path)
    donation = donor_lists.read()
    donation = donation.split(', ')
    donation = [float(x) for x in donation]
    donor_lists.close()
    return(donation)
