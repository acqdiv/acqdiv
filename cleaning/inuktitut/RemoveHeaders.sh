#!/bin/bash

# Author: Danica Pajovic <danica.pajovic@uzh.ch>

# bash script that searches for files which belong to one session, removes headers and @End of them and concatenates them to one big file.
# see code below for more info! (this can be improved!)


# Important: Always manually check the XXXAll.NAC files for left-over headers, plus: some of them contain ugly "^M" characters
# |
# +--> I didn't know how to remove the \r with sed (or the like), so:
# +--> remove in vim (or vi) with :%s/\r//g

# ----------------------------------------------------------------------------------------------------------------------- #
# >>> Note: the filenames and lines to be deleted need to be adjusted in the code according to the files listed below. <<<
# ----------------------------------------------------------------------------------------------------------------------- #


# the following files need to be concatenated to  > XXX.NAC

#JUP21[A-M]TF.NAC (21 first lines to be deleted) > JUP21All.NAC
#JUP22[A-L]TF.NAC (29 first lines to be deleted) > JUP22All.NAC
#JUP31[A-P]TF.NAC (26 first lines to be deleted) > JUP31All.NAC
#JUP43[A-W]TF.NAC (23 first lines to be deleted) > JUP43All.NAC
#JUP62[A-Y]TF.NAC (33 first lines to be deleted) > JUP62All.NAC
#JUP71[A-X]TF.NAC (25 first lines to be deleted) > JUP71All.NAC
#MAE22[A-H]TF.NAC (20 first lines to be deleted) > MAE22All.NAC
#MAE23[A-H]TF.NAC (20 first lines to be deleted) > MAE23All.NAC
#MAE28[A-E]TF.NAC (20 first lines to be deleted) > MAE28All.NAC
#MAE31[A-I]TF.NAC (23 first lines to be deleted) > MAE31ALL.NAC
#MAE33[A-W]TF.NAC (25 first lines to be deleted) > MAE33All.NAC
#MAE41[A-W]TF.NAC (26 first lines to be deleted) > MAE41All.NAC
#MAE44[A-F]TF.NAC (25 first lines to be deleted) > MAE44All.NAC
#MAE81[A-N]TF.NAC (25 first lines to be deleted) > MAE81All.NAC
#MAE83[A-J]TF.NAC (25 first lines to be deleted) > MAE83All.NAC
#SUP61[A-N]TF.NAC (20 first lines to be deleted) > SUP61All.NAC
#SUP72[A-N]TF.NAC (25 first lines to be deleted) > SUP72All.NAC
#SUP83[A-N]TF.NAC (25 first lines to be deleted) > SUP83All.NAC
#SUP84[A-T]TF.NAC (25 first lines to be deleted) > SUP84All.NAC



# delete headers and @End in second to last file from one session, then concatenate those files to one "body file"
find . -type f -exec basename {} \; | grep 'JUP21[B-Z]TF.NAC'|  while read file
do
    gsed '1,20d;s/@End//g' $file
    
done > 'JUP21Body.NAC'

# remove @End from the first file, save it as "headers file"
gsed 's/@End//g' 'JUP21ATF.NAC' > 'JUP21Headers.NAC'

# concatenate "headers" and "body file" to "all file", put @End at the end of the "all file"
cat 'JUP21Headers.NAC' 'JUP21Body.NAC' > 'JUP21All.NAC'
gsed -i '$a @End' 'JUP21All.NAC'

# delete the files that constituted one session as well as the "headers" and "body" file (so that only the "all file" will be left.
find . -type f -exec basename {} \; | egrep 'JUP21[A-Z]TF.NAC|JUP21Headers.NAC|JUP21Body.NAC'|  while read file
do
    rm $file
    
done
