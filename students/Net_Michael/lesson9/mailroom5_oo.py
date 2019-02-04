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

#
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


''' prints thank you laters for their last donation and summary report of all
    donors in the database'''

class allDonors_output(oneDonor):
    def __init__(self, all_donors):
        #self.all_donors = self.all_donors
        self.list_donors = dict(all_donors)
        self.donors = list(self.list_donors.keys())
        self.all_gifts = list(self.list_donors.values())
    ##
    def create_report(self):
        print("Name\t\t\tTotal Donation\t\tNum Gifts\tAverage Gift")
        rep_list = []
        for ll in range( len(self.donors)):
            aa = oneDonor(  donor_name = self.donors[ll],
                            donation = self.all_gifts[ll])
            aa_report = aa.one_report()
            rep_list.append(aa_report)
        return(rep_list)
    #
    # list of the donors and donation in the database
    #
    def thank_all(self):
        for ll in range( len(self.donors)):
            print('''
                Dear {},
                Thank you for your very kind donation of ${:,.2f}.
                It will be put to very good use.
                                        Sincerely,
                                        -The Team'''.format(self.donors[ll],self.all_gifts[ll][-1]))

#
''' the database where all the donor information is extracted
    using the donor_basename() using the pathname,
    updates donation information by intering new donors or new donations'''

class Donors_DB:
    def __init__(self,directory_path):
        self.directory_path = directory_path
        #
    def donor_database(self):
        filenames = os.listdir(self.directory_path)
        donor_info = []
        for j in range(len(filenames)):
            donor = os.path.splitext(filenames[j])[0].replace("_"," ")
            donations = Donations_amts(directory_path = self.directory_path,
                                       filename = filenames[j])
            donor_info.append((donor, donations))
        return(donor_info)
    #
    def new_donationDB(self):
        # list of donors in the database
        new_filename = donor_filename(suffix = "") #
        donor_name = os.path.splitext(new_filename)[0].replace("_"," ")
        new_donation = input("Amount of donation by {} ".format(donor_name))
        donation_path = os.path.join(self.directory_path, new_filename)
        if (new_filename not in os.listdir(self.directory_path)):
            new_file = open(donation_path, 'w')
            new_file.write(new_donation)
            new_file.close()
            print("{} is a new donor".format(donor_name))
        else:
            new_donation = ', ' + str(new_donation)
            append_file = open(donation_path, 'a')
            append_file.write(new_donation)
            append_file.close()
        # update donor-Information
        donor_info = self.donor_database()
        return(donor_info)    #


''' given filename and directory path
    output - list of donations made across time
    donation[0] is first donation
'''

def Donations_amts(directory_path, filename):
    file_path = "\\".join([directory_path, filename])
    donor_lists = open(file_path)
    donation = donor_lists.read()
    donation = donation.split(', ')
    donation = [float(x) for x in donation]
    donor_lists.close()
    return(donation)

''' list all files in the given drive of the machine... say c:\ '''

def list_dir_path():
    root = os.path.dirname( os.getcwd())
    root = "\\".join(root.split("\\")[:2])
    for path, subdir, file in os.walk(root):
        for dirname in subdir:
            dir_info = str(os.path.join(dirname))
            yield dir_info, path

''' converts the donation info to create file containing donations accross time'''

def donor_filename(suffix = ""):
    firstname = input("Donor's firstname " ).title()
    lastname = input("Donor's lastname ").title()
    suffix = input("Donor's suffix ")
    if suffix == "" :
        file_name = "".join([firstname, "_", lastname, ".txt"])
    else:
        file_name = "".join([firstname, "_", lastname,"_", suffix, ".txt"])
    return(file_name)

# output promt functions

def thank_one(all_donors):
    filename = donor_filename(suffix = "")
    donor_name = input("donor's full name ").title()
    donation = dict(all_donors)[donor_name][-1]
    thank_you = oneDonor(donor_name, donation).letter_format(self)
    return(thank_you)

def prepare_reports(all_donors):
    report = allDonors_output(all_donors = all_donors).create_report()
    return(report)

def thank_all(all_donors):
    letters = allDonors_output(all_donors = all_donors).thank_all()
    return(letters)


def new_donation_entry(directory_path):
    update_donors = Donors_DB(directory_path).new_donationDB()
    return(update_donors)


def quit_sel():
    raise SystemExit(1)
    #

main_sel = {
        1: thank_all_letter,
        2: write_report,
        3: thank_one_donor,
        4: enter_donation,
        5: quit_sel,
        }

prompt = "\n".join(("Welcome",
          "Please choose from below options: ",
          "1 - Send Thank you to all donors",
          "2 - Create a Report ",
          "3 - Send Thank you to donor ",
          "4 - Enter new donation ",
          "5 - Quit",
          ">>> "))


if __name__ == "__main__":
    print('''Please wait to list all the filepaths in the machine''')
    all_dir_list = list(list_dir_path())
    #
    dir_patha = dirLocDonor(foldername1 = "donor_file_save",
                            foldername2 = "lesson6",
                             all_dir_list = all_dir_list)
    #
    directory_path = dir_patha.pathdirectory()
    list_files = os.listdir(directory_path)
    if(len(list_files) > 0):
        all_donors_DB = Donors_DB(directory_path = directory_path)
        all_donors = all_donors_DB.donor_database()
        while True:
            sel_choice = eval(input(prompt))
            if sel_choice == 1:
                enter_donation = new_donation_entry(directory_path = directory_path)
                main_sel.get(sel_choice)
            elif sel_choice == 2:
                 write_report = prepare_reports(all_donors = all_donors)
                 main_sel.get(sel_choice)
            elif sel_choice == 3:
                thank_one_letter = thank_one(all_donors = all_donors)
                main_sel.get(sel_choice)
            elif sel_choice == 4:
                thank_all_letter = thank_all(all_donors = all_donors)
                main_sel.get(sel_choice)
            elif sel_choice == 5:
                main_sel_get(sel_choice)
            else:
                print("\n choose less than 4 or press 4 to exit\n")
