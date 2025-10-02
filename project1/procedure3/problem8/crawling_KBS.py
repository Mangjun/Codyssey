from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

class NaverCrawler:
    def __init__(self):
        self.driver = None
        self.before_login_content = []
        self.after_login_content = []

    def setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.execute_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')
        
    def navigate_to_naver(self):
        print('Navigating to Naver main page.')
        self.driver.get('https://www.naver.com')
        time.sleep(3)
        
    def crawl_before_login(self):
        print('Crawling content before login...')
        try:
            services = self.driver.find_elements(By.CSS_SELECTOR, '.shortcut_list .service_name')
            for service in services:
                text = service.text.strip()
                if text:
                    self.before_login_content.append(f'Service: {text}')

            top_buttons = [
                ('#topAsideButton', 'More'),
                ('#topTalkArea .btn_talk', 'Talk'),
                ('#topNotiArea .btn_notify', 'Notifications'),
                ('#topShoppingArea .link_shopping', 'Shopping Cart')
            ]
            
            for selector, name in top_buttons:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    self.before_login_content.append(f'Top Menu: {name}')
                except:
                    continue
                    
        except Exception as e:
            print(f'Error while crawling before login: {e}')
    
        
    def navigate_to_login_page(self):
        print('Navigating to the login page.')
        self.driver.get('https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/')
        time.sleep(3)
        
    def wait_for_manual_login(self):
        print('\nPlease log in manually in the browser.')
        input('Press Enter after you have completed the login...')
        return True
    
    
    
    def crawl_after_login(self):
        try:
            print('Starting to crawl content after login...')
            self.driver.get('https://www.naver.com')
            time.sleep(5)
            
            print('Searching for content in logged-in state...')

            services = self.driver.find_elements(By.CSS_SELECTOR, '.shortcut_list .service_name')
            for service in services:
                text = service.text.strip()
                if text:
                    self.after_login_content.append(f'Service: {text}')
            
            try:
                user_name = self.driver.find_element(By.CSS_SELECTOR, '.MyView-module__nickname___fcxwI')
                if user_name:
                    self.after_login_content.append(f'User: {user_name.text.strip()}')
            except:
                pass
            
            try:
                my_services = self.driver.find_elements(By.CSS_SELECTOR, '.MyView-module__menu_list___UzzwA .MyView-module__item_text___VTQQM')
                for service in my_services:
                    text = service.text.strip()
                    if text:
                        try:
                            parent = service.find_element(By.XPATH, '..')
                            count_elem = parent.find_element(By.CSS_SELECTOR, '.MyView-module__item_num___eHxDY')
                            count = count_elem.text.strip()
                            if count:
                                self.after_login_content.append(f'MY Service: {text} ({count})')
                            else:
                                self.after_login_content.append(f'MY Service: {text}')
                        except:
                            self.after_login_content.append(f'MY Service: {text}')
            except:
                pass

            try:
                alarm_count = self.driver.find_element(By.CSS_SELECTOR, '.alarm_count')
                if alarm_count:
                    count = alarm_count.text.strip()
                    self.after_login_content.append(f'Top Menu: Notifications ({count})')
            except:
                pass
            
            top_buttons = [
                ('#topAsideButton', 'More'),
                ('#topTalkArea .btn_talk', 'Talk'),
                ('#topNotiArea .btn_notify', 'Notifications'),
                ('#topShoppingArea .link_shopping', 'Shopping Cart')
            ]
            
            for selector, name in top_buttons:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if 'alarm_count' not in selector:  # Notification count is handled separately above
                        self.after_login_content.append(f'Top Menu: {name}')
                except:
                    continue
                        
        except Exception as e:
            print(f'Error occurred while crawling after login: {e}')
    
    def print_comparison(self):
        print('=== Content Before Login ===')
        if self.before_login_content:
            services = [c for c in self.before_login_content if c.startswith('Service:')]
            menus = [c for c in self.before_login_content if c.startswith('Top Menu:')]
            
            for i, content in enumerate(services + menus, 1):
                print(f'{i}. {content}')
        else:
            print('Could not find content before login.')
        
        print('\n=== Content After Login ===')
        if self.after_login_content:
            services = [c for c in self.after_login_content if c.startswith('Service:')]
            users = [c for c in self.after_login_content if c.startswith('User:')]
            my_services = [c for c in self.after_login_content if c.startswith('MY Service:')]
            menus = [c for c in self.after_login_content if c.startswith('Top Menu:')]
            
            for i, content in enumerate(services + users + my_services + menus, 1):
                print(f'{i}. {content}')
        else:
            print('Could not find content after login.')
            
        print('\n=== Differences Before/After Login ===')
        login_only_content = []
        
        before_set = set(self.before_login_content)
        for content in self.after_login_content:
            if content not in before_set:
                login_only_content.append(content)
        
        if login_only_content:
            users = [c for c in login_only_content if c.startswith('User:')]
            my_services = [c for c in login_only_content if c.startswith('MY Service:')]
            others = [c for c in login_only_content if not c.startswith('User:') and not c.startswith('MY Service:')]
            
            for i, content in enumerate(users + my_services + others, 1):
                print(f'{i}. {content}')
        else:
            print('Could not find any differences before and after login.')
    
    def close_driver(self):
        if self.driver:
            self.driver.quit()


def main():
    crawler = NaverCrawler()
    
    try:
        print('Starting Naver crawl...')
        crawler.setup_driver()

        print('Crawling content before login')
        crawler.navigate_to_naver()
        crawler.crawl_before_login()

        crawler.navigate_to_login_page()
        crawler.wait_for_manual_login()

        print('\nCrawling content after login')
        crawler.crawl_after_login()

        crawler.print_comparison()
        
    except Exception as e:
        print(f'An error occurred during program execution: {e}')
    
    finally:
        crawler.close_driver()

if __name__ == '__main__':
    main()