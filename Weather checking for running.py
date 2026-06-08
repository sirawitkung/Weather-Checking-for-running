import requests
import sys

api_key="4cc87357-05c0-466e-8380-cda3fcb64fff"
city1="Samut Prakan"
state="Samut Prakan"
country="Thailand"
base_url="http://api.airvisual.com/v2/city"



def get_local_air_quality():
    params = {"city":city1,
              "state":state,
              "country":country,
              "key":api_key, }
    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            city = data['data']['city']
            aqi = data['data']['current']['pollution']['aqius']
            main_pollutant = data['data']['current']['pollution']['mainus']
            Temperature = data['data']['current']['weather']['tp']
            Weather = data['data']['current']['weather']['ic']
            Humidity = data['data']['current']['weather']['hu']
            return aqi,Temperature,Weather,main_pollutant,city,Humidity
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return -1

    except Exception as e:
        print(f"⚠️ An error occurred: {e}")
        return -1
    


def Weather_code_to_text(A):
    if A in ["01d","01n"]:
        return "Clear Sky"
    elif A in["02d","02n"]:
        return "Few Clouds"
    elif A in["03d","03n"]:
        return "Scattered clouds"
    elif A in["04d","04n"]:
        return "Broken clouds"
    elif A in["09d","09n"]:
        return "Shower rain"
    elif A in["10d","10n"]:
        return "Rain"
    elif A in["11d","11n"]:
        return 	"Thunderstorm"
    elif A in["13d","13n"]:
        return "Snow"
    elif A in["50d","50n"]:
        return "Mist / Haze / Fog"
    else:
        return "Check Conditions Manually"



def should_run(aqi,Temperature,Weather,Humidity):
    if aqi>150 or (Temperature>35 or Temperature<15) or Weather in["10d","10n","11d","11n","13d","13n"] or Humidity>90:
        return "Dangerous"
    elif (aqi<=150 and aqi>=101) or (Temperature<=35 and Temperature>=32 or Temperature<=17 and Temperature>=15) or Weather in["09d","09n"] or (80<=Humidity<=90):
        return "Be cautious"
    elif aqi<50 and Temperature<28 and Temperature>=23 and Weather in["01d","01n","02d","02n","03d","03n","04d","04n"] and Humidity<70:
        return "Excellent"
    elif aqi<=100 and (18<=Temperature<32) and Weather in["01d","01n","02d","02n","03d","03n","04d","04n","50d","50n"] and Humidity<=80:
        return "Good"
    else:
        return "Check Conditions Manually"



def main_pollutant_code_to_text(A):
    if A  == "p2":
        return "PM2.5"
    elif A == "p1":
        return "PM10"
    elif A == "o3":
        return "Ozone"
    elif A == "n2":
        return "Nitrogen Dioxide"
    elif A == "s2":
        return "Sulfur Dioxide"
    elif A == "co":
        return "Carbon Monoxide"
    else:
        return "Check Conditions Manually"


if __name__ == "__main__":
    result=get_local_air_quality()
    if result == -1 or len(result) !=6:
        sys.exit()
    else:
        aqi,Temperature,Weather,main_pollutant,city,Humidity=result



        #THIS IS FOR DEBUG ONLY
        #aqi=49
        #Temperature=33
        #Humidity=69
        #city="cat"
        #Weather="01d"
        #main_pollutant="Cat fur"



        print(f"\fCurrent City: {city}\nCurrent Temperature: {Temperature} Celsius\nCurrent weather: {Weather_code_to_text(Weather)}\nCurrent AQI: {aqi}\nMain pollutant: {main_pollutant_code_to_text(main_pollutant)}\nCurrent Hudmidity: {Humidity}\nShould you run condition: {should_run(aqi,Temperature,Weather,Humidity)}\f")