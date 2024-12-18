import streamlit as st
import pandas as pd
import altair as alt
from altair import datum

# Load style css
with open('style.css') as f:
	st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Defining function for loading data
@st.cache_data
def load_excel(excel_path):
	df = pd.read_excel(excel_path)
	return(df)

st.header('SUZANNA-Erhebung')
st.subheader('Milieuspezifische Ergebnisse')

st.html('<p>In SUZANNA werden auf Basis einer Clusteranalyse der repräsentativen Befragungsdaten verschiedene Suffizienz-Milieus identifiziert. Diese verdeutlichen die Gemeinsamkeiten sozialer Gruppen im Hinblick auf sozialstrukturelle Merkmale, Zufriedenheit, Einstellungen, Praktiken und Bedürfnisse.</p>')
with st.expander(label='Methode: Clusteranalyse', expanded=False):
    st.html('''
    <p>Ziel der Clusteranalyse ist es, Strukturen in den Daten zu identifizieren. Die Untersuchungsobjekte, in diesem Fall die befragten Personen, werden basierend auf ihren Eigenschaften zu Clustern zusammengefasst. In unserem Fall haben wir die Metrik „Gower’s Distance“ verwendet. Der Algorithmus berechnet die standardisierte Distanz als Summe aller variablenspezifischen Distanzen zwischen zwei Befragten und gruppiert die Personen anschließend hierarchisch nach ihrer Ähnlichkeit.</p>
    <p>Für die hier durchgeführte Clusteranalyse werden je nach Handlungsfelder 21 bis 25 Variablen berücksichtigt. Dazu zählen soziale Faktoren inkl. Quotenmerkmale, Migrationshintergrund und die Frage nach minderjährigen Kindern, sowie soziale Praktiken in verschiedenen Lebensbereichen. Zusätzlich wurden Faktoren, wie Umweltbewusstsein, Suffizienzbereitschaft, Lebenszufriedenheit und verschiedene Wertvorstellungen, gebildet und als Grundlage für die Analyse verwendet.</p>
    ''')

# Loading additional data
cluster_rec = load_excel('data/cluster_records.xlsx')
milieus = load_excel('data/cluster_description.xlsx')

# Merging additional data with original data frame
df = pd.merge(st.session_state.df, cluster_rec, on='Respondent_Serial')

# Selecting sector and determining index of sector
sector = st.selectbox(label='Auswahl des Handlungsfeldes', options=st.session_state.sectors)
index_sector = st.session_state.sectors.index(sector)

# Defining irrelevant variables and starting sequence of sector variables
variables_irrelevant = ('Respondent_Serial', 'InterviewLength', 'LayoutVariante', 'H')
variables_sectors_start = ['HW', 'HK', 'HE', 'HM']

# Selecting data including selected sector and excluding variables not relevant for visualization
df_selected = pd.concat([df.loc[:, ~df.columns.str.startswith(variables_irrelevant)], df.loc[st.session_state.df['HA03']==sector, df.columns.str.startswith(variables_sectors_start[index_sector])]], axis=1, join='inner')
milieus_selected = milieus.loc[milieus['Handlungsfeld']==sector, :]

# Showing table with selected milieus
table_milieus_selected = milieus_selected.loc[:, milieus.columns.isin(['Nr', 'Name', 'Anzahl'])].set_index('Nr')
table_milieus_selected.insert(0, 'Milieu', variables_sectors_start[index_sector][1] + table_milieus_selected.index.astype(str))
st.table(table_milieus_selected)
index_milieu_not_relevant = 0
if sector == 'Wohnen und Energie':
    st.html('<small>&ast; Das Milieu der Unzufriedenen wird aufgrund der geringen Anzahl an Personen nicht weiter betrachtet.</small>')
    index_milieu_not_relevant = milieus_selected.loc[milieus_selected['Name']=='Die Unzufriedenen*', 'Nr'].values[0]
    milieus_selected = milieus_selected.loc[milieus_selected['Name']!='Die Unzufriedenen*',:]

st.html('<p>Die Ergebnisse kannst du im Folgenden genauer betrachten. Wähle eines der Milieus aus und siehe Dir die Beschreibungen anhand der Variablen der Clusteranalyse an.</p><p>In einer detaillierteren Ansicht erfährst Du außerdem, wie sich die Zustimmungen zu den wichtigsten Faktoren und Bedürfnissen zwischen den verschiedenen Milieus unterscheiden und wie die Milieus die unterschiedlichen Maßnahmenvorschläge bewerten.</p>')

# Determining milieu from selection
milieu = st.selectbox(label='Auswahl des Milieus', options=milieus_selected['Name'])
index_milieu = table_milieus_selected[table_milieus_selected['Name'] == milieu].index[0]

