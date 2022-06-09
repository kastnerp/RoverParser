import streamlit as st
import pandas as pd
import numpy as np 
from re import sub
from decimal import Decimal
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
import matplotlib as mpl
mpl.rc("figure", dpi=100)
import numpy as np
import re
import pandas as pd
import seaborn as sns
import time
sns.set_style("ticks")

#Importing the Nominatim geocoder class 
from geopy.geocoders import Nominatim
 

st.title("RoverParser")


location = st.text_input('City to search for', 'New York, NY')




geolocator = Nominatim(user_agent="my_request")



st.cache()
class ZipCodes():
    def __init__(self):
        self.zip_coords = pd.read_csv(
            "https://gist.githubusercontent.com/erichurst/7882666/raw/5bdc46db47d9515269ab12ed6fb2850377fd869e/US%2520Zip%2520Codes%2520from%25202013%2520Government%2520Data")

    def get_lat_lon(self, zip_code):
        try:
            self.coords = self.zip_coords[self.zip_coords['ZIP'] == int(zip_code)]
            LAT = float(self.coords['LAT'].values)
            LON = float(self.coords['LNG'].values)

            return LAT, LON

        except:
            return None, None


zips = ZipCodes()


class RoverSettings():
    def __init__(self, loc):

        self.loc = loc

        self.repeat_client_class = "CalloutBadge__Badge-rduqlb-0 iuzSam InfoPills__StyledCalloutBadge-sc-1jou7n9-4 jHASEn"
        self.price_class = "PriceAndFavoriteColumn__Price-sc-5y9bmw-3 hYSwMH"
        self.sitter_class = "VerticalLayout-sc-31y83h-0 SearchResultCard__SearchResultCardWrapper-sc-186pa8o-1 csDLKS bsrZxg"
        self.name_class = "NameRow__StyledNameAndBadge-t135c7-1 iecWGG"
        self.sitter_location_class = "InfoColumn__Location-qduboa-2 gJTzwa"


         
        #making an instance of Nominatim class
        #geolocator = Nominatim(user_agent="my_request")
        
        #applying geocode method to get the location
        location = geolocator.geocode(self.loc, addressdetails=True)
        


    
        self.LAT = location.latitude
        self.LON = location.longitude
        self.zip_code = location.address.split(",")[-2]

        self.num_pages = 4


class Sitter():
    def __init__(self):
        self.price = None
        self.repeating_customers = None
        self.name = None
        self.location = None
        self.zip_code = None



    def get_lat_lon(self):
        #st.write(zips.get_lat_lon(self.zip_code))

        self.LAT, self.LON  = zips.get_lat_lon(self.zip_code)

    def as_dict(self):
        return {'name': self.name, 'location': self.location,'zip_code': self.zip_code, 'repeating_customers': self.repeating_customers, 'price': self.price}

    def as_location_dict(self):
        return {'lat': self.LAT, 'lon': self.LON}






settings = RoverSettings(location)


st.write((settings.LAT, settings.LON))


data ={'lat':[settings.LAT],   'lon':[ settings.LON]}



# Create DataFrame
df = pd.DataFrame(data)

st.map(df)


start_date = '05%2F14%2F2022'
end_date = '05%2F15%2F2022'


