import streamlit as st
import pandas as pd
import altair as alt
from altair import datum
from textwrap import wrap

# Load style css
with open('style.css') as f:
	st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.header('SUZANNA-Erhebung')
st.subheader('Grundeinstellungen für ein gutes Leben')
st.html('''
<p>Im allgemeinen Teil der Befragung wurden die Faktoren abgefragt, die ein gutes Leben ausmachen, sowie die dahinterliegenden Wertvorstellungen. Zudem hat uns interessiert, wie groß die Bereitschaft in der Gesellschaft ist, das Verhalten zu ändern und einen nachhaltigeren Lebensstil zu verfolgen, und was die Gründe sind, die einem nachhaltigen Lebensstil im Wege stehen.</p>
<p>Generell zeigen die Ergebnisse der Untersuchung ein ausgeprägtes Umweltbewusstsein in der deutschen Bevölkerung und dass eine grundsätzliche Bereitschaft für suffizientes Verhalten vorhanden ist.</p>
<p>Folgende Punkte haben in der Befragung die höchste Zustimmung, wenn es darum geht, suffizient zu sein.</p>
''')

# Copying data
df_selected = st.session_state.df

# Defining a function to generate charts containing most important factors related to the four sectors
def generate_charts(variable, title):
    data = df_selected
    data = ['Zustimmung' if (value=='trifft eher zu') | (value=='trifft voll zu') else 'keine Zustimmung' for value in data[variable]]
    data = pd.DataFrame({variable: data}) \
        .groupby(by=variable)[variable] \
        .count() \
        .reset_index(name='Anzahl')
    base = alt.Chart(data, title=alt.TitleParams(text=title, orient='bottom', fontSize=14, color='DarkMagenta')).encode(
        theta=alt.Theta('Anzahl:Q'),
        color=alt.condition(f"datum.{variable} == 'Zustimmung'", alt.value('steelblue'), alt.value(None)),
        opacity=alt.condition(f"datum.{variable} == 'Zustimmung'", alt.value(1), alt.value(0))
    ).properties(width=150, height=100)
    pie = base.mark_arc(innerRadius=40, outerRadius=70)
    label = base.mark_text(radius=0, color='black', size=17).encode(
        text=alt.Text('p:Q', format='.1%')
    ).transform_joinaggregate(total='sum(Anzahl)').transform_calculate(p='datum.Anzahl / datum.total')
    return pie, label

# Generating wrapped labels in preparation of generating exemplary charts
variables_example = pd.DataFrame({'variable': ['PZ03_07', 'PZ03_06', 'PZ03_09', 'PZ03_01']})
variables_example['label'] = [st.session_state.meta.column_names_to_labels[key] for key in variables_example['variable']]
variables_example['label'] = variables_example['label'].apply(wrap, args=[23])

# Generating examplary charts
pie_0, label_0= generate_charts(variables_example['variable'][0], variables_example['label'][0])
pie_1, label_1= generate_charts(variables_example['variable'][1], variables_example['label'][1])
pie_2, label_2= generate_charts(variables_example['variable'][2], variables_example['label'][2])
pie_3, label_3= generate_charts(variables_example['variable'][3], variables_example['label'][3])
st.altair_chart((pie_0 + label_0) | (pie_1 + label_1) | (pie_2 + label_2) | (pie_3 + label_3))

st.subheader('Ergebnisse zum Anschauen, Verändern und Vergleichen')

st.html('''
<p>Die allgemeinden Ergebnisse der Befragung kannst Du Dir im Folgenden genauer anschauen.</p>
<p>Wähle eine der Variablen und verschaffe Dir einen ersten Eindruck, wie die Mehrheit der Teilnehmenden geantwortet hat. In der detaillierten Ansicht erfährst Du zudem, wie die Antworten von sozialen Faktoren, wie dem Geschlecht, Schulabschluss oder zum Beispiel dem Alter, abhängig sind.</p> 
''')

with st.expander(label='Tipp', expanded=False):
    st.html('''
    <p>Wenn Du Dir in der vereinfachten Ansicht das Umweltbewusstsein anschaust, siehst Du, dass nur wenige der Befragten Klimaschutzmaßnahmen als eine Bevormundung empfinden.</p>
    <p>In der detaillierten Ansicht findest Du hierzu weitere Details. Wenn Du Dir zum Beispiel genauer anschaust, wie die Antworten von der Altersklasse abhängen, siehst Du, dass vor allem für ältere Menschen Klimaschutzmaßnahmen keine Einschränkung oder ein Gefühl der Kontrolle darstellen.</p>    
    ''')

# Determining x variables
x_variables = list(df_selected.loc[: ,(df_selected.columns.isin(['LF01', 'HA03', 'MP03']))].select_dtypes(include='category').columns)

