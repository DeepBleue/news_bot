class NewsAddress(object):
    
    METADATA = {
        '대한경제': {
            '기자': '박연오',
            '주소': f"https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EB%B0%95%EC%97%B0%EC%98%A4&sort=1&photo=0&field=2&pd=0&ds=&de=&mynews=1&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:dd,p:all,a:all&start=1",
            'split' : 'idxno=',
            'db_name' : 'news_db/dnews.db'
            },
        '머니S': {
            '기자' : '이지운',
            '주소' : f"https://search.naver.com/search.naver?where=news&query=%EC%9D%B4%EC%A7%80%EC%9A%B4&sm=tab_opt&sort=1&photo=0&field=2&pd=0&ds=&de=&docid=&related=0&mynews=1&office_type=1&office_section_code=4&news_office_checked=1417&nso=so%3Add%2Cp%3Aall%2Ca%3Aall&is_sug_officeid=0&office_category=0&service_area=0",
            'split' : 'https://www.moneys.co.kr/article/',
            'db_name' : 'news_db/moneyS.db'
        }
            
    }