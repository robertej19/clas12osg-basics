import subprocess
import os
import readtests

def test_function(command):
	process = subprocess.Popen(command.command,
		stdout=subprocess.PIPE, 
		stderr=subprocess.PIPE)
	stdout, stderr = process.communicate()


	if command.expect_out != '0':
		if stdout == command.expect_out:
			return(stdout,stderr)
		else:
			err_mess = str(stderr) + "unexpected sdtout of: " + str(stdout)
			return(stdout, err_mess)
	else:
		return(stdout,stderr)

#Create example credentials list for MySQL access
f = open('msqlrw.txt',"w")
f.write("root\n")
f.write(" ")
f.close()

#Remove SQLite file if exists (it shouldn't, but someone might have pushed it by accident)
sqlite_filename = os.path.dirname(os.path.abspath(__file__))+'/../common_tools/CLAS12OSG.db'
if os.path.isfile(sqlite_filename):
	print('removing previous sqlite database file')
	subprocess.call(['rm',sqlite_filename])


#Create commands for Travis to run through
command_sequence = readtests.create_commands()

#Run through the commands
def run_through_tests(command_sequence):
	err_sum = 0 
	for command in command_sequence:
		out, err = test_function(command)
		print('Testing command: {0}'.format(command.name))
		if not err:
			print('... success')
		else:
			print(out)
			print('... fail, error message:')
			print(err)
			err_sum += 1
			
	return err_sum

#Give Travis an error status, such that if anything didn't work, Travis will email us
status = run_through_tests(command_sequence)
if status > 0:
	exit(1)
else:
	exit(0)

