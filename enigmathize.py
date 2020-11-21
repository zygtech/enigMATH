#!/usr/bin/env python3
"""Author: Krzysztof Hrybacz <krzysztof@zygtech.pl>"""
"""License: GNU General Public License -- version 3"""

import sys,os,shutil,hashlib

def main():
    if len(sys.argv)!=4 and len(sys.argv)!=3:
        print("ENIGMATHIZER: Creates EnigMATH protected ZIP package for large files.\nUsage: enigmathize.py <outputzipname> <file or folder name> <formula>\nOr to decrypt: enigmathize.py <enigmathizer zip file> <formula>\nExample: enigmathize.py ZipName /Folders \"(pi+cos(#*30))*100/sqrt(3)\"")
        quit()
    if len(sys.argv)==4:
        zipname = sys.argv[1]
        foldername = sys.argv[2]
        formula = sys.argv[3]
    if len(sys.argv)==3:
        unpackname = sys.argv[1]
        formula = sys.argv[2]
        if unpackname[-13:]!='.enigmath.zip':
            print("ENIGMATHIZER: Creates EnigMATH protected ZIP package for large files.\nScript unpacks only files with extension .enigmath.zip!")
            quit()
    if formula.count('#')==0:
        print("ENIGMATHIZER: Creates EnigMATH protected ZIP package for large files.\nUse variable # as iterator at least once in formula!")
        quit()
    if formula.count(' ')!=0 or formula.count('\n')!=0:
        print("ENIGMATHIZER: Creates EnigMATH protected ZIP package for large files.\nDon't use spaces or new line characters in formula!")
        quit()
    if len(sys.argv)==4:
        password = hashlib.sha256(os.urandom(256)).hexdigest()
        os.system("zip -P " + password + " -r " + zipname + ".zip \"" + foldername + "\"")
        passfile = open("password","wt")
        passfile.write(password)
        passfile.close()
        os.system("python3 " + os.path.abspath(os.path.dirname(sys.argv[0])) + "/enigmath.py password \"" + formula + "\"")
        os.system("zip -r " + zipname + ".enigmath.zip " + zipname + ".zip password.enigmath")
        os.remove("password")
        os.remove("password.enigmath")
        os.remove(zipname + ".zip")
    if len(sys.argv)==3:
        os.system("unzip " + unpackname)
        os.system("python3 " + os.path.abspath(os.path.dirname(sys.argv[0])) + "/enigmath.py password.enigmath \"" + formula + "\"")
        passfile = open("password.original","rt")
        password = passfile.read()
        passfile.close()
        os.remove("password.original")   
        os.system("unzip -P " + password + " " + unpackname[:-13] + ".zip -d ./" + unpackname[:-13])
        os.remove(unpackname[:-13] + ".zip")
        os.system("zip -r -j " + unpackname[:-13] + ".zip " + unpackname[:-13])
        shutil.rmtree(unpackname[:-13])
        os.remove("password.enigmath")
        
if __name__ == '__main__':
    main()