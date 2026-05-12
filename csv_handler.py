import csv
from VAT import findVAT
import sys

csv.field_size_limit(9000000)

def transformToCSV(details):
    with open('metadata.csv', mode='r', encoding='utf8') as file:
        csvFile = csv.reader(file) # 11 for isBussnis 21 for region

        with open('single_account.csv', mode='w', encoding='utf8', newline='') as output:
            line = []
            csvOutput = csv.writer(output)
            csvOutput.writerow(next(csvFile))

            account = details['data']['user']['username']
            biography = details['data']['user']['biography']
            business_address_json = details['data']['user']['business_address_json']
            business_category_name = details['data']['user']['business_category_name']
            business_email = details['data']['user']['business_email']
            external_url = details['data']['user']['external_url']
            fbid = details['data']['user']['fbid']
            followers = details['data']['user']['edge_followed_by']['count']
            following = details['data']['user']['edge_follow']['count']
            highlight = ""
            id = details['data']['user']['id']

            is_business_account = "yes" if details['data']['user']['is_business_account'] else "no"
            is_professional_account = "yes" if details['data']['user']['is_professional_account'] else "no"
            is_verified = "yes" if details['data']['user']['is_verified'] else "no"

            posts = "null"
            posts_count = details['data']['user']['edge_owner_to_timeline_media']['count']
            profile_pic_url = details['data']['user']['profile_pic_url']



            profile_name = "null"
            timestamp = "null"
            highlights_count = details['data']['user']['highlight_reel_count']

            country_code = "null"
            region = "null"
            avg_engagement = "0"

            post_hashtags = []
            for i in range(int(posts_count)):
                post_hashtags.append("post")
            
            maybe_country_codes = "Unknown"
            bio_hashtags = details['data']['user']['biography_with_entities']['entities']
            avatar_cached = "null"
            category_enum = "null"
            category_name = "null"
            changelog = "null"
            full_name = details['data']['user']['full_name']
            is_private = "yes" if details['data']['user']['is_private'] else "no"

            line.append(account)
            line.append(biography)
            line.append(business_address_json)
            line.append(business_category_name)
            line.append(business_email)
            line.append(external_url)
            line.append(fbid)
            line.append(followers)
            line.append(following)
            line.append(highlight)
            line.append(id)
            line.append(is_business_account)
            line.append(is_professional_account)
            line.append(is_verified)
            line.append(posts)
            line.append(posts_count)
            line.append(profile_pic_url)
            line.append(profile_name)
            line.append(timestamp)
            line.append(highlights_count)
            line.append(country_code)
            line.append(region)
            line.append(avg_engagement)
            line.append(post_hashtags)
            line.append(maybe_country_codes)
            line.append(bio_hashtags)
            line.append(avatar_cached)
            line.append(category_enum)
            line.append(category_name)
            line.append(changelog)
            line.append(full_name)
            line.append(is_private)

            line.append("")
            line.append("0.00%")
            line.append("Full Trust")
            line.append("Trusted")
            
            importantDetails = {'VAT/Commercial': findVAT(biography)[0],
                                'Username': account,
                                'Business Email':business_email,
                                'External Url':external_url,
                                'ID': id,
                                'Followers': followers,
                                'Following': following,
                                'Verified': is_verified,
                                'Posts': posts_count,
                                'Full Name': full_name,
                                'Private' : is_private}
            #0.00%	Full Trust	Trusted

            csvOutput.writerow(line)

            with open('NewData.csv', mode='a', encoding='utf8', newline='') as add:
               addOut = csv.writer(add)
               
               print(line)
               addOut.writerow(line)

               
            output.close()
    return importantDetails