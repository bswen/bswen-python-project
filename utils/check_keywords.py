

import sys
import re
import glob
import os
import time

FILE_HOME=os.path.expanduser('~/temp')

sensitive_words="bad_keyword1|bad_keyword2|bad_keyword3"

def check_last_modified_files():

    files = glob.glob(FILE_HOME+"/**",recursive=True) #recursively list the files in the directory
    modified_files = list() #construct an empty list
    current_time = time.time() #get current time

    for the_file in files: # iterate over the files and collect the files that changed in 12 hours
        time_delta = current_time - os.path.getmtime(the_file)
        time_delta_hours = time_delta / (60*60)
        if time_delta_hours < 12:
            modified_files.append(the_file)
    return modified_files


def is_sensitive():
    modified_files = check_last_modified_files()
    print("got "+str(len(modified_files))+" changed files")
    for mfile in modified_files:
        if not os.path.isfile(mfile): continue  #check if the file is a directory or a file, if it is not a file, do not process it
        print("checking "+mfile+"...")
        file = open(mfile, 'r') #open the file for read
        try:
            lines = file.readlines() #read the lines in the file
            line_count = 0
            for line in lines:
                line_count= line_count+1
                if re.search(sensitive_words,line,re.IGNORECASE): #check the content with the keywords, using re.IGNORECASE to be case insensitive
                    print("\nfind sensitive line:\n"+line+"\nin file:"+mfile+":"+str(line_count))
                    return True #if sensitive keyword is found, break the process

            pass
        except:
            print('unexpected error %s' % mfile, sys.exc_info())
            pass
    return False

if __name__ == '__main__':
    if is_sensitive():
        print("\nis sensitive true")
    else:
        print("\nnormal files,no issue found")
