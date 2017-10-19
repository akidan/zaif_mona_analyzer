#-*-coding:utf-8-*- 
import sys
import time
import requests
import bs4
print ("============================")
print("   " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

list = ['ask', 'bid']
for mona in list:
    locals()[mona+"_url"] = "https://zaif.jp/more_data/mona_jpy/" + str(mona) + "s.html"
    response = requests.get(locals()[mona+"_url"])
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    locals()[mona+"_list"] = []
    for idx, tr in enumerate(soup.find_all('tr')):
        if idx != 0:
            tds = tr.find_all('td')
            locals()[mona+"_list"].append({
                'mona_jpy'       : float(tds[0].contents[0].strip()),
                'mona_amount'    : float(tds[1].contents[0].strip()),
                'mona_amountxjpy': float(tds[2].contents[0].strip()),
                'mona_all_jpy'   : float(tds[3].contents[0].strip()),
                'mona_all_amount': float(tds[4].contents[0].strip()),
                'mona_avg_jpy'   : float(tds[5].contents[0].strip())
            })
    locals()[mona+"_row"] = len(locals()[mona+"_list"])
    print("   " + mona.capitalize() + " " + str(locals()[mona+"_list"][0]['mona_jpy']))
    
# mona_jpy        : '売値(JPY)'
# mona_amount     : '数量(MONA)'
# mona_amountxjpy : '数量(JPY)'
# mona_all_jpy    : '累計(JPY)'
# mona_all_amount : '累計(MONA)'
# mona_avg_jpy    : '単価(JPY)'

# mona_amountxjpy      == mona_jpy * mona_amount
# sum(mona_amount)     == ask_list[-1]['mona_all_amount']
# sum(mona_amountxjpy) == ask_list[-1]['mona_all_jpy']
# mona_avg_jpy[row]    == mona_all_amount[row] / mona_all_jpy[row]

ask_bid_rate=(round(ask_list[0]['mona_jpy']/bid_list[0]['mona_jpy'],4)-1)*100
bgcolor = "41m" if ask_bid_rate > 5 else "42m";
print ('\x1b[6;30;' + bgcolor + "A/B " + str(ask_bid_rate) + "%" + '\x1b[0m')
print ("============================")

ask_list_sorted = sorted(ask_list, key = lambda k:k['mona_amount'], reverse=True)
bid_list_sorted = sorted(bid_list, key = lambda k:k['mona_amount'], reverse=True)
suggest_sell = 1000.0;
suggest_buy = 0.0;
for i in range (0, 10):
    print ("Ask amount sort " + str(ask_list_sorted[i]['mona_jpy']) + " Avg " + str("{:3.1f}".format(ask_list_sorted[i]['mona_avg_jpy'])) + " " + str(int(ask_list_sorted[i]['mona_amount'])))
    if suggest_sell > ask_list_sorted[i]['mona_avg_jpy']: suggest_sell = ask_list_sorted[i]['mona_avg_jpy']
print("")
for i in range (0, 10):
    print ("Bid amount sort " + str(bid_list_sorted[i]['mona_jpy']) + " Avg " + str("{:3.1f}".format(bid_list_sorted[i]['mona_avg_jpy'])) + " " + str(int(bid_list_sorted[i]['mona_amount'])))
    if suggest_buy < bid_list_sorted[i]['mona_avg_jpy']: suggest_buy = bid_list_sorted[i]['mona_avg_jpy']
print ("============================")

color = 31; #red
amount_diff = ask_list[-1]['mona_all_amount'] - bid_list[-1]['mona_all_amount']
if (amount_diff > 0):
    adjust_color = 1;
    suggest = "Buy "
    divide = bid_list[-1]['mona_all_amount']
else:
    adjust_color = 0;
    suggest = "Sell "
    divide = ask_list[-1]['mona_all_amount']
print ("Ask amount " + str(ask_list[-1]['mona_all_amount']))
print ("Bid amount " + str(bid_list[-1]['mona_all_amount']))
print ("============================")

print ("   " + "Suggestion " + '\033[1;' + str(color+adjust_color) + ';40m ' + suggest + str(abs(round(amount_diff/divide,4)*100)) + "%" + ' \033[0m');
print ("  " + '\x1b[6;30;42mSuggest sell at\x1b[0m ' + str("{:3.1f}".format(float(suggest_sell)-0.1)))
print ("  " + '\x1b[6;30;42mSuggest buy  at\x1b[0m ' + str("{:3.1f}".format(float(suggest_buy)+0.1)))
print ("  " + '\x1b[6;30;42mSuggest stop at\x1b[0m ' + str("{:3.1f}".format(float(ask_list[0]['mona_jpy'])*1.1)))
print ("  " + '\x1b[6;30;42mSuggest rstp at ' + str("{:3.1f}".format(float(bid_list[0]['mona_jpy'])*0.9))+'\x1b[0m')
print ("  " + 'Estimate profit ' + str((round(float(suggest_sell)/float(suggest_buy),2)-1.0)*100)+"%")
print ("============================")
