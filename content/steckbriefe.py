import streamlit as st
import pandas as pd

# Load style css
with open('style.css') as f:
	st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Defining function for loading data
@st.cache_data
def load_excel(excel_path):
	df = pd.read_excel(excel_path, index_col=0)
	return(df)

# Defining function to insert field contents of excel data
def insert(col, title=None, expanded=True):
	if data_option[col].values[0]!='leer':
		if title==None:
			title=col
		with st.expander(label=title, expanded=expanded):
			st.html(data_option[col].values[0])

st.header('Steckbriefe')
st.subheader('Suffizienzfördernde Dienstleistungsangebote')
st.html('''
<p>Die Steckbriefe bieten einen systematischen Überblick über bestehende suffizienzfördernde Angebote auf Basis folgender Fragestellungen:</p>
<ol>
	<li>Wie können suffiziente Lebensweisen in verschiedenen Bevölkerungsgruppen durch Dienstleistungsangebote unterstüzt werden?</li>
	<li>Wie sich hierzu die heute bestehenden Dienstleistungsangebote in den Bereichen Wohnen, Mobilität und Konsum verändern müssten?</li>
	<li>Was sind die fördernden und hemmenden Rahmenbedingungen bei der Umsetzung suffizienzförderender Dienstleistungsangebote?</li>
</ol>
<p>Auf Basis einer Literaturrechereche wurden bestehende suffizienzorientierte Dienstleistungsangebote in den Bereichen Wohnen, Mobilität und Konsum systematisch erfasst und den Lebensbildern zugeordnet, die sich aus der Befragung ergeben. Zudem wurden relevante Anbieter und weitere Akteure identifiziert. Politische und regulatorische Rahmenbedingungen, die diese Angebote beeinflussen wurden ebenfalls berücksichtigt.
Zur Bewertung und Weiterentwicklung dieser Angebote wurden deren Potenziale zur Förderung suffizienzorientierten Verhaltens sowie die Potenziale für die weitere Verbreitung analysiert.</p>
''')

with st.expander('Definition: Suffizienzbegünstigendes Dienstleistungsangebot'):
	st.html('''
	<p>Ein <b>Dienstleistungsangebot</b> besteht aus den spezifischen Dienstleistungen, die eine Organisation, wie z.B. ein privates Unternehmen, einen Kommune oder eine andere öffentliche Einrichtung, ihren Bürger*innen und Kunden anbietet.</p>
	<p>Für das Projekt SUZANNA betrachten wir die suffizienzorientierten Dienstleistungsangebote, die durch die Gestaltung der Außenbedingungen eine suffizienzte Verhaltensweise ermöglichen und fördern und damit den Ressourcenverbrauch reduzieren.</p>
	<p>Die betrachteten Dienstleistungen können in drei Kategorien unterteilt werden:</p>
	<ul>
		<li>Öffentliche Dienstleistungen</li>
		<li>Individuell oder kollektiv initiierte, freiwillige Angebote</li>
		<li>Unternehmensgeführte Angebote</li>
	</ul>
	''')

# Loading data
measures = load_excel('data/measures.xlsx')

# Selecting sector and determining index of sector
sectors_selection = st.session_state.sectors.copy()
item_to_remove = 'Erwerbsarbeitszeit'
if item_to_remove in sectors_selection:
	sectors_selection.remove(item_to_remove)
sector = st.selectbox(label='Auswahl des Sektors', options=sectors_selection)

# Filtering data by sector
measures_selected = measures[measures['Handlungsfeld']==sector]

# Selecting option
option = st.selectbox(label='Auswahl des Steckbriefs', options=list(measures_selected['Ansatz']))

# Filtering data by option
data_option = measures_selected[measures_selected['Ansatz']==option]

# Arranging field contents of excel data in two columns
st.info('Beschreibung')
#col1, col2 = st.columns(2)
#with col1:
insert('Cluster', 'Maßnahmen-Cluster')
insert('Definition')
insert('Variante', 'Varianten', expanded=False)
#with col2:
insert('Anbietendenstruktur', 'Anbietenden- und Angebotsstruktur')
insert('Akteure', 'Weitere Akteure', expanded=False)
insert('Beispiele')
st.info('Politische und regulatorische Rahmenbedingungen')
#col1, col2 = st.columns(2)
#with col1:
insert('Gesetz', 'Gesetze')
#with col2:
insert('Foerderung', 'Förderungen und Subventionen')

st.info('Potenzial zur Förderung suffizienzorientierten Verhaltens')
#col1, col2 = st.columns(2)
#with col1:
insert('Perspektive', 'Perspektive für Suffizienz')

#with col2:
insert('Nutzungsgruppe', 'Nutzungsgruppen')
insert('Ansatzgebiete')
insert('Zielgruppe', 'Potenzielle Zielgruppen')
insert('Potenzial', 'Potenzial für weitere Verbreitung', expanded=False)

insert('Quellen', expanded=False)