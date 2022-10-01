from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver
from time import sleep
import warnings
import requests
from bs4 import BeautifulSoup
import pandas as pd
warnings.filterwarnings("ignore")


class LinkedIn:
    def __init__(self, search_list, count_per_job=-1, location='Worldwide'):
        self._search_list = search_list
        self._count_per_job = count_per_job
        self._location = location
        self._df = pd.DataFrame()
        self._logs = ""

    @property
    def search_list(self):
        return self._search_list

    @search_list.setter
    def search_list(self, value):
        assert type(value) == list
        self._search_list = value

    @property
    def count_per_job(self):
        return self._count_per_job

    @count_per_job.setter
    def count_per_job(self, value):
        assert type(value) == float or type(value) == int
        self._count_per_job = value

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        assert type(value) == str and len(value) > 0
        self._location = value

    def open_driver(self, page_url, sleep_time=1):
        firefoxOptions = Options()
        firefoxOptions.add_argument("--headless")
        service = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(
            options=firefoxOptions,
            service=service,
        )

        while True:
            try:
                driver.get(page_url)
                sleep(sleep_time)
                driver.find_element_by_class_name('join-form')
            except:
                break

        return driver

    def scroll_page(self, driver, sleep_time=1):
        same_height = 0
        # Get scroll height
        last_height = driver.execute_script(
            "return document.body.scrollHeight")
        page_top = 1
        no_jobs = len(driver.find_elements(
            By.CLASS_NAME, 'base-card__full-link'))

        while no_jobs < self._count_per_job:
            # Wait to load page
            sleep(sleep_time)

            # Scroll down to bottom
            for i in range(page_top, last_height, 5):
                driver.execute_script("window.scrollTo(0, {});".format(i))
            try:
                l = driver.find_element(
                    By.XPATH, '//*[@id="main-content"]/section[2]/button')
                driver.execute_script("arguments[0].click();", l)
            except:
                pass

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height:
                same_height += 1
            else:
                same_height = 0

            # Stop If the height is the same for 5 iterations in row
            if same_height == 10:
                break

            no_jobs = len(driver.find_elements(
                By.CLASS_NAME, 'base-card__full-link'))

            page_top = last_height
            last_height = new_height

    def get_jobs_links(self, page_url):
        driver = self.open_driver(page_url)
        self.scroll_page(driver)
        links = []
        soup = BeautifulSoup(driver.page_source)
        driver.quit()
        links_ls = soup.findAll(
            'a', attrs={'data-tracking-control-name': 'public_jobs_jserp-result_search-card'})

        for link in links_ls:
            current_link = link['href']
            final_link = 'https://www.linkedin.com/' + \
                current_link[current_link.find('jobs'):]
            links.append(final_link)
        return links

    def get_job_details(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
        data = requests.get(url, headers=headers).text
        soup = BeautifulSoup(data)
        job_title = soup.find('h1').text
        if job_title.find('(') != -1:
            job_title = job_title[:job_title.find('(')]
        org_name = soup.find('a', attrs={
                             "data-tracking-control-name": "public_jobs_topcard-org-name"}).text.strip()
        job_loc = soup.find('span', attrs={
                            "class": "topcard__flavor topcard__flavor--bullet"}).text.strip().split(',')
        if len(job_loc[-1].strip()) == 2:
            job_country = 'United States'
            job_loc = ', '.join(job_loc)
        else:
            job_country = job_loc[-1]
            job_loc = ', '.join(job_loc[:-1])
        job_desc = soup.find(
            'div', attrs={'class': "show-more-less-html__markup"}).get_text('\n').strip()
        post_time = soup.find(
            'span', attrs={'class': "posted-time-ago__text"}).text.strip()
        logo = soup.find('img', attrs={
                         'data-ghost-classes': 'artdeco-entity-image--ghost'})['data-delayed-url']

        info_label = soup.find(
            'ul', attrs={'class': 'description__job-criteria-list'}).findAll('h3')
        info_value = soup.find(
            'ul', attrs={'class': 'description__job-criteria-list'}).findAll('span')
        info_dict = {}
        for idx in range(len(info_label)):
            label = ' '.join(info_label[idx].text.split())
            value = ' '.join(info_value[idx].text.split())
            info_dict[label] = value

        details = {
            "Job Title": job_title,
            "Company Name": org_name,
            "Country": job_country,
            "City/State": job_loc,
            "Job Description": job_desc,
            "Post Time": post_time,
            "Company Logo": logo}
        details.update(info_dict)
        details['Job Link'] = url
        return details

    def get_job_details_fast(self, page_url):
        driver = self.open_driver(page_url)
        self.scroll_page(driver)
        soup = BeautifulSoup(driver.page_source)
        driver.quit()
        details = {
            "Job Title": [],
            "Company Name": [],
            "Country": [],
            "City/State": [],
            "Post Time": [],
            "Company Logo": [],
            "Job Link": [],
        }

        jobs = soup.findAll('div', attrs={'class': 'base-search-card__info'})
        logos = soup.findAll('div', attrs={'class': 'search-entity-media'})
        links = soup.findAll(
            'a', attrs={'data-tracking-control-name': 'public_jobs_jserp-result_search-card'})
        for job in jobs[:self.count_per_job]:
            job_title = job.find('h3').text.strip()
            org_name = job.find(
                'h4', attrs={'class': 'base-search-card__subtitle'}).text.strip()
            job_loc = job.find(
                'span', attrs={'class': 'job-search-card__location'}).text.strip().split(',')
            if len(job_loc[-1].strip()) == 2:
                job_country = 'United States'
                job_loc = ', '.join(job_loc)
            else:
                job_country = job_loc[-1]
                job_loc = ', '.join(job_loc[:-1])
            post_time = job.find('time')['datetime']

            if job_title.find('(') != -1:
                job_title = job_title[:job_title.find('(')]
            details['Job Title'].append(job_title)
            details['Company Name'].append(org_name)
            details['Country'].append(job_country)
            details['City/State'].append(job_loc)
            details['Post Time'].append(post_time)

        for logo in logos[:self.count_per_job]:
            job_logo = logo.find(
                'img', attrs={'data-ghost-classes': 'artdeco-entity-image--ghost'})
            try:
                job_logo = job_logo['src']
            except:
                job_logo = job_logo['data-delayed-url']

            details['Company Logo'].append(job_logo)

        for link in links[:self.count_per_job]:
            details['Job Link'].append(link['href'])

        return details

    def run(self, sleep_time=0.5, method='fast'):
        for job in self._search_list:
            # concatnating the job with the search link and updating the spaces by '%20'
            self._logs += 'Current searching job: ' + job + '\n'
            yield self._logs
            current_job = job.replace(' ', '%20')
            # Job search link
            url = f'https://www.linkedin.com/jobs/search/?location={self._location}&keywords={current_job}'
            if method == 'slow':
                # getting the job's links from the page
                self._logs += 'Getting jobs URLs.... \n'
                yield self._logs
                links = self.get_jobs_links(url)
                self._logs += 'Number of links fetched: ' + \
                    str(len(links))+'\n'
                yield self._logs
                # iterating over each link and getting the details
                for link in links[:self.count_per_job]:
                    sleep(sleep_time)
                    try:
                        new_df = pd.DataFrame(
                            self.get_job_details(link), index=[0])
                        self._df = pd.concat(
                            [self._df, new_df], ignore_index=True)
                        self._logs += str(len(self._df)) + \
                            ' Jobs has fetched sucessfully\n'
                        yield self._logs
                    except Exception as e:
                        self._logs += 'job could not be fetched ' + str(e)+'\n'
                        yield self._logs
            else:
                self._logs += 'Fetching jobs... \n'
                yield self._logs
                new_df = pd.DataFrame(self.get_job_details_fast(url))
                self._df = pd.concat(
                    [self._df, new_df], ignore_index=True)
                self._logs += str(len(new_df)) + \
                    ' Jobs has fetched sucessfully\n'
                yield self._logs

        return self._df

    def create_csv(self):
        self._df.to_csv('results.xlsx', index=False, encoding='utf-8')

    def create_excel(self):
        self._df.to_excel('results.xlsx', index=False, encoding='utf-8')

    def clear_df(self):
        self._df = pd.DataFrame()
