
from config.ticker_name import Ticker_name
from config.news_info import NewsAddress
from model.news_bot_base import NewsBot
import multiprocessing


meta_data = NewsAddress().METADATA


def run_bot(db_name, address, split_word):
    bot = NewsBot(db_name, address, split_word)



if __name__ == '__main__':
    # Create process objects
    
    processes = []
    
    for key, value in meta_data.items():
        db_name = value['db_name']
        address = value['주소']
        split_word = value['split']

        # Create a process for each bot
        process = multiprocessing.Process(target=run_bot, args=(db_name, address, split_word))
        processes.append(process)
        process.start()

    # Wait for all processes to complete
    for process in processes:
        process.join()
