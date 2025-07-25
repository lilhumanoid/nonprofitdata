import pandas as pd
from faker import Faker
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

fake = Faker()
Faker.seed(13)

def get_diverse_name_by_gender(gender):
    locales = ['en_US', 'es_MX', 'en_UK', 'pt_BR']
    locale = np.random.choice(locales)
    diverse_fake = Faker(locale)
    if gender == 'Female':
        return diverse_fake.name_female()
    elif gender == 'Male':
        return diverse_fake.name_male()
    else:
        return diverse_fake.name()

def get_realistic_acquisition_source(donor_type):
    if donor_type == 'Foundation/Corporate':
        return np.random.choice([
            'Foundation Outreach', 'Partner Organization', 'Website Donation',
            'Email Campaign', 'Referral'
        ], p=[0.50, 0.30, 0.10, 0.07, 0.03])
    elif donor_type == 'Major Individual':
        return np.random.choice([
            'Foundation Outreach', 'Partner Organization', 'Website Donation',
            'Email Campaign', 'Event', 'Referral'
        ], p=[0.25, 0.20, 0.25, 0.15, 0.10, 0.05])
    elif donor_type == 'Monthly Sustainers':
        return np.random.choice([
            'Website Donation', 'Meta Ads', 'Nurture Campaign',
            'Email Campaign', 'Newsletter Signup', 'Volunteer Conversion'
        ], p=[0.40, 0.25, 0.15, 0.10, 0.06, 0.04])
    elif donor_type == 'Event Donors':
        return np.random.choice([
            'Earth Day Event', 'Fox Habitat Event', 'Bat Box Build Event',
            'Website Donation', 'Meta Ads', 'Volunteer Conversion'
        ], p=[0.35, 0.25, 0.20, 0.10, 0.06, 0.04])
    else:  # Small Online Donors
        return np.random.choice([
            'Website Donation', 'Meta Ads', 'Google Ads', 'Nurture Campaign',
            'Newsletter Signup', 'Peer-to-Peer Fundraising'
        ], p=[0.30, 0.25, 0.20, 0.12, 0.08, 0.05])

def get_realistic_campaign(donor_type, generation=None):
    if donor_type == 'Foundation/Corporate':
        return np.random.choice([
            'Annual Appeal', 'Emergency Response Fund', 'Biodiversity Action Program',
            'Gray Bat Habitat Fund', 'Crocodilian Conservation Challenge'
        ], p=[0.35, 0.25, 0.20, 0.12, 0.08])
    elif donor_type == 'Major Individual':
        return np.random.choice([
            'Annual Appeal', 'Giving Season', 'Emergency Response Fund',
            'Endangered Species Fund', 'Biodiversity Action Program', 'Arctic Fox Day'
        ], p=[0.30, 0.25, 0.15, 0.12, 0.10, 0.08])
    elif donor_type == 'Monthly Sustainers':
        return np.random.choice([
            'Monthly Giving Program', 'Annual Appeal', 'Giving Season',
            'Arctic Fox Day', 'Pollinator Protection Project'
        ], p=[0.60, 0.15, 0.10, 0.08, 0.07])
    elif donor_type == 'Event Donors':
        if generation in ['Gen Z', 'Millennial']:
            return np.random.choice([
                'Earth Day Events', 'Red Fox Run 5K', 'Kids 4 Climate School Fundraiser',
                'Arctic Fox Day', 'Gray Bat Habitat Fund', 'Annual Appeal'
            ], p=[0.30, 0.25, 0.20, 0.10, 0.08, 0.07])
        else:  # Gen X, Boomer
            return np.random.choice([
                'Earth Day Events', 'Annual Appeal', 'Giving Season',
                'Red Fox Run 5K', 'Gray Bat Habitat Fund', 'Endangered Species Fund'
            ], p=[0.25, 0.20, 0.18, 0.15, 0.12, 0.10])
    else:  # Small Online Donors
        if generation in ['Gen Z', 'Millennial']:
            return np.random.choice([
                'Arctic Fox Day', 'Kids 4 Climate School Fundraiser', 'Earth Day Events',
                'New Year Giving Initiative', 'Whale Shark Supporter Program', 'Annual Appeal'
            ], p=[0.25, 0.20, 0.18, 0.12, 0.12, 0.13])
        else:
            return np.random.choice([
                'Annual Appeal', 'Giving Season', 'Arctic Fox Day',
                'Endangered Species Fund', 'Earth Day Events', 'Emergency Response Fund'
            ], p=[0.25, 0.20, 0.18, 0.15, 0.12, 0.10])

