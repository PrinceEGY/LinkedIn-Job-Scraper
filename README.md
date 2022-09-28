# LinkedIn-Job-Scraper
Scrape public available jobs on Linkedin using simple technologies.
For each job, the following fields are extracted: 
> `Job Title`, 
> `Organization Name`, 
> `Country`, 
> `City/State`, 
> `Job Description`, 
> `Post Time`, 
> `Company Logo`, 
> `Seniority Level`, 
> `Employoment Type`, 
> `Job Function`,
> `Industries`.
> `Job Link`.
> 
## General info
- This project was created as part of Samsung Innovation Campus (SIC) training for training purposes and i'm not responsible for any misuses
- The application construct is located in the `app.py` file. This file uses the scraping methods from the `scraping_module` folder
- The methods and technologies used for scraping are so simple

![App overview](https://github.com/PrinceEGY/LinkedIn-Job-Scraper/blob/main/images/app-img.png)

## Technologies
The app is fully written in `Python 3.10.1`, the user interface was created using `streamlit 1.13.0`

The whole scraping was done using `BeautifulSoup`, `requests`, `selenium`, `selenium` was used only for scrolling the page to cover more jobs, `requests` was used to request the jobs urls and `BeautifulSoup` was used to extract information from the DOM structure returned from the `selenium` and `requests` 

## Scrapping methods
- Fast scraping: increase scraping speed significantly in exchange for scraping less information, the information that will not be fetched are (Job Description, Seniority level, Employment type, Job function and Industries)
- Slow scraping: Scrape all possible information for each job in exchange for taking more time in scraping

**The reason behind fast scraping is it doesn't have to request each job link and it directly scrape the information from the search link**
