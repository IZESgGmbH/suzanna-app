import streamlit as st
import pandas as pd
import pyreadstat

# Setting and configuring pages
p1 = st.Page('content/die-app.py', title='Die App')
p2 = st.Page('content/das-projekt.py', title='Das SUZANNA-Projekt')
p3 = st.Page('content/projektinformationen.py', title='Weitere Projektinformationen')
p4 = st.Page('content/ergebnisse-allgemein.py', title='Allgemein')
p5 = st.Page('content/ergebnisse-spezifisch.py', title='Handlungsfelder')
p6 = st.Page('content/ergebnisse-milieus.py', title='Milieus')
p7 = st.Page('content/steckbriefe.py', title='Steckbriefe')

pg = st.navigation({
	'Hintergrund': [p1, p2, p3],
	'Ergebnisse der Befragung': [p4, p5, p6],
	'Suffizienzfördernde Angebote': [p7]
})

# Configuring the default settings of the page
st.set_page_config(page_title='Suzanna',
				   page_icon=':material/edit:')

# Inserting logo
st.logo('images/logo.png', size='large')

# Information in sidebar
st.sidebar.html('<small><em>Letzte Aktualisierung: Januar 2025</em></small>')

# Defining function for loading data
@st.cache_data
def load_data(data_path):
	df, meta = pyreadstat.read_sav(data_path, apply_value_formats=True, formats_as_ordered_category=True)
	return(df, meta)

