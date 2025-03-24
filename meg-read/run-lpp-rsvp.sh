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
             2 "Chapters 4-5" \
             3 "Chapters 6-8" \
             4 "Chapters 9-10" \
             5 "Chapters 11-13" \
             6 "Chapters 14-17" \
             7 "Chapters 18-20" \
             8 "Chapters 21-23" \
             9 "Chapters 24-27" \
             Quit  "End the experiment"  2>$tempfile

  retvat=$?
  resp=$(cat $tempfile)

  case $resp in
      1) python rsvp-meg.py --chapter 1 --text-size 60;;
      2) python rsvp-meg.py --chapter 2 --text-size 60;;
      3) python rsvp-meg.py --chapter 3 --text-size 60;;
      4) python rsvp-meg.py --chapter 4 --text-size 60;;
      5) python rsvp-meg.py --chapter 5 --text-size 60;;
      6) python rsvp-meg.py --chapter 6 --text-size 60;;
      7) python rsvp-meg.py --chapter 7 --text-size 60;;
      8) python rsvp-meg.py --chapter 8 --text-size 60;;
      9) python rsvp-meg.py --chapter 9 --text-size 60;;
      Quit) echo "Finito!" ;;
      *) dialog --msgbox "I do not understand..." 6 32 ;;
  esac

done
