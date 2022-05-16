import client
import telegram
import datetime
import os


def get_total_val(cli: client.FtxClient):
    return "totalAccountValue={}\n".format(
        cli.get_account_info()["totalAccountValue"])


def get_coin_info(cli: client.FtxClient, perp_str: str):
    perp = cli.get_future(perp_str)
    coin = "{}\nlast={}\nchange1h={}\nchange24h={}\n".format(
        perp_str, perp["last"], perp["change1h"], perp["change24h"])
    return coin


def get_exchange_info():
    cli = client.FtxClient(os.environ["API_KEY"], os.environ["API_SECRET"],
                           None)
    account = get_total_val(cli)
    res = account + '\n'
    for coin in os.environ["COIN_LIST"].split(','):
        coin_str = get_coin_info(cli, coin)
        res += coin_str + '\n'
    return res.strip()


def get_sh_time():
    sh_tz = datetime.timezone(datetime.timedelta(hours=8),
                              name="Asia/Shanghai")
    return datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).astimezone(sh_tz).strftime(
            "%Y-%m-%d %H:%M:%S") + '\n'


if __name__ == "__main__":
    bot = telegram.Bot(token=os.environ["BOT_TOKEN"])
    bot.send_message(chat_id=os.environ["CHANNEL_ID"],
                     text=get_sh_time() + '\n' + get_exchange_info())
