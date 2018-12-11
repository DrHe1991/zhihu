# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import Spider, Request
from zhihu.items import UserItem
import time

class ZhihuUserSpider(scrapy.Spider):
    name = 'zhihu_user'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    offset = 0
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&amp;offset={offset}&amp;limit={limit}'
    start_user = 'yun-tian-38'
    user_query = 'employments,gender,educations,business,voteup_count,thanked_count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,answer_count,articles_count,pins_count,question_count,commercial_question_count,favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active,is_force_renamed,is_bind_sina,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'
    followers_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
    def start_requests(self):
        yield Request(self.user_url.format(user=self.start_user, include=self.user_query), self.parse_user)
        yield Request(self.followers_url.format(user=self.start_user, include=self.followers_query, limit=20, offset=self.offset), self.parse_followers)
    
    # this is used to parse every user's info
    def parse_user(self, response):
        result = json.loads(response.text)
        item = UserItem()
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)
        yield item

    # this is used to parse followers' list
    def parse_followers(self, response):
        results = json.loads(response.text)
        # loop the userlist and do the user info parse again 
        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user=result.get('url_token'), include=self.user_query),self.parse_user)
                time.sleep(1)
        # move to next page and do the follower's list parse again 
        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            # next_page = results.get('paging').get('next')
            # above is not working cuz next_page is not showing the right url
            next_page = self.followers_url.format(user=self.start_user, include=self.followers_query, limit=20, offset=self.offset+20)        
            yield Request(next_page,self.parse_followers)
            self.offset += 20

