import csv
import math
import sys

csv.field_size_limit(9000000)
# THE SUM SHOULD BE 1!
VAT_NUMBER = 0.1
FOLLOWER_RATION = 0.1
PROFILE_COMPLETENESS = 0.3
ACTIVITY_SCORE = 0.4
API_DATA = 0.1
######################################

def bounded_growth(X, k=0.1, c=35.0):
    return 1 / (1 + math.exp(-k * (X - c)))


def getTrust(value):
    if value >= 70:
        return "Full Trust"
    elif value >= 50:
        return "Moderate Trust"
    elif value >= 30:
        return "Low Trust"
    
    return "Untrust"

def getProfile(data):
    if len(data) < 4:
        return float(0)
    return float(1)

def calculate(line):
    calculated_line = line

    try:
        vat_number = 1
        follower_ration = float(line['followers']) /  (float(line['followers']) + float(line['following']))
        profile_completeness = (getProfile(line['biography']) + getProfile(line['full_name']) + getProfile(line['business_email']))/3
        activity_score = bounded_growth(float(line['posts_count']))
        api_data = 1
       
        trust = ((vat_number * VAT_NUMBER) + (follower_ration * FOLLOWER_RATION) + (profile_completeness * PROFILE_COMPLETENESS) + (activity_score * ACTIVITY_SCORE) + (api_data * API_DATA)) * 100
        calculated_line['trust_percentage'] = str(round(trust,2)) + "%"
        calculated_line['Trust'] = getTrust(trust)
        print(f"{vat_number * VAT_NUMBER}+{follower_ration * FOLLOWER_RATION}+{profile_completeness * PROFILE_COMPLETENESS}+{activity_score * ACTIVITY_SCORE}+{api_data * API_DATA}", "\n\n\n\n")
        return round(trust,2)
    except:
        return float(0)



def getPercentage():
    with open('single_account.csv', mode='r', encoding='utf8') as file:
        csvFile = csv.DictReader(file)
        
        
        
        line = calculate(next(csvFile))
        return line       