# Defining dict containing question labels not included in row data and filtering by selected sector
additional_column_labels = {'MT02': 'Lebenszufriedenheit',
                            'MT03': 'Wertvorstellungen',
                            'MP04': 'Umweltbewusstsein',
                            'PZ03': 'Suffizienzbereitschaft',
                            'PZ07': 'Suffizienzbarrieren',
                            'MP05': 'Narrative'
                            }
# Defining dict containing original labels of variables
orig_name_x_variables = {
    'MT02': 'Wie zufrieden sind Sie mit Ihrem Leben?',
    'MT03': 'Was gehört für Sie zu einem guten Leben?',
    'MP04': 'Im Folgenden finden Sie einige Aussagen über Umwelteinstellungen. Bitte bewerten Sie wie zutreffend diese sind.',
    'PZ03': 'Welche Meinung haben Sie zu folgenden Verhaltensweisen?',
    'PZ07': 'Wie müssten sich die Rahmenbedingungen ändern, damit Sie gleichzeitig ein umweltfreundlicheres undgutes Leben führen könnten?',
    'MP05': 'Wie stark fühlen Sie sich durch folgende Leitsätze angesprochen?',
    'LF01': 'Das Wort Suffizienz...',
    'HA03': 'In welchem der folgenden Lebensbereiche könnten Sie sich am ehesten vorstellen Veränderungen vorzunehmen?',
    'MP03': 'Auf einer Skala von 1 bis 10: Wie viel Wahlfreiheit haben Sie über Ihr Leben?'
}

# Adding the filtered additional variables to the x variables
for i, (key, value) in enumerate(additional_column_labels.items()):
    if key not in st.session_state.meta.column_names_to_labels.keys():
        st.session_state.meta.column_names_to_labels.update({key: value})
    x_variables.insert(i, key)

# Defining variables which shall not be considered furthermore
variables_excluded = []

# Determining name of selected x variable
name_x_variable = st.selectbox(label='Auswahl der Variablen', options=[st.session_state.meta.column_names_to_labels[k] for k in x_variables if (k in st.session_state.meta.column_names_to_labels) & (k not in variables_excluded)])
x_variable = [k for k, v in st.session_state.meta.column_names_to_labels.items() if v==name_x_variable][0]
orig_name_x_variable = orig_name_x_variables[x_variable]
st.success(x_variable + ': ' + orig_name_x_variable)

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

    no_y_selection = 'Keine'
    filter = []
    if type_of_chart==option_detail:
        with st.expander(label='Möglichkeit für weitere Differenzierung nach sozialen Faktoren', expanded=False):

            # Determining y variables
            y_variables = df_selected.loc[:, (df_selected.columns.isin(['SL02', 'SL03', 'SL06', 'SL08', 'SL09', 'SL10', 'SL11', 'SL13_02', 'Alter_Quote', 'Einkommen_Quote']))
                          ].select_dtypes(include='category').columns

            # Determing original names of y variables
            orig_name_y_variables = {
                'SL02': 'Welchem Geschlecht fühlen Sie sich zugehörig?',
                'SL03': 'Was ist Ihr höchster Schulabschluss?',
                'SL06': 'Wie viele Personen leben in Ihrem Wohnort/Ihrer Stadt',
                'SL08': 'Haben Sie Migrationserfahrung?',
                'SL09': 'Sind Sie aktuell erwerbstätig?',
                'SL10': 'Sind Sie selbständig?',
                'SL11': 'Welche Beschreibung trifft auf Ihre Arbeitszeitgestaltung am ehesten zu?',
                'SL13_02': 'Haben Sie minderjährige Kind(er)?',
                'Alter_Quote': 'Wie alt sind Sie?',
                'Einkommen_Quote': 'Welcher Einkommensklasse (netto) können Sie zugeordnet werden?',
            }

            # Selecting y variable
            options = [st.session_state.meta.column_names_to_labels[k] for k in y_variables if
                       k in st.session_state.meta.column_names_to_labels]
            options.insert(0, no_y_selection)
            name_y_variable = st.selectbox(label='Auswahl einer weiteren Variablen (optional)', options=options)

            if name_y_variable != no_y_selection:
                y_variable = [k for k, v in st.session_state.meta.column_names_to_labels.items() if v == name_y_variable][0]
                name_y_variable = st.session_state.meta.column_names_to_labels[y_variable]
                st.success(y_variable + ': ' + orig_name_y_variables[y_variable])

                # Setting filter by selecting the values for grouping
                filter_options = list(df_selected[y_variable].cat.categories)
                filter_options = ["\>= 3.000 Euro" if option=='>= 3.000 Euro' else option for option in filter_options]
                filter_options.insert(0, 'Gesamt')
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
        total_label = 'Gesamt'
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
        if type_of_chart==option_detail:
            if name_y_variable == no_y_selection:
                altair_chart_total = alt.Chart(df_selected.dropna(subset=subset)).mark_bar().encode(
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
            if int((len(options) + 1) / 2 - 2)>0:
                end_index = int((len(options) + 1) / 2 - 2)
            else:
                end_index = 1
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