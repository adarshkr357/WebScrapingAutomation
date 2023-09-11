# Define a function to extract a substring between two words
def extract_substring(source_string, start_word, end_word):
    # Try block to handle exceptions
    try:
        # Find the index of the start word and adjust the index to the end of the start word
        start_index = source_string.index(start_word) + len(start_word)

        # Find the index of the end word, starting the search from start_index
        end_index = source_string.index(end_word, start_index)

        # Return the substring between start_index and end_index
        return source_string[start_index:end_index]

    # Exception handling for ValueError
    except ValueError:
        # If either start_word or end_word is not found in source_string, return False
        return False


# Define a class for automation and web scraping tasks
class AutomationScraper:
    # Docstring for class
    """
    A class that provides functionality for various automation and web scraping tasks.
    """

    # Define a static method to fetch cryptocurrency news
    @staticmethod
    def fetch_crypto_news():
        """
        Fetches and prints cryptocurrency news and market data from 'https://coinmarketcap.com/'.

        Returns:
        str: A string containing cryptocurrency news and market data. If an error occurs, it returns an error message.
        """
        # Import requests module for making HTTP requests
        import requests

        # Make a GET request to the website and get the response text
        response = requests.get('https://coinmarketcap.com/').text

        # Check if a specific element is in the response text
        if '<span class="icon-Caret-down"></span>' in response:
            # Extract market value using the helper function
            market_value = extract_substring(response, '<span color="neutral6" font-weight="semibold" font-size="1" data-sensors-click="true" class="sc-4984dd93-0 sc-994ef6db-0 bKfFVd">', '</span>')
            # Extract current news using the helper function
            current_news = extract_substring(response, '<span class="icon-Caret-down"></span>', ' over the last day').replace('<!-- -->%</span>', '').split(' ')
            # Make a GET request to the API and get the JSON response
            api_response = requests.get(
                'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol=BTC,ETH,LTC,USDT',
                headers={
                    "Accepts": "application/json",
                    "X-CMC_PRO_API_KEY": "5d1a48f1-ab43-42f9-8b0c-54ec2206a04f"
                }
            ).json()
            # Extract current prices from the API response and round them to 4 decimal places
            btc_current_price = round(api_response['data']['BTC']['quote']['USD']['price'], 4)
            eth_current_price = round(api_response['data']['ETH']['quote']['USD']['price'], 4)
            ltc_current_price = round(api_response['data']['LTC']['quote']['USD']['price'], 4)
            usdt_current_price = round(api_response['data']['USDT']['quote']['USD']['price'], 4)

            # Return a formatted string with all the extracted information
            return f"Today's Cryptocurrency Prices by Market Cap\n\t-> The global crypto market cap is {market_value}, a {current_news[0]}% {current_news[1]} over the last day.\n\t->Here are the current prices of some cryptocurrencies:\n\t\tBitcoin (BTC): ${btc_current_price}\n\t\tEthereum (ETH): ${eth_current_price}\n\t\tLitecoin (LTC): ${ltc_current_price}\n\t\tUnited States Department of the Treasury (USDT): ${usdt_current_price}"

        else:
            # Return an error message if something went wrong
            return "An error occurred while fetching cryptocurrency news."

    @staticmethod
    def get_latest_news(topic, lang_code='en'):
        """
        Fetches and prints the latest news about a given topic.

        Parameters:
        topic (str): The topic to fetch news about.
        lang_code (str): The language code for the news. Default is 'en' for English.

        Returns:
        str: A string containing the latest news about the topic. If no news is found, it returns a message saying so.
        """
        import requests  # Importing requests module for making HTTP requests
        import datetime  # Importing datetime module for working with dates

        # Making a GET request to News API and getting JSON response
        response = requests.get(
            f'https://newsapi.org/v2/everything?q={topic}&language={lang_code}&from={datetime.date.today()}&searchIn=title,description&sortBy=publishedAt&apiKey=5b45a89fe4ad448bbf44126c105d521c'
        ).json()

        # Checking if there are any results
        if response['totalResults'] != 0:
            # Getting the first article from the response
            response = response['articles'][0]
            # Returning a formatted string with the article information
            return f"Latest News on '{topic}'\n\t-> Source: {response['source']['name']}\n\t-> Author: {response['author']}\n\t-> Title: {response['title']}\n\t-> Description: {response['description']}\n\t-> Published at: {response['publishedAt']}"

        else:
            # Returning a message if no news was found for the topic
            return f"No latest news found for '{topic}'."

    @staticmethod
    def get_latest_weather(location):
        """
        Fetches and prints the latest weather forecast for a given location.

        Parameters:
        location (str): The location to fetch the weather forecast for.

        Returns:
        str: A string containing the weather forecast. If no forecast is found, it returns a message saying so.
        """
        import requests  # Importing requests module for making HTTP requests

        # Making a GET request to Weather API and getting JSON response
        response = requests.get(
            f'https://api.weatherapi.com/v1/forecast.json?key=79a860b470a145afa5f190821231109&q={location.replace(" ", "+")}'
        ).json()

        # Checking if there is a forecast in the response
        if response['forecast']['forecastday'][0]['day']['condition']['text']:
            # Getting the forecast from the response
            forecast = response['forecast']['forecastday'][0]['day']['condition']['text']
            # Returning a formatted string with the forecast
            return f"It will be a {forecast} day in {location}."

        else:
            # Returning a message if no weather data was found for the location
            return "No weather data found for the specified location."


if __name__ == "__main__":
    scraper = AutomationScraper()  # Creating an instance of AutomationScraper class
    print(scraper.fetch_crypto_news())  # Printing cryptocurrency news
    print(scraper.get_latest_news('ai'))  # Printing the latest news on 'ai'
    print(scraper.get_latest_weather('Vipin Garden New Delhi'))  # Printing the latest weather for 'Vipin Garden New Delhi'