def create_donor_data(n_donors=507):
    donors = []

    donor_types = {
        'Foundation/Corporate': {'weight': 0.02, 'avg_donation': 25000, 'frequency': 1.5, 'std': 15000},
        'Major Individual': {'weight': 0.03, 'avg_donation': 5000, 'frequency': 2, 'std': 2000},
        'Monthly Sustainers': {'weight': 0.15, 'avg_donation': 35, 'frequency': 11, 'std': 15},  # $35/month
        'Event Donors': {'weight': 0.20, 'avg_donation': 150, 'frequency': 1.2, 'std': 75},
        'Small Online Donors': {'weight': 0.60, 'avg_donation': 45, 'frequency': 1.8, 'std': 25}  # Most donors!
    }

    for i in range(n_donors):
        donor_type = np.random.choice(
            list(donor_types.keys()),
            p=[donor_types[dt]['weight'] for dt in donor_types.keys()]
        )
        generation = np.random.choice(
            ['Gen Z', 'Millennial', 'Gen X', 'Boomer'],
            p=[0.15, 0.35, 0.30, 0.20]
        )

        age_mapping = {
            'Gen Z': ['18-30'],
            'Millennial': ['18-30', '31-45'],
            'Gen X': ['31-45', '46-60'],
            'Boomer': ['46-60', '60+']
        }

        if generation == 'Millennial':
            age_group = np.random.choice(age_mapping[generation], p=[0.3, 0.7])
        elif generation == 'Gen X':
            age_group = np.random.choice(age_mapping[generation], p=[0.4, 0.6])
        elif generation == 'Boomer':
            age_group = np.random.choice(age_mapping[generation], p=[0.3, 0.7])
        else:
            age_group = age_mapping[generation][0]

        if generation == 'Boomer':
            income_probs = [0.20, 0.35, 0.35, 0.10]
        elif generation == 'Gen X':
            income_probs = [0.25, 0.40, 0.25, 0.10]
        elif generation == 'Millennial':
            income_probs = [0.40, 0.35, 0.15, 0.10]
        else:  # Gen Z
            income_probs = [0.60, 0.25, 0.05, 0.10]

        income_bracket = np.random.choice(
            ['<$50k', '$50k-$100k', '$100k+', 'Prefer not to say'],
            p=income_probs
        )

        gender = np.random.choice(
            ['Female', 'Male', 'Non-binary', 'Prefer not to say'],
            p=[0.58, 0.40, 0.015, 0.005]
        )
        name = get_diverse_name_by_gender(gender)
        acquisition_source = get_realistic_acquisition_source(donor_type)

        donor = {
            'donor_id': f'DNR{i:04d}',
            'name': name,
            'gender': gender,
            'generation': generation,
            'age_group': age_group,
            'income_bracket': income_bracket,
            'email': fake.email(),
            'phone': fake.phone_number(),
            'address': fake.address().replace('\n', ', '),
            'donor_type': donor_type,
            'first_donation_date': fake.date_between(start_date='-5y', end_date='-1y'),
            'acquisition_source': acquisition_source
        }
        donors.append(donor)
    return pd.DataFrame(donors)

