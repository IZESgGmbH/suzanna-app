import streamlit as st
import pandas as pd
import altair as alt
from altair import datum
from textwrap import wrap

# Load style css
with open('style.css') as f:
	st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.header('SUZANNA-Erhebung')
st.subheader('Ergebnisse in den Handlungsfeldern')
st.html('''
<p>Innerhalb der Umfrage wurden die Teilnehmenden gebeten, aus vier Handlungsfeldern zu wählen.</p>
<ol>
<li>Wohnen und Energie</li>
<li>Ernährung und Konsum</li>
<li>Erwerbsarbeitszeit</li>
<li>Mobilität</li>
</ol>
<p>Die Verteilung der Antworten in diesen Handlungsfeldern zeigt die folgende Abbildung:</p>
''')

# Generating data for chart
data = st.session_state.df.groupby(by='HA03')['HA03'] \
    .count() \
    .reset_index(name='Anzahl') \
    .head(4)

# Generating chart
base = alt.Chart(data).encode(
    theta=alt.Theta('Anzahl:Q').stack(True),
    color=alt.Color('HA03:N', legend=alt.Legend(title='Handlungsfeld')),
    tooltip=[alt.Tooltip('HA03:N', title='Handlungsfeld:'), alt.Tooltip('Anzahl', title='Anzahl:')]
).properties(width=500, height=200)

pie = base.mark_arc(innerRadius=40, outerRadius=70)

rel = 0
if rel==1:
    # Alternative Darstellung der relativen Anteile
    label = base.mark_text(radius=85, color='black').encode(
        text=alt.Text('p:Q', format='.1%')
    ).transform_joinaggregate(total='sum(Anzahl)').transform_calculate(p='datum.Anzahl / datum.total')
else:
    label = base.mark_text(radius=85, color='black').encode(
        text=alt.Text('Anzahl:Q')
    )

st.altair_chart(pie + label)

st.html('''
<p>Für den gewählten Lebensbereich wurden den Teilnehmenden Fragen zu folgenden Aspekten gestellt:</p>
<ul>
    <li>Verhaltensweisen</li>
    <li>Zufriedenheit</li>
    <li>Klimabewusstsein</li>
    <li>Wichtige Faktoren und Bedürfnisse in Bezug auf ihre Lebensqualität</li>
    <li>Zustimmung zu handlungsspezifischen Maßnahmen</li>
</ul>
''')

st.subheader('Ergebnisse im Überblick')
st.html('<p>Die Teilnehmenden der Umfrage wurden gefragt, wie wichtig ihnen verschiedene Punkte in Bezug auf das jeweilige Handlungsfeld sind. Die Ergebnisse zeigen, dass ein Ansatz, der auf den Bedürfnissen der Menschen aufbaut, nicht nur die Lebensqualität verbessert, sondern auch Chancen für den Klimaschutz bietet.</p>')

# Defining a function to generate charts containing most important factors related to the four sectors
def generate_charts(variable, title, sector):
    data = st.session_state.df.loc[st.session_state.df['HA03']==sector, :]
    data = ['Zustimmung' if (value=='eher wichtig') | (value=='sehr wichtig') else 'keine Zustimmung' for value in data[variable]]
    data = pd.DataFrame({variable: data}) \
        .groupby(by=variable)[variable] \
        .count() \
        .reset_index(name='Anzahl')
    base = alt.Chart(data, title=alt.TitleParams(text=title, orient='bottom', fontSize=14, color='DarkMagenta')).encode(
        theta=alt.Theta('Anzahl:Q'),
        color=alt.condition(f"datum.{variable} == 'Zustimmung'", alt.value('steelblue'), alt.value(None)),
        opacity=alt.condition(f"datum.{variable} == 'Zustimmung'", alt.value(1), alt.value(0))
    ).properties(width=200, height=100)
    pie = base.mark_arc(innerRadius=40, outerRadius=70)
    label = base.mark_text(radius=0, color='black', size=17).encode(
        text=alt.Text('p:Q', format='.1%')
    ).transform_joinaggregate(total='sum(Anzahl)').transform_calculate(p='datum.Anzahl / datum.total')
    return pie, label

# Selecting sector and determining index of sector
sector = st.selectbox(label='Auswahl des Handlungsfeldes', options=st.session_state.sectors)
index_sector = st.session_state.sectors.index(sector)

st.html(f'<p>Die drei folgenden Punkte zeigen exemplarisch, welche Aspekte den Befragten im Handlungsfeld {sector} am wichtigsten sind.</p>')

