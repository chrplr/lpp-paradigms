#! /bin/bash

tempfile=`(tempfile) 2>/dev/null` || tempfile=/tmp/test$$
trap "rm -f $tempfile" 0 $SIG_NONE $SIG_HUP $SIG_INT $SIG_QUIT $SIG_TERM

resp=0

subject_id=$(dialog --inputbox "Enter Subject ID:" 8 40 3>&1 1>&2 2>&3 3>&-)

until [ "$resp" = "Quit" ]
do
    next=$(($resp + 1))
    if [ $next = "10" ]; then
        next="Quit";
    fi

    dialog --clear --title "Le Petit Prince" "$@" \
         --nocancel --default-item  "$next" \
         --menu "Please select the run number and press Enter\n" \
             24 40 11 \
             1 "Chapters 1-3" \
             2 "Chapters 4-6" \
             3 "Chapters 7-9" \
             4 "Chapters 10-12" \
             5 "Chapters 13-14" \
             6 "Chapters 15-17" \
             7 "Chapters 18-21" \
             8 "Chapters 22-24" \
             9 "Chapters 25-28" \
             Quit  "End the experiment"  2>$tempfile

  retvat=$?
  resp=$(cat $tempfile)

  case $resp in
      1) python lpp-meg-distraction.py --subject $subject_id --run 1; python lpp-meg-distraction.py --subject $subject_id --run 2; python lpp-meg-distraction.py --subject $subject_id --run 3;
         python ask_lpp_question.py $subject_id 2 ;;
      2) python lpp-meg-distraction.py --subject $subject_id --run 4; python lpp-meg-distraction.py --subject $subject_id --run 5; python lpp-meg-distraction.py --subject $subject_id --run 6 ;
         python ask_lpp_question.py $subject_id 5 ;;
      3) python lpp-meg-distraction.py --subject $subject_id --run 7; python lpp-meg-distraction.py --subject $subject_id --run 8; python lpp-meg-distraction.py --subject $subject_id --run 9 ;
         python ask_lpp_question.py $subject_id 8 ;;
      4) python lpp-meg-distraction.py --subject $subject_id --run 10; python lpp-meg-distraction.py --subject $subject_id --run 11; python lpp-meg-distraction.py --subject $subject_id --run 12 ;
         python ask_lpp_question.py $subject_id 11 ;;
      5) python lpp-meg-distraction.py --subject $subject_id --run 13; python lpp-meg-distraction.py --subject $subject_id --run 14 ;
         python ask_lpp_question.py $subject_id 13 ;;
      6) python lpp-meg-distraction.py --subject $subject_id --run 15; python lpp-meg-distraction.py --subject $subject_id --run 16; python lpp-meg-distraction.py --subject $subject_id --run 17 ;
         python ask_lpp_question.py $subject_id 16 ;;
      7) python lpp-meg-distraction.py --subject $subject_id --run 18; python lpp-meg-distraction.py --subject $subject_id --run 19; python lpp-meg-distraction.py --subject $subject_id --run 20; python lpp-meg-distraction.py --subject $subject_id --run 21;
         python ask_lpp_question.py $subject_id 19 ;;
      8) python lpp-meg-distraction.py --subject $subject_id --run 22; python lpp-meg-distraction.py --subject $subject_id --run 23; python lpp-meg-distraction.py --subject $subject_id --run 24 ;
         python ask_lpp_question.py $subject_id 24 ;;
      9) python lpp-meg-distraction.py --subject $subject_id --run 25; python lpp-meg-distraction.py --subject $subject_id --run 26; python lpp-meg-distraction.py --subject $subject_id --run 27; python lpp-meg-distraction.py --subject $subject_id --run 28 ;;
      Quit) echo "Finito!" ;;
      *) dialog --msgbox "I do not understand..." 6 32 ;;
  esac

done