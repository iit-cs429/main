# Convert all lectures to pdf using nbconvert and wkhtmltopdf (this looks
# prettier than nbconvert's build-in pdf conversion.
for d in `ls -d lec*`; do \
    echo $d; \
    cd $d && s=`ls *.ipynb` && s=${s%.*} && ipython nbconvert --to html `ls *.ipynb` && wkhtmltopdf $s.html $s.pdf && cd .. ; \
done

# merge into one big pdf.
pdftk `ls -1  */*.pdf | egrep -v diagrams` cat output cs429-lectures.pdf