# Defining irrelevant variables and starting sequence of sector variables
variables_irrelevant = ('Respondent_Serial', 'InterviewLength', 'LayoutVariante', 'H')
variables_sectors_start = ['HW', 'HK', 'HE', 'HM']

# Selecting data including selected sector and excluding variables not relevant for visualization
df_selected = pd.concat([st.session_state.df.loc[:, ~st.session_state.df.columns.str.startswith(variables_irrelevant)], st.session_state.df.loc[st.session_state.df['HA03']==sector, st.session_state.df.columns.str.startswith(variables_sectors_start[index_sector])]], axis=1, join='inner')

# Generating wrapped labels in preparation of generating exemplary charts
variables_example = pd.DataFrame({'variable': [\
    'HW10_03', 'HW10_20', 'HW10_07', \
    'HK12_14', 'HK12_02', 'HK12_04', \
    'HE09_01', 'HE09_04', 'HE09_05', \
    'HM13_04', 'HM13_10', 'HM13_13']})
variables_example['label'] = [st.session_state.meta.column_names_to_labels[key] for key in variables_example['variable']]
variables_example['label'] = variables_example['label'].apply(wrap, args=[30])
variables_example = variables_example[variables_example.variable.str.startswith(variables_sectors_start[index_sector])].reset_index(drop=True)

# Generating examplary charts dependend on the selected sector
pie_0, label_0= generate_charts(variables_example['variable'][0], variables_example['label'][0], sector)
pie_1, label_1= generate_charts(variables_example['variable'][1], variables_example['label'][1], sector)
pie_2, label_2= generate_charts(variables_example['variable'][2], variables_example['label'][2], sector)
st.altair_chart((pie_0 + label_0) | (pie_1 + label_1) | (pie_2 + label_2))

st.subheader('Ergebnisse zum Anschauen, Verändern und Vergleichen')
st.html('<p>Nachfolgend kannst Du Dir einen Überblick über die handlungsspezifischen Ergebnisse verschaffen. Dabei kannst Du zwischen einer vereinfachten und detaillierten Darstellung unterscheiden.</p>')

# Determining x variables from selection
x_variables = list(df_selected.loc[: ,(df_selected.columns.str.startswith('H')) & ~(df_selected.columns.str.contains('Codes')) & (df_selected.columns.str.len()==4)].select_dtypes(include='category').columns)

# Defining dict containing question labels not included in row data and filtering by selected sector
additional_column_labels = {'HM04': 'Verfügen Sie über ein Fahrrad?',
                            'HM12': 'Wie stark beeinflussen folgende Faktoren Ihr Mobilitätsverhalten?',
                            'HM13': 'Wie wichtig sind Ihnen darüber hinaus folgende Punkte in Bezug auf alltägliche Mobilität?',
                            'HM14': 'Was macht für Sie eine hohe Lebensqualität in Bezug auf Mobilität aus?',
                            'HM15': 'Welche Maßnahmen halten Sie für geeignet, um ökologische Auswirkungen zu verringern und trotzdem eine hohe Lebensqualität zu erzielen?',
                            'HE03': 'Arbeiten Sie darüber hinaus unbezahlt?',
                            'HE08': 'Welche der folgenden Faktoren spielen für Sie persönlich eine Rolle, wenn Sie Ihre aktuelle Jobsituation verändern möchten (z.B. Arbeitszeit oder Art der Arbeit)?',
                            'HE09': 'Welche Rolle spielen für Sie persönlich darüber hinaus folgende Punkte, wenn Sie Ihre aktuelle Jobsituation verändern möchten? (Arbeitszeit oder Art der Arbeit) ',
                            'HE10': 'Was macht für Sie eine hohe Lebensqualität in Bezug auf das Verhältnis von Arbeitszeit und Freizeit aus?',
                            'HE11': 'Welche Maßnahmen würden es Ihnen ermöglichen Ihre Arbeitszeit zu Ihrer Zufriedenheit zu verändern?',
                            'HK11': 'Wie stark beeinflussen die folgenden Faktoren Ihre Konsumentscheidungen? (kann auch die Entscheidungsein nicht zu konsumieren)',
                            'HK12': 'Wie stark beeinflussen darüber hinaus folgende Punkte Ihre Konsumentscheidungen?',
                            'HK13': 'Was macht für Sie eine hohe Lebensqualität im Bezug auf Konsum und Ernährung aus?',
                            'HK14': 'Welche Maßnahmen halten Sie für geeignet, um ökologische Auswirkungen zu verringern und dabei trotzdem eine hohe Lebensqualität zu erzielen?',
                            'HW06': 'Welche Beschreibung trifft auf Ihre Wärmeversorgung am ehesten zu? (Mehrfachnennung möglich)',
                            'HW09': 'Wie stark wirken sich die folgenden Faktoren darauf aus, wie Sie wohnen? (z.B. Wahl des Wohnortes oderder Wohnungsgröße)',
                            'HW10': 'Was ist Ihnen darüber hinaus beim Wohnen wichtig?',
                            'HW11': 'Was macht für Sie eine hohe Lebensqualität in Bezug auf Wohnen aus?',
                            'HW12': 'Welche Maßnahmen halten Sie für geeignet, um ökologische Auswirkungen zu verringern und trotzdem dabei eine hohe Lebensqualität zu erzielen?'
                            }
