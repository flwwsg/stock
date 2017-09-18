from selenium import webdriver
import time

hybrid_fund = '//div[@class="types"]/ul[@id="types"]/li[contains(text(),"混合")]'
top_fund_url_xpath = '//div[@class="dbtable"]/table[@id="dbtable"]/tbody/tr/td[3]/a'
top_fund_name_xpath = '//div[@class="dbtable"]/table[@id="dbtable"]/tbody/tr/td[4]/a'
top_fund_index_xpath = '//div[@class="dbtable"]/table[@id="dbtable"]/thead/tr/th'
stack_in_top_fund_xpath = '//div[@class="bd"]/ul/li[@id="position_shares"]/div/table/tbody/tr/td[1]/a'
start_url = 'http://fund.eastmoney.com/data/fundranking.html'
browser = webdriver.Chrome()

# get index page
browser.get(start_url)
hy = browser.find_element_by_xpath(hybrid_fund)
hy.click()
time.sleep(5)

top_fund_urls = browser.find_elements_by_xpath(top_fund_url_xpath)
top_fund_names = browser.find_elements_by_xpath(top_fund_name_xpath)
print(len(top_fund_urls))
stacks = []
top_fund = []
tmp = webdriver.Chrome()
i = 0
for iurl, iname in zip(top_fund_urls[:2], top_fund_names[:2]):
    try:
        index = iurl.get_attribute('href')
    except Exception:
        continue
    print(iurl.text)
    tmp.get(index)
    time.sleep(3)
    ts = tmp.find_elements_by_xpath(
stack_in_top_fund_xpath)
    stacks.append({i.text:i.get_attribute('href').split('/')[3][:-5] for i in ts})
    top_fund.append(iname.text)

tmp.quit()
browser.quit()
print(top_fund)
print(stacks)