# Inserting an expander to describe the milieus
with st.expander(label='Beschreibung der Milieus', expanded=False):

    # Filtering data by milieu
    data_option = milieus_selected[milieus_selected['Name']==milieu]

    # Arranging field contents of excel data
    st.html('<b>Soziale Lage</b>')
    st.html(data_option['Soziale Lage'].values[0])

    st.html('<b>Praktizierter Lebensstil</b>')
    st.html(data_option['Praktizierter Lebensstil'].values[0])

    st.html('<b>Wertvorstellung & Umweltbewusstsein</b>')
    st.html(data_option['Wertvorstellung & Umweltbewusstsein'].values[0])
    selection = 'MP04_mean'
    label = 'Umweltbewusstsein'
    left = alt.Chart(df_selected).mark_bar().encode(
        alt.X('Milieu:N'),
        alt.Y(f'mean({selection}):Q', scale=alt.Scale(domain=[1, 10]), axis=alt.Axis(values=[1,2,3,4,5])).title(None),
        color=alt.condition(f'{alt.datum.Milieu}=={index_milieu}', alt.value('steelblue'), alt.value('lightgray'))
    ).transform_filter(f'datum.Milieu!={index_milieu_not_relevant}'
    ).properties(height=150, title=label)
    selection = 'PZ03_mean'
    label = 'Suffizienzbereitschaft'
    middle = alt.Chart(df_selected).mark_bar().encode(
        alt.X('Milieu:N'),
        alt.Y(f'mean({selection}):Q', scale=alt.Scale(domain=[1, 10]), axis=alt.Axis(values=[1,2,3,4,5])).title(None),
        color=alt.condition(f'{alt.datum.Milieu}=={index_milieu}', alt.value('steelblue'), alt.value('lightgray'))
    ).transform_filter(f'datum.Milieu!={index_milieu_not_relevant}'
    ).properties(height=150, title=label)
    selection_variable = ['HW07', 'HK09', 'HE05', 'HM10'][index_sector]
    selection = f'{selection_variable}_factorized'
    if selection not in df_selected.columns:
        df_selected[selection] = df_selected[selection_variable].factorize(sort=True)[0] + 1
    label = 'Klimabewusstsein'
    right = alt.Chart(df_selected).mark_bar().encode(
        alt.X('Milieu:N'),
        alt.Y(f'mean({selection}):Q', scale=alt.Scale(domain=[1, 10])).title(None),
        color=alt.condition(f'{alt.datum.Milieu}=={index_milieu}', alt.value('steelblue'), alt.value('lightgray'))
    ).transform_filter(f'datum.Milieu!={index_milieu_not_relevant}'
    ).properties(height=150, title=label)
    st.altair_chart(alt.hconcat(left, middle, right).configure_title(anchor='middle', color='DarkMagenta', fontSize=15))

    st.html('<b>Zufriedenheit</b>')
    st.html(data_option['Zufriedenheit'].values[0])
    label = 'Lebenssituation'
    left = alt.Chart(df_selected).mark_bar().encode(
        alt.X('Milieu:N'),
        alt.Y('mean(MT02_mean):Q', scale=alt.Scale(domain=[1, 10]), axis=alt.Axis(values=[1,2,3,4,5,6,7])).title(None),
        color=alt.condition(f'{alt.datum.Milieu}=={index_milieu}', alt.value('steelblue'), alt.value('lightgray'))
    ).transform_filter(f'datum.Milieu!={index_milieu_not_relevant}'
    ).properties(height=150, title=label)
    selection_variable = ['HW13', 'HK15', 'HE12', 'HM16'][index_sector]
    selection = f'{selection_variable}_factorized'
    if selection not in df_selected.columns:
        df_selected[selection] = df_selected[selection_variable].factorize(sort=True)[0] + 1
    label = ['Wohnsituation', 'Konsum und Ernährung', 'Arbeitszeit und Privatleben', 'Mobilität'][index_sector]
    right = alt.Chart(df_selected).mark_bar().encode(
        alt.X('Milieu:N'),
        alt.Y(f'mean({selection}):Q', scale=alt.Scale(domain=[1, 10])).title(None),
        color=alt.condition(f'{alt.datum.Milieu}=={index_milieu}', alt.value('steelblue'), alt.value('lightgray'))
    ).transform_filter(f'datum.Milieu!={index_milieu_not_relevant}'
    ).properties(height=150, title=label)
    st.altair_chart(alt.hconcat(left, right).configure_title(anchor='middle', color='DarkMagenta', fontSize=15))

    st.html('<b>Suffizienzorientierung im Handlungsfeld</b>')
    st.html('Die Suffizienzorientiertung zeigt an, wie hoch die Bereitschaft ist, suffizienzunterstützende Angebote anzunehmen, und welche äußeren Faktoren bestehen, die eine solche Entscheidung beeinflussen.')
    label = 'Suffizienzbereitschaft'
    selection = ['HW10_mean', 'HK12_mean', 'HE09_mean', 'HM13_mean'][index_sector]
    left = alt.Chart(df_selected).mark_bar().encode(
        alt.X('Milieu:N'),
        alt.Y(f'mean({selection}):Q', scale=alt.Scale(domain=[1, 5])).title(None),
        color=alt.condition(f'{alt.datum.Milieu}=={index_milieu}', alt.value('steelblue'), alt.value('lightgray'))
    ).transform_filter(f'datum.Milieu!={index_milieu_not_relevant}'
    ).properties(height=150, title=label)
    label = 'Suffizienzbedürfnisse'
    selection = ['HW11_mean', 'HK13_mean', 'HE10_mean', 'HM14_mean'][index_sector]
    right = alt.Chart(df_selected).mark_bar().encode(
        alt.X('Milieu:N'),
        alt.Y(f'mean({selection}):Q', scale=alt.Scale(domain=[1, 5])).title(None),
        color=alt.condition(f'{alt.datum.Milieu}=={index_milieu}', alt.value('steelblue'), alt.value('lightgray'))
    ).transform_filter(f'datum.Milieu!={index_milieu_not_relevant}'
    ).properties(height=150, title=label)
    st.altair_chart(alt.hconcat(left, right).configure_title(anchor='middle', color='DarkMagenta', fontSize=15))