additional_column_labels_selected = dict(filter(lambda item: variables_sectors_start[index_sector] in item[0], additional_column_labels.items()))

# Adding the filtered additional variables to the x variables
for key, value in additional_column_labels_selected.items():
    if key not in st.session_state.meta.column_names_to_labels.keys():
        st.session_state.meta.column_names_to_labels.update({key: value})
    x_variables.append(key)
    x_variables.sort()

# Defining variables which shall not be considered furthermore
variables_excluded = ['HE13']

# Determining name of selected x variable
name_x_variable = st.selectbox(label='Auswahl der Variablen', options=[st.session_state.meta.column_names_to_labels[k] for k in x_variables if (k in st.session_state.meta.column_names_to_labels) & (k not in variables_excluded)])
x_variable = [k for k, v in st.session_state.meta.column_names_to_labels.items() if v==name_x_variable][0]
st.success('Variablenname: ' + x_variable)

# Choosing type of chart
option_simple = 'Vereinfacht'
option_detail = 'Detailliert'
type_of_chart = st.radio(label='Auswahl der Art der Abbildungen', options=[option_simple, option_detail], index=0,
                         horizontal=True, label_visibility='collapsed')

# Continuing if x variable is selected
if x_variable!=None:

    # Adding subvariables to questions with multiple answers
    x_subvariables = list(df_selected.loc[:, (df_selected.columns.str.startswith(x_variable)) & ~(
        df_selected.columns.str.contains('Codes'))].select_dtypes(include='category').columns)

    # Defining codes and captions of x variables
    x_codes = []
    x_captions = pd.DataFrame()
    for variable in x_subvariables:
        df_selected['codes_{}'.format(variable)] = df_selected[variable].cat.codes + 1
        x_codes.append('codes_{}'.format(variable))
        x_captions.loc[0, variable] = st.session_state.meta.column_names_to_labels[variable]
        x_captions = x_captions.rename(columns={variable: 'codes_{}'.format(variable)})
    df_selected['x_codes'] = df_selected[x_subvariables[0]].cat.codes
    labels_x_variables = list(st.session_state.meta.variable_value_labels[x_subvariables[0]].values())

    # Removing rows with NaN from x labels
    na_value = 'Keine Angabe'
    if na_value in labels_x_variables:
        labels_x_variables.remove(na_value)

    total_label = 'Gesamt'
    no_y_selection = 'Keine'
    filter = []
    if type_of_chart==option_detail:
        with st.expander(label='Möglichkeit für weitere Differenzierung', expanded=False):

            # Determining y variables
            y_variables = df_selected.loc[:, (df_selected.columns.isin(['SL02', 'SL03', 'SL06', 'SL08', 'SL09', 'SL10', 'SL11', 'SL13_02', 'Alter_Quote', 'Einkommen_Quote']))
                          ].select_dtypes(include='category').columns

            # Selecting y variable
            options = [st.session_state.meta.column_names_to_labels[k] for k in y_variables if
                       k in st.session_state.meta.column_names_to_labels]
            no_y_selection = 'Keine'
            options.insert(0, no_y_selection)
            name_y_variable = st.selectbox(label='Auswahl einer weiteren Variablen (optional)', options=options)
            filter = []
            if name_y_variable != no_y_selection:
                y_variable = [k for k, v in st.session_state.meta.column_names_to_labels.items() if v == name_y_variable][0]
                name_y_variable = st.session_state.meta.column_names_to_labels[y_variable]
                st.success('Variablenname: ' + y_variable)

                # Setting filter by selecting the values for grouping
                filter_options = list(df_selected[y_variable].cat.categories)
                filter_options = ["\>= 3.000 Euro" if option == '>= 3.000 Euro' else option for option in
                                  filter_options]
                filter_options.insert(0, total_label)
                if na_value in filter_options:
                    filter_options.remove(na_value)
                filter = st.segmented_control(label='Auswahl der Optionen',
                                  selection_mode='multi',
                                        options=filter_options,
                                        default=filter_options
                                        )
                filter = [">= 3.000 Euro" if option == '\>= 3.000 Euro' else option for option in filter]

    with st.expander(label='Darstellung der Ergebnisse', expanded=True):
        # Setting caption of the charts generated below
        caption = alt.Chart(x_captions).mark_text(align='left', dx=-10, size=14, fontStyle='bold', limit=400).encode(
            text=alt.Text(alt.repeat('row')),
            tooltip=alt.Tooltip(alt.repeat('row'))
        )

        # Setting help column as basis of the first chart generated below

        df_selected[total_label] = total_label

        # Setting help variable to remove rows with NaN while creating charts
        if x_variable == x_subvariables[0]:
            subset = x_variable
        else:
            subset = total_label

        # Setting variables including the scale and legend labels within the charts generated below
        x_labels = '{}[datum.value]'.format(st.session_state.meta.variable_value_labels[x_subvariables[0]])
        x_keys = list(range(1, len(labels_x_variables)+1))

        # Creating first chart showing total counts for the selected variable
        if type_of_chart == option_detail:
            if name_y_variable == no_y_selection:
                altair_chart_total = alt.Chart(df_selected.dropna(subset=subset)).mark_bar().encode(
                    y=alt.Y(total_label, type='nominal', axis=alt.Axis(title='')),
                    x=alt.X(alt.repeat('row'), aggregate='count').stack('normalize').title(None),
                    color=alt.Color(alt.repeat('row'),
                                    scale=alt.Scale(scheme='redyellowblue',
                                                    reverse=True,
                                                    domain=x_keys),
                                    legend=alt.Legend(title=f'Variable {x_variable}',
                                                      labelExpr=x_labels)
                                    ),
                    tooltip=[alt.Tooltip(alt.repeat('row'), aggregate='count', title='Anzahl:')]
                    )

                # Joining caption and chart
                altair_chart = (caption & altair_chart_total).repeat(row=x_codes)

            # Creating second chart showing counts for the selected variable grouped by the variable for grouping
            else:
                altair_chart_total = alt.Chart(df_selected[df_selected[total_label].isin(filter)].dropna(subset=subset)).mark_bar().encode(
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

                altair_chart_grouped = alt.Chart(df_selected[df_selected[y_variable].isin(filter)].dropna(subset=subset)).mark_bar().encode(
                    y=alt.Y(y_variable, type='nominal', sort=df_selected[y_variable].cat.categories),
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
        else:
            # Changing items shown
            options=list(st.session_state.meta.variable_value_labels[x_subvariables[0]].values())
            na_value = 'Keine Angabe'
            if na_value in options:
                options.remove(na_value)
            options=options[::-1]
            if int((len(options) + 1) / 2 - 2) > 0:
                end_index = int((len(options) + 1) / 2 - 2)
            elif len(options) == 2:
                end_index = 0
            else:
                end_index = 1
            if x_variable in ['HW03', 'HE04', 'HM05', 'HM06']:
                items = st.segmented_control(label='Auswahl des Milieus',
                                         selection_mode='multi',
                                         options=options,
                                         default=options[2:4]
                                         )
                colors = []
                for item in options:
                    if item in items:
                        colors.insert(0, 'steelblue')
                    else:
                        colors.insert(0, 'lightgrey')
            else:
                start_item, end_item = st.select_slider(label='Kategorie',
                                         options=options,
                                         value=(options[0], options[end_index]),
                                         label_visibility='hidden')
                colors = []
                for i in range(len(options)):
                    if (i >= options.index(start_item)) & (i <= options.index(end_item)):
                        colors.insert(0, 'steelblue')
                    else:
                        colors.insert(0, 'lightgrey')

            altair_chart_total = alt.Chart(df_selected.dropna(subset=subset)).mark_bar().encode(
                x=alt.X(alt.repeat('row'), aggregate='count').stack('normalize').sort('descending').axis(None).title(None),
                color=alt.Color(alt.repeat('row'),
                                scale=alt.Scale(range=colors,
                                                  reverse=False,
                                                  domain=x_keys),
                                legend=None
                                ),
                tooltip=[alt.Tooltip(alt.repeat('row'), aggregate='count', title='Anzahl:')]
            )

            # Joining caption and chart
            altair_chart = (caption & altair_chart_total).repeat(row=x_codes)

        # Calculating space between caption and chart
        if total_label in filter:
            spacing = 10
        else:
            spacing = 5

        # Displaying joined charts
        st.altair_chart(alt.vconcat(altair_chart).configure_concat(spacing=spacing))