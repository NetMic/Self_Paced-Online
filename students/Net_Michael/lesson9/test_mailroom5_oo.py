#!/usr/bin/env python
# coding: utf-8

import pytest
#import mailroom5_oo as ml
from mailroom5_oo import *


# test if directory_path can find the directory path of donor_list (
# folder containing all donor text files)

def test_list_dir_path():
    test_dir_list = list(list_dir_path())
    files_in_list = len(test_dir_list)
    assert files_in_list > 1

def test_dirLocDonorh():
    all_dir_list = list(list_dir_path())
    test_path = dirLocDonor(foldername1 = "donor_file_save",
                               foldername2 = "lesson6",
                               all_dir_list = all_dir_list).pathdirectory()
    directories = test_path.split("\\")
    assert "donor_file_save" == directories[-1]

def test_all_donors():
    directory_path = 'C:\\Users\\Netsanet\\Desktop\\UW_courses\\UWpython\\Self_Paced-Online\\students\\Net_Michael\\lesson6\\donor_file_save'
    donors = Donors_DB(directory_path = directory_path).donor_database()
    assert  donors[1][0] == 'Ammy Clay'