# Loading data
if 'df' not in st.session_state:
	st.session_state['df1'], st.session_state['meta'] = load_data('data/part1_file.sav')
	st.session_state['df2'], st.session_state['meta'] = load_data('data/part2_file.sav')
	st.session_state['df'] = pd.concat([st.session_state.df1, st.session_state.df2], ignore_index=True)

	# Changing label for sector mobility
	st.session_state.df.HA03 = ['Mobilität' if value.startswith('Mobilität') else value for value in st.session_state.df.HA03]

	# Adjusting keys of certain meta data
	for v in ['HM04_01', 'HE03_01', 'HW06_01']:
		st.session_state.meta.variable_value_labels[v] = {1.0: 'Nein', 2.0: 'Ja'}

	# Setting variable 'SL13'
	st.session_state.df.insert(st.session_state.df.columns.get_loc('SL13_01'), 'SL13',
							   ['Ja' if x == 'Nein' else 'Nein' for x in st.session_state.df['SL13_01']])
	st.session_state.df['SL13'] = pd.Categorical(st.session_state.df['SL13'], categories=['Nein', 'Ja'], ordered=True)
	column_names_to_labels = dict(list(st.session_state.meta.column_names_to_labels.items())[
								  :list(st.session_state.meta.column_names_to_labels).index('SL13_01')])
	column_names_to_labels.update({'SL13': 'Haben Sie Kinder?'})
	column_names_to_labels.update(dict(list(st.session_state.meta.column_names_to_labels.items())[
									   list(st.session_state.meta.column_names_to_labels).index('SL13_01'):(
												   len(list(st.session_state.meta.column_names_to_labels)) + 1)]))
	st.session_state.meta.column_names_to_labels = column_names_to_labels

	# Changing labels of variables
	column_names_to_labels.update({'Alter_Quote': 'Wie alt sind Sie?'})
	column_names_to_labels.update({'Einkommen_Quote': 'Welcher Einkommensklasse (netto) können Sie zugeordnet werden?'})
	column_names_to_labels.update({'SL12_01': 'Sind Sie in Leiharbeit?'})
	column_names_to_labels.update({'SL12_02': 'Sind Sie befristet angestellt?'})
	column_names_to_labels.update({'SL12_03': 'Arbeiten Sie auf Honorarbasis?'})
	column_names_to_labels.update({'SL12_04': 'Würden Sie Ihre soziale Absicherung als mangelhaft bezeichnen?'})
	column_names_to_labels.update({'SL12_05': 'Würden Sie sagen, dass Sie nur geringe Aufstiegschancen im Job haben?'})
	column_names_to_labels.update({'SL12_06': 'Arbeiten Sie räumlich getrennt von Ihrer Familie?'})
	column_names_to_labels.update({'SL12_07': 'Haben Sie mehrere Jobs?'})

	column_names_to_labels.update({'SL02': 'Geschlecht'})
	column_names_to_labels.update({'SL03': 'Schulabschluss'})
	column_names_to_labels.update({'SL06': 'Größenklasse des Wohnortes'})
	column_names_to_labels.update({'SL08': 'Migrationserfahrung'})
	column_names_to_labels.update({'SL09': 'Erwerbstätigkeit'})
	column_names_to_labels.update({'SL10': 'Selbstständigkeit'})
	column_names_to_labels.update({'SL11': 'Arbeitszeitmodell'})
	column_names_to_labels.update({'SL13_02': 'Minderjährige Kinder'})
	column_names_to_labels.update({'Alter_Quote': 'Altersklasse'})
	column_names_to_labels.update({'Einkommen_Quote': 'Haushaltseinkommensgruppe'})

	column_names_to_labels.update({'HA03': 'Lebensbereiche, wo Veränderungen am ehesten vorstellbar sind'})
	column_names_to_labels.update({'HW09': 'Wie stark wirken sich die folgenden Faktoren darauf aus, wie Sie wohnen?'})
	column_names_to_labels.update({'HW10': 'Was ist Ihnen darüber hinaus beim Wohnen wichtig?'})
	column_names_to_labels.update({'HW11': 'Was macht für Sie eine hohe Lebensqualität in Bezug auf Wohnen aus?'})
	column_names_to_labels.update({'HW12': 'Welche Maßnahmen halten Sie für geeignet, um ökologische Auswirkungen zu verringern und trotzdem dabei eine hohe Lebensqualität zu erzielen?'})
	column_names_to_labels.update({'HM12': 'Wie stark beeinflussen folgende Faktoren Ihr Mobilitätsverhalten?'})
	column_names_to_labels.update({'HM13': 'Wie wichtig sind Ihnen darüber hinaus folgende Punkte in Bezug auf alltägliche Mobilität?'})
	column_names_to_labels.update({'HM14': 'Was macht für Sie eine hohe Lebensqualität in Bezug auf Mobilität aus?'})
	column_names_to_labels.update({'HM15': 'Welche Maßnahmen halten Sie für geeignet, um ökologische Auswirkungen zu verringern und trotzdem eine hohe Lebensqualität zu erzielen?'})
	column_names_to_labels.update({'HK11': 'Wie stark beeinflussen die folgenden Faktoren Ihre Konsumentscheidungen?'})
	column_names_to_labels.update({'HK12': 'Wie stark beeinflussen darüber hinaus folgende Punkte Ihre Konsumentscheidungen?'})
	column_names_to_labels.update({'HK13': 'Was macht für Sie eine hohe Lebensqualität im Bezug auf Konsum und Ernährung aus?'})
	column_names_to_labels.update({'HK14': 'Welche Maßnahmen halten Sie für geeignet, um ökologische Auswirkungen zu verringern und dabei trotzdem eine hohe Lebensqualität zu erzielen?'})
	column_names_to_labels.update({'HE08': 'Welche der folgenden Faktoren spielen für Sie persönlich eine Rolle, wenn Sie Ihre aktuelle Jobsituation verändern möchten?'})
	column_names_to_labels.update({'HE09': 'Welche Rolle spielen für Sie persönlich darüber hinaus folgende Punkte, wenn Sie Ihre aktuelle Jobsituation verändern möchten?'})
	column_names_to_labels.update({'HE10': 'Was macht für Sie eine hohe Lebensqualität in Bezug auf das Verhältnis von Arbeitszeit und Freizeit aus?'})
	column_names_to_labels.update({'HE11': 'Welche Maßnahmen würden es Ihnen ermöglichen Ihre Arbeitszeit zu Ihrer Zufriedenheit zu verändern?'})

	column_names_to_labels.update({'MP03': 'Selbstbestimmung'})

# Defining sector labels
if 'sectors' not in st.session_state:
    st.session_state['sectors'] = ['Wohnen und Energie',
								   'Ernährung und Konsum',
								   'Erwerbsarbeitszeit',
								   'Mobilität']

# Executing page
pg.run()
