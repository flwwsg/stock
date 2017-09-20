from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

# stop loading page 

browser.set_page_load_timeout(10)
exception TimeoutException