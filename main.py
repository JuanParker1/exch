import client
import telegram
import datetime
import os


def get_total_val(main_client: client.FtxClient) -> str:
    totalAccountValue = float(
        main_client.get_account_info()["totalAccountValue"])
    for subaccount_name in os.environ["SUBACCOUNT_NAME_LIST"].split(','):
        cli = client.FtxClient(os.environ["API_KEY"], os.environ["API_SECRET"],
                               subaccount_name)
        totalAccountValue += float(cli.get_account_info()["totalAccountValue"])
    return "totalAccountValue={}\n".format(round(totalAccountValue, 2))


def get_change_percent(title: str, num: float) -> str:
    title_prefix = title + "="
    title_postfix = "%"
    bold_char = "*"
    if num < 0.0:
        title_prefix += bold_char
        title_postfix = bold_char + title_postfix
    return "{}{}{}".format(title_prefix, round(num * 100, 2), title_postfix)


def get_coin_info(cli: client.FtxClient, perp_str: str) -> str:
    perp = cli.get_future(perp_str)
    bold_perp_str = "*" + perp_str + "*"
    change1h_str = get_change_percent("change1h", float(perp["change1h"]))
    change24h_str = get_change_percent("change24h", float(perp["change24h"]))
    coin = "{}\nlast={}\n{}\n{}\n".format(bold_perp_str, perp["last"],
                                          change1h_str, change24h_str)
    return coin


def get_exchange_info() -> str:
    cli = client.FtxClient(os.environ["API_KEY"], os.environ["API_SECRET"],
                           None)
    account = get_total_val(cli)
    res = account + '\n'
    for coin in os.environ["COIN_LIST"].split(','):
        coin_str = get_coin_info(cli, coin)
        res += coin_str + '\n'
    return res.strip()


def get_sh_time() -> str:
    sh_tz = datetime.timezone(datetime.timedelta(hours=8),
                              name="Asia/Shanghai")
    return datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).astimezone(sh_tz).strftime(
            "%Y-%m-%d %H:%M:%S") + '\n'


if __name__ == "__main__":
    bot = telegram.Bot(token=os.environ["BOT_TOKEN"])
    bot.send_message(chat_id=os.environ["CHANNEL_ID"],
                     text=get_sh_time() + '\n' + get_exchange_info(),
                     parse_mode=telegram.ParseMode.MARKDOWN)