# Inserting an expander to describe the milieus additionally
with st.expander(label='Detaillierte Darstellung: Einflussfaktoren, Bedürfnisse und Maßnahmen sowie deren Relevanz', expanded=True):

    # Choosing type of chart
    option_simple = 'Vereinfacht'
    option_detail = 'Detailliert'
    type_of_chart= st.radio(label='Auswahl der Art der Abbildungen', options=[option_simple, option_detail], index=0, horizontal=True, label_visibility='collapsed')

    # Determining x variables from selection
    x_variables = [x for x in ['HW09', 'HW10', 'HW11', 'HW12', 'HM12', 'HM13', 'HM14', 'HM15', 'HK11', 'HK12', 'HK13', 'HK14', 'HE08', 'HE09', 'HE10', 'HE11'] if x .startswith(variables_sectors_start[index_sector])]

    # Determining name of selected x variable
    sector_desc = ['Wohn', 'Konsum', 'Arbeits', 'Mobilitäts'][index_sector]
    options = [f'Einflussfaktoren aufs {sector_desc}verhalten', 'Zusätzlich wichtige Faktoren', 'Faktoren für eine hohe Zufriedenheit', 'Angebote und Maßnahmen']
    selection = st.selectbox(label='Auswahl der Variablen', options=options)
    x_variable = x_variables[options.index(selection)]
    name_x_variable = [v for k, v in st.session_state.meta.column_names_to_labels.items() if k==x_variable][0]
    st.success(x_variable + ': ' + name_x_variable)

    # Continuing if x variable is selected
    if x_variable!=None:

        # Adding subvariables to questions with multiple answers
        x_subvariables = list(df_selected.loc[:, (df_selected.columns.str.startswith(x_variable)) & ~(
            df_selected.columns.str.contains('Codes'))].select_dtypes(include='category').columns)

        # Defining codes and captions of x variables
        x_codes = []
        x_captions = pd.DataFrame()
        for variable in x_subvariables:
            df_selected['codes_{}'.format(variable)] = df_selected[variable].cat.codes+1
            x_codes.append('codes_{}'.format(variable))
            x_captions.loc[0, variable] = st.session_state.meta.column_names_to_labels[variable]
            x_captions = x_captions.rename(columns={variable: 'codes_{}'.format(variable)})
        if x_subvariables:
            df_selected['x_codes'] = df_selected[x_subvariables[0]].cat.codes
            labels_x_variables = list(st.session_state.meta.variable_value_labels[x_subvariables[0]].values())

            # Removing rows with NaN from x labels
            na_value = 'Keine Angabe'
            if na_value in labels_x_variables:
                labels_x_variables.remove(na_value)

        # Setting caption of the charts generated below
        caption = alt.Chart(x_captions).mark_text(align='left', dx=-10, size=14, fontStyle='bold', limit=400).encode(
            text=alt.Text(alt.repeat('row')),
            tooltip=alt.Tooltip(alt.repeat('row'))
        )

        # Setting empty line
        empty_line = alt.Chart(None).mark_text().encode()

        # Setting help column as basis of the first chart generated below
        total_label = 'Ø'
        df_selected[total_label] = total_label

        # Setting help variable to remove rows with NaN while creating charts
        if x_variable == x_subvariables[0]:
            subset = x_variable
        else:
            subset = total_label

        # Setting variables including the scale and legend labels within the charts generated below
        x_labels = '{}[datum.value]'.format(st.session_state.meta.variable_value_labels[x_subvariables[0]])
        x_keys = list(range(1, len(labels_x_variables)+1))

        # Continuing if simple option is chosen
        if type_of_chart == option_simple:

            # Changing items shown
            options=['5: Starke Zustimmung', '4: Zustimmung', '3: Neutral', '2: Ablehnung', '1: Starke Ablehnung']
            if int((len(options) + 1) / 2 - 2)>0:
                end_index = int((len(options) + 1) / 2 - 2)
            start_item, end_item = st.select_slider(label='Kategorie',
                                     options=options,
                                     value=(options[0], options[end_index]),
                                     label_visibility='hidden'
                                     )
            colors = []
            for i in range(len(options)):
                if (i >= options.index(start_item)) & (i <= options.index(end_item)):
                    colors.insert(0, 'steelblue')
                else:
                    colors.insert(0, 'lightgrey')

            # Selecting milieus shown
            filter_options = list(milieus_selected['Nr'])
            filter_options.insert(0, total_label)
            filter = st.segmented_control(label='Auswahl des Milieus',
                                         selection_mode='multi',
                                         options=filter_options,
                                         default=index_milieu
                                         )

            # Creating first chart showing total counts for the selected variable
            altair_chart_total = alt.Chart(df_selected[df_selected[total_label].isin(filter)]).mark_bar().encode(
                y=alt.Y(total_label, type='nominal', axis=alt.Axis(title='')),
                x=alt.X(alt.repeat('row'), aggregate='count').stack('normalize').sort('descending').axis(None).title(None),
                color=alt.Color(alt.repeat('row'),
                                scale=alt.Scale(range=colors,
                                                reverse=False,
                                                domain=x_keys),
                                legend=None
                                ),
                tooltip=[alt.Tooltip(alt.repeat('row'), type='ordinal', title='Kategorie'),
                         alt.Tooltip(alt.repeat('row'), aggregate='count', title='Anzahl:')]
            )

            altair_chart_grouped = alt.Chart(df_selected[df_selected['Milieu'].isin(filter)]).mark_bar().encode(
                y=alt.Y('Milieu', type='nominal'),#, axis=alt.Axis(titleAngle=0),
                x=alt.X(alt.repeat('row'), aggregate='count').stack('normalize').sort('descending').axis(None).title(None),
                color=alt.Color(alt.repeat('row'),
                                scale=alt.Scale(range=colors,
                                                  reverse=False,
                                                  domain=x_keys),
                                legend=None
                                ),
                tooltip=[alt.Tooltip(alt.repeat('row'), type='ordinal', title='Kategorie:'),
                         alt.Tooltip(alt.repeat('row'), type='quantitative', aggregate='count', title='Anzahl:')]
            )

            # Joining caption and charts
            altair_chart = (caption & altair_chart_total & altair_chart_grouped & empty_line).repeat(row=x_codes)

            # Displaying joined charts
            st.altair_chart(alt.vconcat(altair_chart).configure_concat(spacing=0))

        else:
            # Creating first chart showing total counts for the selected variable
            altair_chart_total = alt.Chart(df_selected).mark_bar().encode(
                y=alt.Y(total_label, type='nominal', axis=alt.Axis(title='')),
                x=alt.X(alt.repeat('row'), aggregate='count').stack('normalize').axis(None).title(None),
                color=alt.Color(alt.repeat('row'),
                                scale=alt.Scale(scheme='redyellowblue',
                                                reverse=True,
                                                domain=x_keys),
                                legend=alt.Legend(title=f'Variable {x_variable}',
                                                labelExpr=x_labels)
                                ),
                tooltip=[alt.Tooltip(alt.repeat('row'), aggregate='count', title='Anzahl:')]
            )

            altair_chart_grouped = alt.Chart(df_selected).mark_bar().encode(
                y=alt.Y('Milieu', type='nominal'),
                x=alt.X(alt.repeat('row'), aggregate='count').stack('normalize').title(None),
                color=alt.Color(alt.repeat('row'),
                                scale=alt.Scale(scheme='redyellowblue',
                                                  reverse=True,
                                                  domain=x_keys),
                                legend=alt.Legend(title=f'Variable {x_variable}',
                                                labelExpr=x_labels)
                                ),
                tooltip=[alt.Tooltip(alt.repeat('row'), type='quantitative', aggregate='count', title='Anzahl:')]
            )

            # Joining caption and charts
            altair_chart = (caption & altair_chart_total & altair_chart_grouped).repeat(row=x_codes)

            # Displaying joined charts
            st.altair_chart(alt.vconcat(altair_chart).configure_concat(spacing=12))