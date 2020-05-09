# f-bot
Bot for hunting delivery dates on frisco.pl.

## Getting Started
1. Download repo to your device.

```e.g. $ git clone https://github.com/Mrooie/f-bot.git```

2. Create virtualenv and activate it

```
/f-bot
$ virtualenv <venv_name>
$ . <venv_name>/bin/activate
```

3. Install dependencies to your virtualenv, using requirements.txt

```
pip install -r requirements.txt
```

4. Replace placeholders in .env with your data.
```
EMAIL=<your_frisco_login_email>
PASSWORD=<your_frisco_password>
```

5. Install Selenium WebDriver 

6. Set the range of days when you want to get your delivery.
Change ```BUFFER_DAYS=<days>``` in ```scraper.py``` for any int you like.

7. Run scraper.py

 - Linux and Mac:

```python scraper.py```

or

```./scraper.py``` - if you have permissions ;)

## Installing selenium WebDriver

To work properly, f-bot needs the selenium web driver. You can use any driver you want, I wanned to try Chrome. :P
Remember, that you need to have according browser installed. ;)

You can manually download [Chrome Driver](https://chromedriver.chromium.org/downloads) and insert its path in scraper.py - ```DRIVER_PATH=<path>```

OR

##### You can use brew on MacOs:
```$ brew cask install chromedriver```
in this case path to driver is ```r"/usr/local/bin/chromedriver"```

## How it works

* F-bot launches your browser in a new window, opens frisco.pl website and logs you in.
* If the nearest delivery date falls on a day outside your set range, f-bot refreshes page and checks again.
* If delivery date falls on a day in your set range, F-bot makes a reservation and exits, keeping your browser open on the finished reservation.

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* If you want to use that bot, please don't go crazy! :P We all want to have a chance for a delivery!
