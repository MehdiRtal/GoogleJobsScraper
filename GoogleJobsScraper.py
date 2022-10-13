from playwright.sync_api import sync_playwright
from multiprocessing import Process
import urllib.parse
import argparse
import re


parser = argparse.ArgumentParser()
parser.add_argument("-type", help="FULL_TIME, PART_TIME, TEMPORARY, INTERN", default="")
parser.add_argument("-degree", help="BACHELORS, MASTERS, DOCTORATE, ASSOCIATE, ENTRY_LEVEL", default="")
parser.add_argument("-location", default="")
parser.add_argument("-skills", default="")
parser.add_argument("-remote", action="store_true", default="")
parser.add_argument("-o")
args = parser.parse_args()


if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        page = browser.new_page()
        page.goto(f"https://careers.google.com/jobs/results/?degree={args.degree}&employment_type={args.type}&has_remote={args.remote}&location={urllib.parse.quote(args.location)}&skills={args.skills}")
        pages_count = int("".join(re.findall("\d", page.locator("css=[class='gc-h-flex gc-sidebar__pagination--page']").inner_text())[1:]))
        for i in range(1, pages_count):
            page.goto(f"https://careers.google.com/jobs/results/?degree={args.degree}&employment_type={args.type}&has_remote={args.remote}&page={i}&location={urllib.parse.quote(args.location)}&skills={args.skills}")
            jobs = []
            for j in range(20):
                jobs.append("https://careers.google.com" + page.locator("id=search-results").locator("css=li").locator("css=a[class='gc-card']").nth(j).get_attribute("href"))
            for job in jobs:
                page.goto(job)
                title = page.locator("css=[class='gc-card__title gc-job-detail__title gc-heading gc-heading--beta']").inner_text().strip()
                link = page.locator("css=[class='gc-button gc-button--primary gc-button--raised gc-button--icon gc-job-detail__header-cta']").get_attribute("href")
                if args.o:
                    with open(args.o, "a") as f:
                        f.write(title + "|" + link + "\n")
                else:
                    print(link)
        browser.close()
