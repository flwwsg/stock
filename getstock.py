from selenium import webdriver
import time
from handler import count_stocks


def get_top_fund(browser, top_fund=[], stacks=[]):
    top_fund_url_xpath = '//div[@class="dbtable"]/table[@id="dbtable"]/tbody/tr/td[3]/a'
    top_fund_name_xpath = '//div[@class="dbtable"]/table[@id="dbtable"]/tbody/tr/td[4]/a'
    stack_in_top_fund_xpath = '//div[@class="bd"]/ul/li[@id="position_shares"]/div/table/tbody/tr/td[1]/a'
    top_fund_urls = browser.find_elements_by_xpath(top_fund_url_xpath)
    top_fund_names = browser.find_elements_by_xpath(top_fund_name_xpath)
    print(len(top_fund_urls))
    tmp = webdriver.Chrome()
    i = 0
    for iurl, iname in zip(top_fund_urls, top_fund_names):
        try:
            index = iurl.get_attribute('href')
        except Exception:
            continue
        # print(iurl.text)
        tmp.get(index)
        time.sleep(3)
        ts = tmp.find_elements_by_xpath(
            stack_in_top_fund_xpath)
        stacks.append({i.get_attribute('href').split('/')
                       [3][:-5]: i.text for i in ts})
        top_fund.append(iname.text)
    tmp.quit()
    return top_fund, stacks


hybrid_fund = '//div[@class="types"]/ul[@id="types"]/li[contains(text(),"混合")]'
top_fund_month = '//div[@class="dbtable"]/table[@id="dbtable"]/thead/tr/th[@col="1yzf"]'
top_fund_index_xpath = '//div[@class="dbtable"]/table[@id="dbtable"]/thead/tr/th'
top_fund_next_page_xpath = '//div[@id="pagebar"]/label[contains(text(), "下一页")]'
start_url = 'http://fund.eastmoney.com/data/fundranking.html'
browser = webdriver.Chrome()

# get index page
browser.get(start_url)
hy = browser.find_element_by_xpath(hybrid_fund)
hy.click()
time.sleep(5)
browser.find_element_by_xpath(top_fund_month).click()
time.sleep(5)

top_fund = []
stacks = []
get_top_fund(browser, top_fund, stacks)

# next page
next_page = browser.find_element_by_xpath(
    '//div[@id="pagebar"]/label[contains(text(), "下一页")]')
browser.execute_script('arguments[0].click();', next_page)
time.sleep(3)
get_top_fund(browser, top_fund, stacks)

# print(top_fund)
# print(stacks)
reserved = count_stocks(top_fund, stacks)
# print(reserved)
# stocks_to_be_chk = input('input stocks you want to check>>\n')
# new = set(reserved) - set(stocks_to_be_chk.split())
# print(new)


browser.quit()
