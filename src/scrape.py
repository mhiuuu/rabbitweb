import requests
from stem import Signal
from stem.control import Controller
from bs4 import BeautifulSoup
from selenium import webdriver

equations = []

class TorManager:
  def __init__(self, tor_password, tor_port):
    self.tor_password = tor_password
    self.tor_port = tor_port

  def change_tor_circuit(self):
    with Controller.from_port(port=self.tor_port) as controller:
      controller.authenticate(password=self.tor_password)
      print("Success!")
      controller.signal(Signal.NEWNYM)
      print("New Tor connection processed")

  def get_tor_session(self, port=9050):
    self.change_tor_circuit()
    session = requests.session()
    session.proxies = {
      'http': f'socks5://127.0.0.1:{port}',
      'https': f'socks5://127.0.0.1:{port}'
    }
    return session

def get_html(page, asin):
  url = f"https://cunghocvui.com/phuong-trinh?chat_tham_gia=NH3&page={asin}"
  page.get(url)
  html = BeautifulSoup(page.page_source, 'html.parser')
  return html

def run_with_tor():
  # Start Tor
  tor_manager = TorManager('66771508', 9051)
  torified_session = tor_manager.get_tor_session()
  print(torified_session.get("http://httpbin.org/ip").text) 
  # Use Selenium with Tor
  chrome_options = webdriver.ChromeOptions()
  #chrome_options.add_argument('--headless')
  #chrome_options.add_argument(f"--proxy-server=socks5://127.0.0.1:9050")
  browser = webdriver.Chrome(options=chrome_options)

  for i in range(1, 10):
    html = get_html(browser, i)
    parse_html(html, i)

def parse_html(html, asin):
  elements = html.select('.chemical-equation')
  if elements:
    for element in elements:
      equations.append(element.text)
  else:
    print(f"No elements found on page {asin}")

def main():
  run_with_tor()
  print(equations)
  print(f'There are a total of {len(equations)} equations')

if __name__ == "__main__":
  main()
