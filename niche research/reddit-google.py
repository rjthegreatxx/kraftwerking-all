import pandas as pd
from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException

# Google Ads API Credentials
DEVELOPER_TOKEN = 'your_developer_token'
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
REFRESH_TOKEN = 'your_refresh_token'
CLIENT_CUSTOMER_ID = 'your_client_customer_id'  # Replace with your Google Ads account ID

# Initialize Google Ads Client
google_ads_client = GoogleAdsClient.load_from_storage()
google_ads_client.config.update({
    'developer_token': DEVELOPER_TOKEN,
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'refresh_token': REFRESH_TOKEN,
    'login_customer_id': CLIENT_CUSTOMER_ID,
})

def get_keyword_metrics(keywords):
    keyword_plan_idea_service = google_ads_client.get_service('KeywordPlanIdeaService', version='v6')
    location_ids = [...]  # List of location criteria IDs
    language_id = '1000'  # Language criterion ID for English

    keyword_plan_network = client.get_type('KeywordPlanNetworkEnum').GOOGLE_SEARCH_AND_PARTNERS

    try:
        response = keyword_plan_idea_service.generate_keyword_ideas(
            customer_id=CLIENT_CUSTOMER_ID,
            language=language_id,
            geo_target_constants=location_ids,
            keyword_plan_network=keyword_plan_network,
            keyword_seed={'keywords': keywords}
        )

        keyword_data = []
        for result in response.results:
            keyword_data.append({
                'Keyword': result.text.value,
                'Avg. Monthly Searches': result.keyword_idea_metrics.avg_monthly_searches.value,
                'Competition': result.keyword_idea_metrics.competition.name,
                'CPC': result.keyword_idea_metrics.average_cpc.value / 1e6  # Convert from micros to currency units
            })

        return pd.DataFrame(keyword_data)

    except GoogleAdsException as ex:
        print(f'Request failed with status {ex.error.code().name} and includes the following errors:')
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f'\t\tOn field: {field_path_element.field_name}')
        return pd.DataFrame()

# Example usage
keywords = ['data engineering', 'web development', 'system administration', 'marketing']
df = get_keyword_metrics(keywords)
print(df)
