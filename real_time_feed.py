import datetime

class Feed:
    OPENING_TIME = datetime.datetime.strptime('09:30:00', '%H:%M:%S').time()
    CLOSING_TIME = datetime.datetime.strptime('16:30:00', '%H:%M:%S').time()
    feed = dict()
    
    def add_column_data(self, column_name, data, row_name):
        if column_name in self.feed[row_name]:
            self.feed[row_name][column_name].append(data)
        else:
            self.feed[row_name][column_name] = [data]
    
    def update_ticker_meta_fields(self, date, time, symbol, price):
        if symbol not in self.feed[date]['ticker_metadata']:
            self.feed[date]['ticker_metadata'][symbol] = {
                'time': time,
                'max_price': price,
                'min_price': price
            }
        else:
            current_ticker_metadata = self.feed[date]['ticker_metadata'][symbol]
            self.feed[date]['ticker_metadata'][symbol] = {
                'time': time,
                'max_price': price if price > current_ticker_metadata['max_price'] else current_ticker_metadata['max_price'],
                'min_price': price if price < current_ticker_metadata['min_price'] else current_ticker_metadata['min_price']
            }

    def add_quote(self, quote):
        row_name = quote[0]
        if row_name not in self.feed:
            self.feed[row_name] = {
                'ticker_metadata': {} 
            }
        self.add_column_data('times', quote[1], row_name)
        self.add_column_data('tickers', quote[2], row_name)
        self.add_column_data('price', quote[3], row_name)
        self.update_ticker_meta_fields(row_name, quote[1], quote[2], float(quote[3]))
    
    def get_last_quote_time(self, date):
        return self.feed[date]['times'][-1]
    
    def get_quotes_count(self, date):
        return len(self.feed[date]['times'])
    
    def get_most_common_element_from_array(self, array):
        counter = 0
        element = array[0]
        for i in array:
            curr_frequency = array.count(i)
            if(curr_frequency> counter):
                counter = curr_frequency
                element = i
        return element

    def get_most_active_hour(self, date):
        times = self.feed[date]['times']
        hours = list(map(lambda time:time.split(':')[0], times))
        return self.get_most_common_element_from_array(hours)
    
    def get_most_active_ticker(self, date):
        return self.get_most_common_element_from_array(self.feed[date]['tickers'])

    def is_valid_time(self, quote_time):
        return self.OPENING_TIME <= quote_time <= self.CLOSING_TIME

    def get_time(self, time_string):
        return datetime.datetime.strptime(time_string, '%H:%M:%S').time()
    
    def get_symbols_info(self, date):
        sorted_symbols = dict(sorted(self.feed[date]['ticker_metadata'].items(), key=lambda x: x[0].lower()))
        tickers_data = []
        for symbol, symbol_meta in sorted_symbols.items():
            tickers_data.append('{} {},{},{:.2f},{:.2f}'.format(date, symbol_meta['time'], symbol, symbol_meta['max_price'], symbol_meta['min_price']))
        return '\n'.join(tickers_data)

    def __init__(self, input_data):
        quotes_data = input_data[1:]
        for quote_data in quotes_data:
            quote = quote_data.split(',')
            quote_time = self.get_time(quote[1])
            if self.is_valid_time(quote_time):
                self.add_quote(quote)

def get_input():
    return '''
    8
    2017-01-03,13:18:50,AAPL,142.64
    2017-01-03,13:19:50,AAPL,142.64
    2017-01-03,13:25:22,AMD,13.86
    2017-01-03,13:25:25,AAPL,141.64
    2017-01-03,16:25:25,AAPL,141.64
    2017-01-03,16:25:28,AMZN,845.61
    2017-01-03,16:28:50,AAPL,140.64
    2017-01-03,16:29:59,FB,140.34
    2017-01-04,16:29:32,AAPL,143.64
    2017-01-04,16:30:50,AAPL,141.64
    '''.strip()

def real_time_feed():
    input_data = get_input().split('\n')
    input_data = list(map(lambda x:x.strip(), input_data))
    feed = Feed(input_data)
    for date in feed.feed:
        print('Trading Day = {}'.format(date))
        print('Last Quote Time = {}'.format(feed.get_last_quote_time(date)))
        print('Number of valid quotes = {}'.format(feed.get_quotes_count(date)))
        print('Most active hour = {}'.format(feed.get_most_active_hour(date)))
        print('Most active symbol = {}'.format(feed.get_most_active_ticker(date)))
        print(feed.get_symbols_info(date))
if __name__ == '__main__':
    real_time_feed()
# make sure python is installed..
# just run the file using python3 real_time_feed.py to see the output