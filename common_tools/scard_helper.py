#****************************************************************
"""
# This file reads the text of the scard, validates the information,
# and writes it into the scard table in the database.
# Some effort should be developed to sanitize the scard to prevent
# against sql injection attacks
"""
#****************************************************************

from __future__ import print_function
import sqlite3, time
import utils, fs

class scard_class:
    def __init__(self,scard_text):
        self.name = 'scard.txt'

        #Define scard properties:
        self.project = None


        #This is likely not needed anymore
        self.farm_name = None
        
        self.configuration = None
        self.generator = None
        self.generatorOUT = None
        self.gemcEvioOUT = None
        self.gemcHipoOUT = None
        self.reconstructionOUT = None
        self.dstOUT = None
        self.jobs = None
        self.genOptions = None
        self.nevents = None

        self.scardID = None
        self.userSubmissionID = None
        self.client_ip = None

        self.coatjavaVersion = "0.0.0"
        
        self.raw_text = None
        self.fields = None
        self.torus = None
        self.solenoid = None
        self.submission = None
        self.bkmerging = None

        self.parse_scard(scard_text)

    def printer(self):
        print("Here are all the attributes of {}".format(self.name))
        #print(self.__dict__)
        for key in self.__dict__:
            print('"{}" has value "{}"'.format(key,self.__dict__[key]))



    def parse_scard(self, scard_text):
        scard_lines = scard_text.split("\n")
        for linenum, line in enumerate(scard_lines):
            if not line:
              print("Reached end of scard")
              break
            pos_delimeter_colon = line.find(":")
            key   =  line[:pos_delimeter_colon].strip()
            value =  line[pos_delimeter_colon+1:].strip()
            if key == "generator" and not 'http' in value:
              if key != fs.scard_key[linenum]:
                  pass
                  # utils.printer("ERROR: Line {0} of the steering card has the key '{1}''.".format(linenum+1,key))
                  # utils.printer("That line must have the key '{0}'.".format(fs.scard_key[linenum]))

    
            setattr(self,key,value)
        
        
        magfields = getattr(self,"fields")
        tor, sol = magfields.split("_")
        tor_val = tor[3:]
        sol_val = sol[3:]

        self.torus = tor_val
        self.solenoid = sol_val

        #set coatjava version attribute
        self.coatjavaVersion = fs.coatjavaVersion[getattr(self,"configuration")]

        print(self.coatjavaVersion)

        # Set event generator executable and output to null if the
        # generator doesn't exist in our container.  We are
        # trying to keep the client agnostic to SCard type.

        """this needs to be reworked for converting from dict to attributes
        self.data['genExecutable'] = fs.genExecutable.get(
            self.data.get('generator'), 'Null'
        )
        self.data['genOutput'] = fs.genOutput.get(
            self.data.get('generator'), 'Null'
        )
        """

    def validate_scard_line(self, linenum, line):
        if line.count("#") ==0:
            utils.printer("Warning: No comment in line {0}.".format(linenum+1))
        elif line.count("#")>1:
            utils.printer("ERROR: number of hashes>1 in line {0}".format(linenum+1))
            utils.printer("# can be used only as a delimeter and only once per line. Edit scard to fix.")
            #exit() No longer mandating hastags as a format as of 20200708
        if line.count(":") ==0:
            utils.printer("ERROR: No colon in line {0}".format(linenum+1))
            utils.printer("The data cannot be interpreted. Stopped.")
            exit()

def SCard_Entry(UserSubmissionID,timestamp,scard_dict):
    strn = """INSERT INTO Scards(UserSubmissionID,timestamp) VALUES ("{0}","{1}");""".format(UserSubmissionID,timestamp)
    utils.db_write(strn)
    for key in scard_dict:
      strn = "UPDATE Scards SET {0} = '{1}' WHERE UserSubmissionID = {2};".format(key,scard_dict[key],UserSubmissionID)
      utils.db_write(strn)
    utils.printer("SCard record added to database corresponding to UserSubmissionID {0}".format(UserSubmissionID))
