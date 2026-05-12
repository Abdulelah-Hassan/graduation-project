import csv
import math

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
    if len(data) < 8:
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
        calculated_line['trust_percentage'] = str(trust) + "%"
        calculated_line['Trust'] = getTrust(trust)
        return calculated_line
    except:
        return calculated_line


data = []
with open('Insta(5000).csv', mode='r', encoding='utf8') as file:
    csvFile = csv.DictReader(file)
    with open('Insta_output.csv', mode='w', encoding='utf8', newline='') as output:
        csvOutput = csv.writer(output)
        csvOutput.writerow(next(csvFile))
        for lines in csvFile:
            line = calculate(lines)
            row = []
            for val in line.values():
                row.append(val)
            data.append(row)
   
        csvOutput.writerows(data)
        output.close()