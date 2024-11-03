from enum import Enum

#

import apis.kis as kis


TRADE_COST = 0.25  # 거래 수수료

class OrderType(Enum):
    LIMIT = "00"
    LOC = "34"

class Currency(Enum):
    USD = "02"
    KRW = "01"


# api 호출 하기 전 초기 값 세팅
def set_init_api_params(env, account_num, appkey, appsecret):

    # if dev
    if env == 'DEV':
        base_url = "https://openapivts.koreainvestment.com:29443"
        account_num = "50116567"
        appkey = "PS4PRPhdNR32NAAjtQ94H67owtpabAzIElaK"
        appsecret = "flRL1JxXhoffiDyMeu3lEPQ01dd5m0HSxzD9Z6HvmVk/EDixB8u6hqcU15dbdrWhIGYd+gX6YFFjAmzC3l7jd/tbkmJpPyqCMlk4Qlb1mliBWnNfqWk8aKaQPJRwdQolDcQiM89C+uRvMKM9m/g6e8NZtHTUDjV50S9XFD6pgM+8d4E0334="

        return {
            'BASE_URL': base_url,
            'ACCOUNT_NUM': account_num,
            'APPKEY': appkey,
            'APPSECRET': appsecret,
            'TOKEN': kis.generate_token(base_url, appkey, appsecret),
            'HASH': kis.generate_hashkey(base_url, appkey, appsecret, account_num)
        }

    elif env == 'PROD':
        base_url = "https://openapi.koreainvestment.com:9443"
        return {
            'BASE_URL': base_url,
            'ACCOUNT_NUM': account_num,
            'APPKEY': appkey,
            'APPSECRET': appsecret,
            'TOKEN': kis.generate_token(base_url, appkey, appsecret),
            'HASH': kis.generate_hashkey(base_url, appkey, appsecret, account_num)
        }

    else:
        ValueError("[ERROR] We must use DEV or PROD env.")

# 무매법 시작하기 전 초기 설정 값 세팅
def set_init_invest_params(init_deposit, num_buy_partitions, sell_threshold_percentage):

    purchase_amount = init_deposit/num_buy_partitions

    return {
        'INIT_DEPOSIT': init_deposit,                               # 원금
        'NUM_BUY_PARTITIONS': num_buy_partitions,                   # 분할
        'PURCHASE_AMOUNT': purchase_amount,                         # 1일 매수 금
        'SELL_THRESHOLD_PERCENTAGE': sell_threshold_percentage,     # 매도 지점
    }
