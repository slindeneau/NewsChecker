import newsgrabber
paper_list = [
    'http://www.wsj.com/',
    'http://www.nytimes.com/',
    'http://www.usatoday.com/',
    'http://www.latimes.com/',
    'http://www.mercurynews.com/',
    'http://www.nydailynews.com/',
    'http://nypost.com/',
    'http://www.washingtonpost.com/',
    'http://chicago.suntimes.com/',
    'http://www.denverpost.com/',
    'http://www.chicagotribune.com/',
    'http://www.dallasnews.com/',
    'http://www.newsday.com/',
    'http://www.chron.com/',
    'http://www.ocregister.com/',
    'http://www.nj.com/starledger/',
    'http://www.tampabay.com/',
    'http://www.cleveland.com/#/0',
    'http://www.philly.com/inquirer/',
    'http://www.startribune.com/',
    'http://www.azcentral.com/',
    'http://www.staradvertiser.com/',
    'http://www.reviewjournal.com/',
    'http://www.sandiegouniontribune.com/',
    'http://www.bostonglobe.com/'
]

newsgrabber.get_articles_from(paper_list)
