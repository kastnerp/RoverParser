



from bs4 import BeautifulSoup

import requests


page = requests.get("https://www.rover.com/search/?alternate_results=true&override_check=true&accepts_only_one_client=false&apse=false&bathing_grooming=false&cat_care=false&centerlat=40.79164069999999&centerlng=-73.9447994&dogs_allowed_on_bed=false&dogs_allowed_on_furniture=false&end_date=02%2F15%2F2022&frequency=onetime&morning_availability=false&midday_availability=false&evening_availability=false&fulltime_availability=true&giant_dogs=false&has_fenced_yard=false&has_house=false&has_no_children=false&is_premier=false&knows_first_aid=false&large_dogs=false&location=New%20York%2C%20NY%2010029%2C%20USA&location_accuracy=5161&maxprice=150&medium_dogs=true&minprice=49&no_caged_pets=false&no_cats=false&no_children_0_5=false&no_children_6_12=false&non_smoking=false&page=5&person_does_not_have_dogs=false&pet=&petsitusa=false&pet_type=dog&puppy=false&service_type=overnight-boarding&small_dogs=false&spaces_required=1&start_date=02%2F14%2F2022&search_score_debug=false&injected_medication=false&special_needs=false&oral_medication=false&more_than_one_client=false&uncrated_dogs=false&unspayed_females=false&non_neutered_males=false&females_in_heat=false&unactivated_provider=false&premier_matching=false&premier_or_rover_match=false&is_member_of_sitter_to_sitter=false&is_member_of_sitter_to_sitter_plus=false&location_type=zip-code&raw_location_types=postal_code&dog_size=medium")


soup = BeautifulSoup(page.content, 'html.parser')


mydivs = soup.find_all("div", {"class": "PriceAndFavoriteColumn__Price-sc-5y9bmw-3 hYSwMH"})

print(len(mydivs))

for p in mydivs:
    print(p)