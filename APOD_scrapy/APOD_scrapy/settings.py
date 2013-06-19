# Scrapy settings for APOD_scrapy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'APOD_scrapySpider'

SPIDER_MODULES = ['APOD_scrapy.spiders']
NEWSPIDER_MODULE = 'APOD_scrapy.spiders'

ITEM_PIPELINES = ['APOD_scrapy.pipelines.MyImagesPipeline',
                  'APOD_scrapy.pipelines.guardadoSQLPipeline',
                  'APOD_scrapy.pipelines.guardadoXMLPipeline',
                    ]

IMAGES_STORE = '/home/dj/Escritorio'
IMAGES_THUMBS = {
    'medianas': (600, 400),
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'APOD_scrapy (http://osl.ugr)'
