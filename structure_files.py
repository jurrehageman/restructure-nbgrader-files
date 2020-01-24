#!/usr/bin/env python3
"""
Name: structure_files.py
Purpose: restructure file/path stucture for NB grader.
Author: Jurre Hageman
Created: 2020-01-24
Updated: NA
"""

# Imports
import os
import shutil
import sys
import argparse
import itertools
import warnings


def args():
    "parses command line arguments"
    parser = argparse.ArgumentParser(description="restructures files")
    parser.add_argument("in_dir", help="the path to the directory with the input")
    parser.add_argument("test_name", help="the name of the test")
    parser.add_argument("jupyter_name", help="the name of the jupyter notebook (without file-extension)")
    args = parser.parse_args()
    return args


def peek_generator_object(iterable):
    try:
        first = next(iterable)
    except StopIteration:
        return None
    return first, itertools.chain([first], iterable)


def write_files(src, dst):
    dstfolder = os.path.dirname(dst)
    if not os.path.exists(dstfolder):
        os.makedirs(dstfolder)
        shutil.copy(src, dst)


def recreate_dir_structure(in_dir, test_name, jupyter_name):
    students = []
    dst_file_name = jupyter_name + '.ipynb'
    subfolders = os.walk(in_dir)
    has_content = peek_generator_object(subfolders)
    if not has_content:
        warnings.warn("Dir does not exist or no subfolders foud")
        return
    for subfolder in subfolders:
        warning_flag = False
        st_num = subfolder[0].split('_')[-1]
        print("Processing", st_num)
        if st_num in students:
            warnings.warn("Double submission detected {}".format(st_num))
            continue
        else:
            students.append(st_num)
        st_path = subfolder[0]
        files = subfolder[-1]
        for item in files:
            if item.endswith('.ipynb'):
                file_name = item
            else:
                warnings.warn("Other filetype found: {}".format(item))
                warning_flag = True
        if warning_flag:
            continue
        src = os.path.join(st_path, file_name)
        dst = os.path.join('submitted', st_num, test_name, dst_file_name)
        write_files(src, dst)


def main():
    comm_args = args()
    in_dir = comm_args.in_dir
    test_name = comm_args.test_name
    jupyter_name = comm_args.jupyter_name
    recreate_dir_structure(in_dir, test_name, jupyter_name)
    print("Done restructuring files")
    return 0


if __name__ == "__main__":
    sys.exit(main())