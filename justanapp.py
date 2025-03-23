import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to load driver data
def load_driver_data():
    data = {
        'Driver': [
            'Stoffel Vandoorne', 'Mitch Evans', 'Edoardo Mortara', 'Jean-Eric Vergne', 
            'Antonio Felix da Costa', 'Jake Dennis', 'Nyck de Vries', 'Lucas di Grassi',
            'Pascal Wehrlein', 'Oliver Rowland'
        ],
        'Team': [
            'Mercedes-EQ', 'Jaguar TCS Racing', 'ROKiT Venturi Racing', 'DS Techeetah',
            'DS Techeetah', 'Avalanche Andretti', 'Mercedes-EQ', 'ROKiT Venturi Racing',
            'Porsche', 'Mahindra Racing'
        ],
        'Points': [213, 180, 169, 152, 145, 126, 106, 101, 89, 78],
        'Wins': [3, 2, 4, 2, 1, 2, 1, 2, 1, 0],
        'Podiums': [7, 6, 5, 5, 4, 3, 3, 4, 3, 2],
    }
    return pd.DataFrame(data)

# Function to load race results
def load_race_results():
    data = {
        'Race': [
            'Mexico City EPrix', 'Diriyah E-Prix (Race 1)', 'Diriyah E-Prix (Race 2)',
            'Rome E-Prix (Race 1)', 'Rome E-Prix (Race 2)', 'Monaco E-Prix',
            'Berlin E-Prix (Race 1)', 'Berlin E-Prix (Race 2)', 'Jakarta E-Prix',
            'Marrakesh E-Prix'
        ],
        'Winner': [
            'Stoffel Vandoorne', 'Nyck de Vries', 'Edoardo Mortara', 'Mitch Evans', 
            'Jean-Eric Vergne', 'Antonio Felix da Costa', 'Lucas di Grassi', 
            'Jake Dennis', 'Pascal Wehrlein', 'Stoffel Vandoorne'
        ],
        'Runner-up': [
            'Mitch Evans', 'Jake Dennis', 'Stoffel Vandoorne', 'Edoardo Mortara', 
            'Antonio Felix da Costa', 'Nyck de Vries', 'Jean-Eric Vergne', 
            'Mitch Evans', 'Edoardo Mortara', 'Pascal Wehrlein'
        ],
        'Third Place': [
            'Jean-Eric Vergne', 'Stoffel Vandoorne', 'Jean-Eric Vergne', 'Nyck de Vries',
            'Pascal Wehrlein', 'Jake Dennis', 'Stoffel Vandoorne', 'Edoardo Mortara',
            'Lucas di Grassi', 'Jake Dennis'
        ]
    }
    return pd.DataFrame(data)

# Function to apply custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Main function
def main():
    # Load custom CSS
    local_css("style.css")
    
    st.title('🏎️ Formula E Dashboard')
    st.sidebar.title('Navigation')
    
    # Sidebar options
    options = st.sidebar.radio('Select a section', ['🏁 Overview', '🏎️ Drivers', '🔧 Teams', '📊 Race Results', '📡 Live Updates'])
    
    if options == '🏁 Overview':
        st.header('Overview')
        st.write('Welcome to the Formula E Dashboard. Here you can find the latest updates, statistics, and race results.')
        driver_data = load_driver_data()
        st.dataframe(driver_data.style.set_properties(**{'background-color': 'white', 'color': 'black', 'border-color': 'grey'}))

        st.subheader('Points Distribution')
        fig, ax = plt.subplots()
        driver_data.plot(kind='bar', x='Driver', y='Points', ax=ax, color='green', edgecolor='white')
        ax.set_facecolor('grey')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.tick_params(axis='x', colors='black')
        ax.tick_params(axis='y', colors='black')
        st.pyplot(fig)

    elif options == '🏎️ Drivers':
        st.header('Drivers')
        st.write('Detailed statistics of Formula E drivers.')
        driver_data = load_driver_data()
        driver = st.selectbox('Select Driver', driver_data['Driver'])
        selected_driver_data = driver_data[driver_data['Driver'] == driver]
        st.write(selected_driver_data.style.set_properties(**{'background-color': 'white', 'color': 'black', 'border-color': 'white'}))

    elif options == '🔧 Teams':
        st.header('Teams')
        st.write('Detailed statistics of Formula E teams.')
        driver_data = load_driver_data()
        team = st.selectbox('Select Team', driver_data['Team'].unique())
        selected_team_data = driver_data[driver_data['Team'] == team]
        st.write(selected_team_data.style.set_properties(**{'background-color': 'white', 'color': 'black', 'border-color': 'white'}))

    elif options == '📊 Race Results':
        st.header('Race Results')
        st.write('Race results of recent Formula E events.')
        race_results = load_race_results()
        st.dataframe(race_results.style.set_properties(**{'background-color': 'white', 'color': 'black', 'border-color': 'white'}))

    elif options == '📡 Live Updates':
        st.header('Live Updates')
        st.write('Live updates from Formula E races.')
        st.write('Live updates functionality to be implemented...')

if __name__ == "__main__":
    main()

