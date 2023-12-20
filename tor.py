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

def run():
  #Start tor
  tor_manager = TorManager('66771508', 9051)
  torified_session = tor_manager.get_tor_session()
  #Get the IP address use for checking
  print(torified_session.get("http://httpbin.org/ip").text) 
  normal_session = requests.session()
  print(normal_session.get("http://httpbin.org/ip").text)

if __name__ == "__main__":
  run()
