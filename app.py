import streamlit as st
from datetime import date, datetime

from crawling_weather import crwalingweather

current_date = date.today()  # 이 라인 변경

city = st.text_input('City','seoul')
st.write('selected city : ', city)

d = st.date_input("Date", current_date)
st.write('selected city : ', d)


def fetch_weather(city_, selected_date):
    st.write(f'Fetching weather information for {city_} on {selected_date}...')
    # parse_date = datetime.strptime(selected_date, "%Y-%m-%d")


    if d > current_date:
        st.write('Cannot Select Future Date')
    else:
        result = crwalingweather(city_, selected_date)
        st.write("### One year ago:")
        st.write(f"**Temperature:** {result['one_year_ago_temp']}, **Weather:** {result['one_year_ago_wdesc']}")

        st.write("### Two years ago:")
        st.write(f"**Temperature:** {result['two_year_ago_temp']}, **Weather:** {result['two_year_ago_wdesc']}")

        st.write("### Three years ago:")
        st.write(f"**Temperature:** {result['three_year_ago_temp']}, **Weather:** {result['three_year_ago_wdesc']}")


if st.button('Get Weather'):
    fetch_weather(city, d)
