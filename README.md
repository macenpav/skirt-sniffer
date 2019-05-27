# Skirt Sniffer
A tool for my girlfriend to mine data, detect newly added data and spam her with email. You won't believe it or not, but this skirt shop is almost like a cult of crazy women buying, trading, selling skirts. I just wanted to try how to do this kind of stuff in python, so it's an example of how to use BeautifulSoup. Everything else is pretty much ordinary like sending an email, using sqlite, etc. Running the script performs a single iteration, so the best way to mine data continuously is to write a shell script and run the python once a while.

# How to install?
Dependencies: jinja2, bs4, sqlite3, smtplib
1) Rename config-sample.ini to config.ini and fill in the details, you can use your gmail account for example
2) Write your shell script to run skirt-sniffer.py once a while (e.g. every 15 seconds) and run it in the background or you can use crontab (up to you)
