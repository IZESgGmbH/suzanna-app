import streamlit as st
import pandas as pd
import altair as alt

# Load style css
with open('style.css') as f:
	st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Adding title and header
st.header('Das SUZANNA-Projekt')
st.subheader('Entwicklung von Suffizienz-geleiteten Angeboten und Narrativen als Teil der Energiewende auf Grundlage einer konsumorientierten Bedürfnisanalys')

# Adding text
st.html('<p>SUZANNA ist ein Forschungsprojekt im Forschungsbereich <i>Energiewende und Gesellschaft</i> im 7. Energieforschungsprogramm. In dem Projekt haben wir ermittelt, wie <b>Suffizienz</b> stärker in erfolgreichen Klimaschutz einbezogen werden kann.</p>')
with st.expander('Definition von Suffizienz', expanded=False):
    st.html('<p>Suffizienz verstehen wir als Nachhaltigkeitsstrategie, die eine Reduktion des Ressourcenverbrauchs bewirkt und zwar durch dessen Vermeidung oder Verringerung. Im Gegensatz zu Effizienz wird Reduktion also nicht durch technische Lösungen erreicht. Suffizienz ist damit ein transformatives Konzept, das zum einen die Veränderung sozialer Praktiken sowie den Wandel von Lebensstilen und Lebensbildern erforderlich macht, zum anderen aber neuartige wirtschaftliche Produktionsweisen sowie Angebotsformate impliziert. SUZANNA arbeitet im Anschluss an Winterfeld (2011) mit einem positiven Suffizienzansatz, welcher an den Lebensbedürfnissen der Menschen ansetzt.</p>')
    col1, col2 = st.columns([1,8])
    with col1:
        st.html('<p><font color="DarkMagenta"><small><b>Quelle</b>:</small></font></p>')
    with col2:
        st.html(
            '<p><font color="DarkMagenta"><small>Winterfeld, Uta von (2011): <i>Vom Recht auf Suffizienz.</i> In: Rätz, Werner/von Egan-Krieger, Tanja/Muraca, Barbara/Passadakis, Alexis/Schmelzer, Matthias/Vetter, Andrea (hg.): <i>Ausgewachsen! Soziale Gerechtigkeit. Soziale Rechte. Gutes Leben.</i> Hamburg: VSA.</small></font></p>')

st.subheader('Inhalte im Projekt')
col1, col2, col3, col4 = st.columns([0.95, 0.65, 0.5, 0.5])
with col1:
    st.info('Hierzu haben wir eine sozialwissenschaftliche Analyse durchgeführt, in der die Einstellungen der Bürger*innen in Bezug auf ein gutes und ressourenschonendes Leben ermittelt wurden.')
with col2:
    st.info('Darauf aufbauend haben wir Suffizienz-fördernde Angebotsmodelle ermittelt und mit Praxisbeispielen hinterlegt')
with col3:
    st.info('Wir haben untersucht, wie der Rahmen für Suffizienz verbessert werden kann.')
with col4:
    st.info('Und wir haben Narrative entwickelt, die eine positive Suffizienzkul-tur fördern.')

st.subheader('Veröffentlichungen')
st.html('''
<ul>
    <li><i>Suffiziente Mobilitätspolitik für ein gutes Leben.</i> Impulspapier für die Politik. Schriftenreihe der IZES gGmbH | 2024_2, Juni 2024.</li>
    <li><i>SUZANNA. Nachhaltigkeit – Kultur – Suffizienz. Das Magazin.</i> Herausgeber: IZES gGmbH. Taucha: Verlag Marian Arnd UG, 2024.</li>
    <li><i>Vorstellung des Projektes SUZANNA. Erhebung individueller Lebensbilder und sozialstruktureller Faktoren: zu den Voraussetzungen von Suffizienz und zur Verbesserung ihrer Kommunikationsstrategien.</i> Vortrag von Dr. Andrea Amri-Henkel, IZES gGmbH & Prof. Dr. Ingo Uhlig, IKEM.</li>
</ul>
''')