# most similar to us
url = "https://www.rover.com/search/?alternate_results=true&override_check=true&accepts_only_one_client=false&apse=false&bathing_grooming=false&cat_care=false&centerlat={1}&centerlng={2}&dogs_allowed_on_bed=true&dogs_allowed_on_furniture=true&end_date={4}&frequency=onetime&morning_availability=false&midday_availability=false&evening_availability=false&fulltime_availability=true&giant_dogs=false&has_fenced_yard=true&has_house=false&has_no_children=false&is_premier=false&knows_first_aid=false&large_dogs=false&location={4}&location_accuracy=1000&maxprice=150&medium_dogs=true&minprice=1&no_caged_pets=false&no_cats=false&no_children_0_5=false&no_children_6_12=false&non_smoking=true&page={0}&person_does_not_have_dogs=true&pet=&petsitusa=false&pet_type=dog&puppy=false&service_type=overnight-boarding&small_dogs=true&spaces_required=1&start_date={3}&search_score_debug=false&injected_medication=false&special_needs=false&oral_medication=false&more_than_one_client=false&uncrated_dogs=false&unspayed_females=false&non_neutered_males=false&females_in_heat=false&unactivated_provider=false&premier_matching=false&premier_or_rover_match=false&is_member_of_sitter_to_sitter=false&is_member_of_sitter_to_sitter_plus=false&location_type=zip-code&raw_location_types=postal_code&dog_size=small,medium"



from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

options = Options()
options.add_argument('--headless')

#driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()),options=options)
#driver.get("https://www.google.com")
#print('Done')
#driver.quit()



def get_sitters(i, sitter_divs, settings):

    s = Sitter()

    name_string = str(sitter_divs[i].find(
        "div", {"class": settings.name_class}).text).replace('\xa0', '')    

    price_string = sitter_divs[i].find("div", {"class": settings.price_class}).string

    location_string = sitter_divs[i].find( "span", "InfoColumn__Location-qduboa-2 gJTzwa").string
    #st.write(location_string)

    s.name = name_string
    s.price = float(Decimal(sub(r'[^\d.]', '', price_string)))
    s.location = location_string
    s.zip_code = location_string.split(',')[-1]
    s.get_lat_lon()

    try:
        repeated_clients_string = sitter_divs[i].find(
            "span", {"class": settings.repeat_client_class}).string
        if str.endswith(repeated_clients_string, 'repeat clients'):
            rc = int(re.findall(r'\d+', repeated_clients_string)[0])
            s.repeating_customers = rc
    except:
        s.repeating_customers = 0

    #print(s.name, s.price, s.repeating_customers)

    return s


from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

options = Options()
options.add_argument('--headless')

driver = webdriver.Firefox(service=Service( GeckoDriverManager().install()), options=options)



sitters = []

my_bar = st.progress(0)
max_results = (settings.num_pages * 20) - 20

st.write(max_results)

for page in range(1, settings.num_pages):

    driver.get(url.format(page, settings.LAT, settings.LON,
               start_date, end_date, settings.zip_code))

    html = driver.page_source
    page_html = BeautifulSoup(html)

    sitter_divs = page_html.find_all("div", {"class": settings.sitter_class})

    for i, sitter in enumerate(sitter_divs):

        s = get_sitters(i, sitter_divs, settings)

        sitters.append(s)

        my_bar.progress(len(sitters)/max_results)





sitters_df =  pd.DataFrame([x.as_dict() for x in sitters])

st.dataframe(sitters_df)




sitters_location_df = pd.DataFrame([x.as_location_dict() for x in sitters])



st.map(sitters_location_df.dropna(thresh=2))











keys_in_class = vars(sitters[0]).keys()

df = pd.DataFrame([[getattr(i,j) for j in keys_in_class] for i in sitters], columns = keys_in_class)
df = df.drop_duplicates()

df.to_csv("results.csv", index=False)

filtered = df.loc[(df['repeating_customers'] > 1) & (df['repeating_customers'] < 125 ) & (df['price'] < 150 ) ]

#filtered.sort_values(by=['repeating_customers']).to_csv("repeating_customers_"+str(zip_code)+".csv")
filtered.sort_values(by=['repeating_customers'])


sns.displot(filtered, x="price", y="repeating_customers",binwidth=(5, 5), cbar='True',cbar_kws={'label': 'observations'}, legend= True)
plt.xlim(0, 120)
plt.ylim(0, 100)
#plt.savefig('displot_price_rc_'+str(zip_code)+'.png', transparent=False)
plt.show()