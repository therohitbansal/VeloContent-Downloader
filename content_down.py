def download_content(content_name, quality):
    import undetected_chromedriver as uc 
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time
    from urllib.parse import urlparse
    import sys
    content_name=content_name.replace(" ", "-")
    print(f"Running automation for: {content_name} [{quality}]")


    def close_extra_tabs(driver, main_window):
        for window in driver.window_handles:
            if window != main_window:
                driver.switch_to.window(window)
                driver.close()
        driver.switch_to.window(main_window)

    def scroll_until_element(driver, by, value, max_scrolls=10):
        for _ in range(max_scrolls):
            try:
                element = driver.find_element(by, value)
                if element.is_displayed():
                    return True
            except:
                pass
            driver.execute_script("window.scrollBy(0, 250);")
            time.sleep(0.3)
        return False

    def handle_mediator(driver, mediator_url):
        mediator_host = urlparse(mediator_url).netloc
        print("Mediator domain locked to:", mediator_host)

        driver.get(mediator_url)
        time.sleep(2)

        visited_hublinks = False
        max_attempts = 5
        attempts = 0
        flag=0
        while attempts < max_attempts:
            attempts += 1
            current_url = driver.current_url.lower()
            if mediator_host not in urlparse(driver.current_url).netloc:
                print(f"🔄 Redirected outside mediator domain: {driver.current_url}, returning...")
                if quality=='HQ 1080p':
                    break
                driver.get(mediator_url)
                time.sleep(2)
                continue

            try:
                button = WebDriverWait(driver, 8).until(
                    EC.element_to_be_clickable((By.XPATH,
                        "//a[contains(text(),'Continue') or contains(text(),'Get Link') "
                        "or contains(text(),'Download') or contains(text(),'CLICK TO CONTINUE') or contains(text(),'GET LINKS')]"))
                )
                print("🟢 Mediator button found:", button.text)
                
                if(button.text=='GET LINKS'):
                    flag+=1
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                time.sleep(0.5)
                driver.execute_script("arguments[0].click();", button)
                time.sleep(3)
                if flag==2:
                    print("🔴 Mediator button clicked twice, stopping further clicks.")
                    latest_tab = driver.window_handles[-1]
                    driver.switch_to.window(latest_tab)
                    break
            except:
                print("Waiting for mediator button to appear...")
                time.sleep(2)

        print("⏹️ Max attempts reached. Stopping mediator handler.")


    # --------------------- Main Script ---------------------
    options = uc.ChromeOptions()
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-blink-features=AutomationControlled")
    prefs = {"download.prompt_for_download": False, "download.directory_upgrade": True}
    options.add_experimental_option("prefs", prefs)

    driver = uc.Chrome(options=options)
    driver.get("https://example.com/") #type website name here
    print(driver.title)

    body = driver.find_element(By.TAG_NAME, "body")
    body.click()
    close_extra_tabs(driver, driver.current_window_handle)

    search_box = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#searchForm input[name='s']"))
    )
    search_box.clear()
    search_box.send_keys(content_name)
    search_box.send_keys(Keys.RETURN)

    content_name_xpath = f"//ul[contains(@class,'recent-contents')]//a[contains(translate(@href,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), '{content_name.lower()}')]"
    if scroll_until_element(driver, By.XPATH, content_name_xpath, max_scrolls=6):
        driver.execute_script(
            "arguments[0].click();",
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, content_name_xpath)))
        )
        close_extra_tabs(driver, driver.current_window_handle)
        print(f"Opened {content_name} content page successfully!")
    else:
        raise Exception(f"Please check the content name and try again.")

    hd_xpath = f"//a[span[contains(text(),'{quality}')] or contains(text(),'{quality}')]"
    hd_elements = driver.find_elements(By.XPATH, hd_xpath)

    if not hd_elements:
        driver.close()
        raise Exception(f"Quality '{quality}' not found in the content page!")
    hd_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, hd_xpath)))
    mediator_url = hd_element.get_attribute("href")
    print("Direct mediator URL:", mediator_url)

    handle_mediator(driver, mediator_url)
    time.sleep(5)
    print("DEBUGGING")
    print("Final page URL:", driver.current_url)
    try:
        hub_xpath = "//a[.//img[contains(@src, 'Hubdrive2.png')]]"
        hd_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, hub_xpath))
        )
        hubdrive_link = hd_element.get_attribute("img")
        print("✅ HubDrive Link:", hubdrive_link)

        # Navigate to the HubDrive link
        driver.get(hubdrive_link)

        # Close any popups
        main_window = driver.current_window_handle
        for handle in driver.window_handles:
            if handle != main_window:
                driver.switch_to.window(handle)
                driver.close()
        driver.switch_to.window(main_window)
    except Exception as e:
        print("❌ Error fetching HubDrive link:", e)

    try:
        hub_xpath = "//a[contains(translate(@href, 'HUBCLOUD', 'hubcloud'), 'hubcloud')]"
        hd_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, hub_xpath))
        )
        hubcloud_link = hd_element.get_attribute("href")
        print("✅ HubCloud Link:", hubcloud_link)

        # Navigate to the HubDrive link
        driver.get(hubcloud_link)

        # Close any popups
        main_window = driver.current_window_handle
        for handle in driver.window_handles:
            if handle != main_window:
                driver.switch_to.window(handle)
                driver.close()
        driver.switch_to.window(main_window)
    except Exception as e:
        driver.close()
        print("❌ Error fetching HubDrive link:", e)

    try:
        hub_xpath = "//a[contains(translate(@href, 'viralkhabarbull', 'viralkhabarbull'), 'viralkhabarbull')]"
        hd_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, hub_xpath))
        )
        hubcloud_link = hd_element.get_attribute("href")
        print("✅ HubCloud Link:", hubcloud_link)

        # Navigate to the HubDrive link
        driver.get(hubcloud_link)

        # Close any popups
        main_window = driver.current_window_handle
        for handle in driver.window_handles:
            if handle != main_window:
                driver.switch_to.window(handle)
                driver.close()
        driver.switch_to.window(main_window)
    except Exception as e:
        driver.close()
        print("❌ Error fetching Content link:", e)

    try:
        if quality!='HQ 1080p':
            hub_xpath = "//a[contains(@href, '.mkv') and not(contains(@href, '.mkv.zip'))]"
        else:
            hub_xpath = "//a[contains(@href, '.mkv.zip')]"
        print("HubCloud XPath:", hub_xpath)
        hd_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, hub_xpath))
        )
        hubcloud_link = hd_element.get_attribute("href")
        print("✅ HubCloud Link:", hubcloud_link)

        # Navigate to the HubDrive link
        driver.get(hubcloud_link)

        # Close any popups
        main_window = driver.current_window_handle
        for handle in driver.window_handles:
            if handle != main_window:
                driver.switch_to.window(handle)
                driver.close()
        driver.switch_to.window(main_window)
        print("✅ Check download folder for content file.")
    except Exception as e:
        print("❌ Error fetching HubDrive link:", e)
        driver.close()
