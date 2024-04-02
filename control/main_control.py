import mecademicpy.robot as mdr #mechademicpy API import (see Github documentation)
import time #for time.sleep()
import utility_functions as uf #import utility functions
import gcode_translator as gt #import gcode translator
from utility_functions import robot_stats
import rt_user_functions as ruf #extra functions such as 'exiting'


#initiate exit indicator
#setup exit key
ruf.check_for_exit()

#initiate robot
msb = uf.activationsequence()

#set initial positions
uf.cleanpose(msb)

#------------load file path---------------------
file_path = r"C:\Users\steph\OneDrive\_Studium\_Semester 6 (FS2024)\Bachelor Thesis\CODEBASE\BachelorThesis_SonoBone\gcode\ARSL_am.gcode"

#-----------print 2D file-----------------------
gt.write_coordinates(gt.extract_coordinates(file_path), msb)

#deactivate robot
uf.deactivationsequence(msb)
