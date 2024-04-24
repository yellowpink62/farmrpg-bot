import requests
import random
from tkinter import *
from multiprocessing import Pool

def login(user, password):
  url = "https://farmrpg.com/worker.php?go=login"

  payload = f"username={user}&password={password}"
  headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Accept': '*/*',
    'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://farmrpg.com',
    'Connection': 'keep-alive',
    'Referer': 'https://farmrpg.com/index.php',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'TE': 'trailers'
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  cookies = response.headers['set-cookie']
  if response.text == 'success':
    farmrpg_token = cookies.split("farmrpg_token=")[1].split(';')[0]
    high_wind = cookies.split("HighwindFRPG=")[1].split(';')[0]

    return farmrpg_token, high_wind, response.text

  return None, None, response.text



headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Accept': '*/*',
    'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://farmrpg.com',
    'Connection': 'keep-alive',
    'Referer': 'https://farmrpg.com/',
    'Cookie': '',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Content-Length': '0',
    'TE': 'trailers'
}

def make_headers(farmrpg_token, high_wind):
  headers['Cookie'] = f'farmrpg_token={farmrpg_token}; HighwindFRPG={high_wind};'



def get_worms(response):
    return int(response.split("Worms: <strong>")[1].split("</strong>")[0])

def get_explores(response):
    return int(
        (response.split('<div id="explorestam">')[1].split("</div>")[0]).replace(",", "")
    )

def get_silver_and_gold(response):
    silver = (
        (response.split('<span><img src=\'/img/items/silver_17.png?1\' alt="Silver" style=\'width:17px;vertical-align:middle\'> ')[1].split("</span>")[0])
    )

    gold = (
        (response.split('<span><img src=\'/img/items/gold_17.png?1\' alt="Gold" style=\'width:17px;vertical-align:middle\'> ')[1].split("</span>")[0])
    )

    silver = silver.replace("&nbsp;", "").strip()
    gold = gold.replace("&nbsp;", "").strip()

    return silver, gold

def getstats():
    url = "https://farmrpg.com/worker.php?go=getstats"
    payload = {}
    response = requests.request("GET", url, headers=headers, data=payload)

    return get_silver_and_gold(response.text)





def fishcaught(_):
    # get random number
    r = random.randint(10000, 99999)
    r2 = random.randint(400, 600)

    url = f"https://farmrpg.com/worker.php?go=fishcaught&id=8&r={r}&bamt=1&p=1053&q={r2}"
    payload = {}
    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code != 200:
        print("Error")


def chargebait():
    url = "https://farmrpg.com/worker.php?go=chargebait"
    payload = {}
    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code != 200:
        print("Error")



def buy_worms(quantity):
    url = f"https://farmrpg.com/worker.php?go=buyitem&id=18&qty={quantity}"
    payload = {}
    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code != 200:
        print("Error")



def sellalluserfish():
    url = "https://farmrpg.com/worker.php?go=sellalluserfish"
    payload = {}
    response = requests.request("POST", url, headers=headers, data=payload)




def baitarea(_):
    url = "https://farmrpg.com/worker.php?go=baitarea&id=5"
    payload = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.text



def get_streak():
    url = "https://farmrpg.com/fishing.php?id=8"
    payload = {}
    response = requests.request("GET", url, headers=headers, data=payload)

    return response.text.split("Streak: <strong>")[1].split("</strong>")[0]

def reset_streak():
    while int(get_streak()) > 0:
        chargebait()


def explore(_):
    url = "https://farmrpg.com/worker.php?go=explore&id=6"
    payload = {}
    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code != 200:
        print("Error")

    return response.text


def log(text):
    log_textarea.insert(END, text)
    log_textarea.update()

def _login():
    username = username_entry.get()
    password = password_entry.get()
    
    farmrpg_token, high_wind, response = login(username, password)

    if farmrpg_token is None:
        result_label.config(text=response)
        return
    
    make_headers(farmrpg_token, high_wind)
    result_label.config(text=response)
    login_button.config(state=DISABLED)

def _start_fishing():
    log_textarea.delete(1.0, END)
    log_textarea.update()

    log("Startin Fishing...\n")
    interval = fishing_loop_interval_entry.get()
    if interval == '':
        interval = 1

    for i in range(int(interval)):
        log_textarea.delete(1.0, END)
        log_textarea.update()

        log(f"\nLoop #{i+1} of {interval}\n")

        response = baitarea(1)
        worms = get_worms(response)

        log(f"{worms} worms\n")

        if worms <= 0:
            buy_worms(200)
            worms = 200
            log_textarea.insert(END, "Bought 200 worms\n")
            log_textarea.update()

        log("Fishing...\n")
        while worms > 0:
            with Pool(5) as p:
                p.map(fishcaught, range(worms))
            
            response = baitarea(1)
            worms = get_worms(response)
            log(f"{worms} worms restants\n")
        
        log("Reseting streak...\n")

        reset_streak()
        
        log("Selling fishes...\n")
        sellalluserfish()

    log_textarea.delete(1.0, END)
    log_textarea.update()
    log("\nFINISHED\n")

def _start_explore():
    log_textarea.delete(1.0, END)
    log_textarea.update()

    while True:
        response = explore(1)
        explores = get_explores(response)
        
        log(f"{explores} stamina restants\n")

        if explores <= 0:
            log("No stamina restants\n")
            break

        with Pool(5) as p:
            p.map(explore, range(explores))


root = Tk()
root.geometry('400x600')
root.title("FarmRPG Bot")
root.columnconfigure(0, weight=110)

username_label = Label(root, text="Username")
username_label.grid(row=0, column=0, sticky='w', padx=(0, 0))

username_entry = Entry(root)
username_entry.grid(row=0, column=0, sticky='w', padx=(90, 0))

password_label = Label(root, text="Password")
password_label.grid(row=1, column=0, sticky='w', padx=(0, 0))

password_entry = Entry(root, show="*")
password_entry.grid(row=1, column=0, sticky='w', padx=(90, 0))

login_button = Button(root, text="Login", command=_login)
login_button.grid(row=2, column=0, sticky='w')

result_label = Label(root, text="")
result_label.grid(row=2, column=0, sticky='w', padx=(90, 0))

# row gap
Label(root, text="").grid(row=3, column=0)


fishing_loop_interval_label = Label(root, text="Loops")
fishing_loop_interval_label.grid(row=5, column=0, sticky='w')

fishing_loop_interval_entry = Entry(root, width=5)
fishing_loop_interval_entry.grid(row=5, column=0, sticky='w', padx=(45, 0))

fishing_button = Button(root, text="Fishing", command=_start_fishing)
fishing_button.grid(row=5, column=0, sticky='w', padx=(100, 0))

fishing_button = Button(root, text="Explore", command=_start_explore)
fishing_button.grid(row=5, column=0, sticky='w', padx=(230, 0))

log_textarea = Text(root, height=22, width=48)
log_textarea.grid(row=6, column=0, columnspan=3, sticky='w')


root.mainloop()

