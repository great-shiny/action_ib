import argparse

#

import apis.kis as kis
import models.ib_v_2_2 as model
import utils.sender as sender
import common.config as config

#

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-env", "--env", dest="env", action="store")  # env DEV or PROD
    parser.add_argument("-account", "--account", dest="account", action="store")  # 계좌번호
    parser.add_argument("-appkey", "--appkey", dest="appkey", action="store")  # appkey
    parser.add_argument("-appsecret", "--appsecret", dest="appsecret", action="store")  # appsecret
    parser.add_argument("-deposit", "--deposit", dest="deposit", type=int, action="store")  # 초기 원금
    parser.add_argument("-partitions", "--partitions", dest="partitions", type=int, action="store")  # 분할 수
    parser.add_argument("-threshold", "--threshold", dest="threshold", type=int, action="store")  # 매도 지점
    parser.add_argument("-ticker", "--ticker", dest="ticker", action="store")  # 종목코드(ex, SOXL, NAIL)

    return parser.parse_args()


# Defining main function
def main():
    env = get_args().env
    ticker = get_args().ticker
    account = get_args().account

    webhook_url = "https://hooks.slack.com/services/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"

    # 무매법 초기 변수 설정
    invest_values = config.set_init_invest_params(
        init_deposit=int(get_args().deposit),
        num_buy_partitions=int(get_args().partitions),
        sell_threshold_percentage=int(get_args().threshold),
    )

    # api 호출 전 초기화
    api_values = config.set_init_api_params(
        env='PROD',
        account_num=account,
        appkey=get_args().appkey,
        appsecret=get_args().appsecret,
    )

    # 무매법 진행을 위한 변수 계산
    ib_params = model.calc_daily_value(api_values, invest_values)

    info_send = {
        'is_buy': True,
        'partitions': invest_values['NUM_BUY_PARTITIONS'],
        't': ib_params['t'],
        'broker_name': '한국투자증권',
        'account_no': api_values['ACCOUNT_NUM'],
        'ticker': ticker,
        'order_type': 'LOC',
        'order_price': ib_params['loc_sell_price'],
        'order_quantity': ib_params['loc_sell_cnt'],
        'avg_price': ib_params['average_purchase_price'],
        'init_deposit': invest_values['INIT_DEPOSIT'],
        'remain_deposit': ib_params['remain_deposit'],

    }

    # 매수 주문 리스트 확인
    buy_order_list = {
        "LOC": [ib_params['loc_buy_cnt'], ib_params['loc_buy_price']],
        "TOP": [ib_params['top_buy_cnt'], ib_params['top_buy_price']],
        "AVG": [ib_params['avg_buy_cnt'], ib_params['average_purchase_price']]
    }
    print("매수 주문 리스트: ", buy_order_list)

    # 매수 주문 실행 + 슬랙 알람
    for buy_method, [qty, price] in buy_order_list.items():
        if qty > 0:
            kis.post_stock_order(
                api_values['BASE_URL'],
                api_values['TOKEN'],
                api_values['APPKEY'],
                api_values['APPSECRET'],
                api_values['ACCOUNT_NUM'],
                "AMEX",
                ticker,
                str(qty),
                str(price),
                "buy",
                config.OrderType.LOC.value
            )
            sender.send_slack_msg(
                env,
                webhook_url,
                info_send,
            )


    # 매도 주문 실행 + 슬랙 알람
    info_send['is_buy'] = False
    kis.post_stock_order(
        api_values['BASE_URL'],
        api_values['TOKEN'],
        api_values['APPKEY'],
        api_values['APPSECRET'],
        api_values['ACCOUNT_NUM'],
        "AMEX",
        ticker,
        str(ib_params['loc_sell_cnt']),
        str(ib_params['loc_sell_price']),
        "sell",
        config.OrderType.LOC.value
    )
    sender.send_slack_msg(
        env,
        webhook_url,
        info_send,
    )

    info_send['order_type'] = "지정가"
    info_send['order_quantity'] = ib_params['sell_threshold_cnt']
    info_send['order_price'] = ib_params['sell_threshold_price']

    kis.post_stock_order(
        api_values['BASE_URL'],
        api_values['TOKEN'],
        api_values['APPKEY'],
        api_values['APPSECRET'],
        api_values['ACCOUNT_NUM'],
        "AMEX",
        ticker,
        str(ib_params['sell_threshold_cnt']),
        str(ib_params['sell_threshold_price']),
        "sell",
        config.OrderType.LIMIT.value
    )
    sender.send_slack_msg(
        env,
        webhook_url,
        info_send,
    )


if __name__=="__main__":
    main()
