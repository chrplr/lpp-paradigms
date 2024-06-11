#! /usr/bin/bash
#  set parameters for the ProPixx videoprojector @ MEG Neuropsin

# export PATH=$PATH;"/usr/local/bin/vputil"

set -x
export logFile="/home/neurostim/MEG_studies/lpp-paradigms_2024_JulieB/meg-distraction/init_PROPixx.log"


echo "#######################" >> $logFile
date >> $logFile

# Set ProPixx video mode
# 0->RGB 120Hz (Default)
# 2->RGB Quad 480Hz
echo 0 | vputil -seq -quit >>$logFile

# Set ProPixx luminosity. Must be placed at the end of the script.
# 0 -> 100%
# 1 -> 50%
# 2 -> 25%
# 3 -> 12.5%
# 4 -> 6.25%
echo 3 | vputil -ppi -quit >>$logFile
set +x
