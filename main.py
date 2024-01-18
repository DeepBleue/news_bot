
from config.ticker_name import Ticker_name
from config.news_info import NewsAddress
from model.news_bot_base import NewsBot
import multiprocessing


meta_data = NewsAddress().METADATA

### 대한경제
db_name1 = meta_data['대한경제']['db_name']
address1 = meta_data['대한경제']['주소']
split_word1 = meta_data['대한경제']['split']

### 머니S
db_name2 = meta_data['머니S']['db_name']
address2 = meta_data['머니S']['주소']
split_word2 = meta_data['머니S']['split']


def run_bot(db_name, address, split_word):
    bot = NewsBot(db_name, address, split_word)



if __name__ == '__main__':
    # Create process objects
    process1 = multiprocessing.Process(target=run_bot, args=(db_name1, address1, split_word1))
    process2 = multiprocessing.Process(target=run_bot, args=(db_name2, address2, split_word2))

    # Start processes
    process1.start()
    process2.start()

    # Optionally, wait for both processes to complete
    process1.join()
    process2.join()
        