def create_donation_data(donors_df):
    donations = []
    donor_type_info = {
        'Foundation/Corporate': {'avg_donation': 25000, 'frequency': 1.5, 'std': 15000},
        'Major Individual': {'avg_donation': 5000, 'frequency': 2, 'std': 2000},
        'Monthly Sustainers': {'avg_donation': 35, 'frequency': 11, 'std': 15},
        'Event Donors': {'avg_donation': 150, 'frequency': 1.2, 'std': 75},
        'Small Online Donors': {'avg_donation': 45, 'frequency': 1.8, 'std': 25}
    }

    for _, donor in donors_df.iterrows():
        type_info = donor_type_info[donor['donor_type']]
        num_donations = max(1, int(np.random.poisson(type_info['frequency'])))
        
        for _ in range(num_donations):
            amount = max(5, np.random.normal(
                type_info['avg_donation'],
                type_info['std']
            ))
            start_date = donor['first_donation_date']
            end_date = datetime.now()
            donation_date = fake.date_between(start_date=start_date, end_date=end_date)
            campaign = get_realistic_campaign(donor['donor_type'], donor['generation'])
            
            donation = {
                'donation_id': fake.uuid4(),
                'donor_id': donor['donor_id'],
                'amount': round(amount, 2),
                'donation_date': donation_date,
                'campaign': campaign,
                'method': np.random.choice([
                    'Credit Card', 'Check', 'Bank Transfer', 'PayPal', 'Cash', 'Venmo'
                ], p=[0.35, 0.25, 0.15, 0.15, 0.05, 0.05])
            }
            donations.append(donation)
    return pd.DataFrame(donations)

print("🌲 Generating conservation nonprofit data...")
donors_df = create_donor_data(500)
donations_df = create_donation_data(donors_df)

merged_df = donations_df.merge(donors_df, on='donor_id')

print(f"Generated {len(donors_df)} donors and {len(donations_df)} donations")
print("\nSample data:")
print(merged_df[['name', 'gender', 'generation', 'income_bracket', 'donor_type', 'amount', 'campaign']].head())

print("\n=== CONSERVATION NONPROFIT INSIGHTS ===")

print("\n1. DONOR DEMOGRAPHICS:")
gender_analysis = merged_df.groupby('gender').agg({
    'amount': ['sum', 'mean', 'count']
}).round(2)
gender_analysis.columns = ['Total_Raised', 'Avg_Donation', 'Num_Donations']
print("By Gender:")
print(gender_analysis)

print("\nBy Generation:")
gen_analysis = merged_df.groupby('generation').agg({
    'amount': ['sum', 'mean', 'count']
}).round(2)
gen_analysis.columns = ['Total_Raised', 'Avg_Donation', 'Num_Donations']
print(gen_analysis.sort_values('Total_Raised', ascending=False))

print("\n2. CAMPAIGN PERFORMANCE:")
campaign_analysis = merged_df.groupby('campaign').agg({
    'amount': ['sum', 'mean', 'count']
}).round(2)
campaign_analysis.columns = ['Total_Raised', 'Avg_Donation', 'Num_Donations']
print(campaign_analysis.sort_values('Total_Raised', ascending=False).head(10))

print("\n3. ACQUISITION SOURCE EFFECTIVENESS:")
source_analysis = merged_df.groupby('acquisition_source').agg({
    'amount': ['sum', 'mean', 'count']
}).round(2)
source_analysis.columns = ['Total_Raised', 'Avg_Donation', 'Num_Donations']
print(source_analysis.sort_values('Total_Raised', ascending=False))

print("\n4. MOST CONSISTENT DONORS:")
consistency = donations_df.groupby('donor_id').agg({
    'amount': ['count', 'sum', 'mean']
}).round(2)
consistency.columns = ['Donation_Count', 'Total_Given', 'Avg_Donation']
consistency = consistency.merge(donors_df[['donor_id', 'name', 'donor_type', 'generation']], on='donor_id')
print(consistency.sort_values('Donation_Count', ascending=False).head(10))

donors_df.to_csv('conservation_donors.csv', index=False)
donations_df.to_csv('conservation_donations.csv', index=False)
merged_df.to_csv('conservation_analysis.csv', index=False)

print("\n✅ Conservation nonprofit data saved to CSV files!")
print("🦊 Ready for your donor data dashboard! 📊")