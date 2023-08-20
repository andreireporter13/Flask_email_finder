#
#
#
#
# New APP with Flask -> Portofolio edition
# -------------------
# Author: Andrei Cojocaru
# LinkedIn: https://www.linkedin.com/in/andrei-cojocaru-985932204/
# Youtube: https://www.youtube.com/channel/UCgx_Y9OHi5KPVzLJo9setxw
# ------------------
#
# Email Finder from Sites: v. 0.1.0
#
from flask import Flask, render_template, request
import requests     # for check if domain return status_code 200
from bs4 import BeautifulSoup
#
from time import sleep
#
# Main modules
from email_regex_extract import FindEmailRegex
#

# start APP here
app = Flask(__name__)

# set a secret KEY here
# --->

# Default Headers
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5',
    'Refer': 'https://google.com',
    'DNT': '1'
}


def check_site_name(site_name: str) -> str:
    '''
    This function return valid https://domainname.ro
    '''
    entire_domain = ''
    if '.' in site_name and 'https://' in site_name:
        entire_domain = site_name
    elif 'https://' not in site_name:
        entire_domain = f'https://{site_name}'

    return entire_domain


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home_page():

    # check if exist post method
    if request.method == 'POST':
        site_name = request.form['site_name'].strip().lower()

        session = requests.Session()
        checker_domain = check_site_name(site_name)

        if checker_domain:
            try:
                resp = session.get(url=checker_domain, headers=DEFAULT_HEADERS)
                # next ---> logic of scraping data
                response_for_bs4 = session.get(url=checker_domain, headers=DEFAULT_HEADERS)
                soup_links = [link['href'] for link in BeautifulSoup(response_for_bs4.text, 'lxml').find_all('a') if 'href' in link.attrs]

                # parse emails from this domains

                # list for emails
                lst_with_emails = []

                # try to add data from first page.
                lst_with_emails.extend(FindEmailRegex(str(resp)).extract_email())
                for soup_link in soup_links:

                    soup_link = soup_link.strip()
                    # check if domain name exist in soup_link
                    if site_name not in soup_links:
                        soup_link = site_name + soup_link

                    try:
                        req_soup_link = session.get(url=soup_link, headers=DEFAULT_HEADERS).text
                        sleep(0.2)
                    except:
                        req_soup_link = ''

                    # add emails to list
                    lst_with_emails.extend(FindEmailRegex(str(req_soup_link)).extract_email())


                return render_template('response.html', emails=list(set(lst_with_emails)))

            # else something wrong
            except:
                 return render_template('response.html', emails=[f'0x0 -> invalid data {checker_domain}'])

    return render_template('home.html')


@app.route('/contact')
def contact_page():
    return render_template('contact.html')


if __name__ == "__main__":
    app.run(debug=True)
