from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def create_webrtc_disabled_driver():
    chrome_options = Options()
    
    # Method 1: Chrome arguments
    chrome_options.add_argument('--disable-webrtc')
    chrome_options.add_argument('--disable-webrtc-hw-encoding')
    chrome_options.add_argument('--disable-webrtc-hw-decoding')
    
    # Method 2: Use WebRTC IP handling policy
    chrome_options.add_argument('--webrtc-ip-handling-policy=disable_non_proxied_udp')
    
    # Method 3: Additional privacy options
    chrome_options.add_argument('--disable-features=WebRTCHideLocalIpsWithMdns')
    
    # Method 4: Add extension (optional)
    # chrome_options.add_extension('path_to_webrtc_control_extension.crx')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print(f"Error with Service object: {e}")
        try:
            # Fallback: Try without Service object
            driver = webdriver.Chrome(options=chrome_options)
        except Exception as e:
            print(f"Failed to create driver: {e}")
            return None
    
    # Method 5: JavaScript injection
    try:
        script = """
        Object.defineProperty(navigator.mediaDevices, 'getUserMedia', {
            value: () => new Promise((resolve, reject) => {
                reject(new Error('getUserMedia is disabled'));
            })
        });
        """
        driver.execute_script(script)
    except Exception as e:
        print(f"Failed to inject JavaScript: {e}")
    
    return driver

def test_webrtc_blocking():
    driver = create_webrtc_disabled_driver()
    if not driver:
        print("Failed to create WebDriver")
        return
    
    try:
        # Test multiple WebRTC testing sites
        test_urls = [
            'https://ipleak.net',
            'https://browserleaks.com/webrtc',
            'https://test.webrtc.org'
        ]
        
        for url in test_urls:
            print(f"\nTesting URL: {url}")
            driver.get(url)
            time.sleep(5)  # Give time for the page to load
            
            # Take a screenshot for verification
            driver.save_screenshot(f'webrtc_test_{url.split("//")[1].split("/")[0]}.png')
            print(f"Screenshot saved for {url}")
            
            # Optional: Wait for user verification
            user_input = input(f"Verify WebRTC is disabled on {url}. Enter 'n' for next site, 'q' to quit: ")
            if user_input.lower() == 'q':
                break
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        driver.quit()

def troubleshooting_tips():
    print("\nTroubleshooting Tips:")
    print("1. Ensure you have the latest chromedriver installed")
    print("2. Verify the chromedriver version matches your Chrome browser version")
    print("3. Try running Chrome with --no-sandbox if you're on Linux")
    print("4. Check if your Chrome browser is updated")
    print("5. Consider using a WebRTC blocking extension as a backup")
    print("\nTo check versions:")
    print("Chrome browser: chrome://version/")
    print("Chromedriver needed: https://sites.google.com/chromium.org/driver/")

if __name__ == "__main__":
    troubleshooting_tips()
    test_webrtc_blocking()