"""
 Subtitleseeker (Video)

 @website     http://www.subtitleseeker.com
 @provide-api no

 @using-api   no
 @results     HTML
 @stable      no (HTML can change)
 @parse       url, title, content
"""

from urllib import quote_plus
from lxml import html
from searx.languages import language_codes
from searx.engines.xpath import extract_text

# engine dependent config
categories = ['videos']
paging = True
language = ""

# search-url
url = 'http://www.subtitleseeker.com/'
search_url = url + 'search/TITLES/{query}&p={pageno}'

# specific xpath variables
results_xpath = '//div[@class="boxRows"]'


# do search-request
def request(query, params):
    params['url'] = search_url.format(query=quote_plus(query),
                                      pageno=params['pageno'])
    return params


# get response from search-request
def response(resp):
    results = []

    dom = html.fromstring(resp.text)

    search_lang = ""

    if resp.search_params['language'] != 'all':
        search_lang = [lc[1]
                       for lc in language_codes
                       if lc[0][:2] == resp.search_params['language'].split('_')[0]][0]

    # parse results
    for result in dom.xpath(results_xpath):
        link = result.xpath(".//a")[0]
        href = link.attrib.get('href')

        if language is not "":
            href = href + language + '/'
        elif search_lang:
            href = href + search_lang + '/'

        title = extract_text(link)

        content = extract_text(result.xpath('.//div[contains(@class,"red")]'))
        content = content + " - "
        text = extract_text(result.xpath('.//div[contains(@class,"grey-web")]')[0])
        content = content + text

        if result.xpath(".//span") != []:
            content = content +\
                " - (" +\
                extract_text(result.xpath(".//span")) +\
                ")"

        # append result
        results.append({'url': href,
                        'title': title,
                        'content': content})

    # return results
    return results