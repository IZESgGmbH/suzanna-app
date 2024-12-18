import streamlit as st
import pandas as pd
import altair as alt

# Load style css
with open('style.css') as f:
	st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Adding title and header
st.header('Die SUZANNA-App')
st.html('<p>Diese App beinhaltet eine interaktive Darstellung der im Projekt erhobenen Daten und Ergebnisse. Damit möchten wir die datenbasierten Erkenntnisse für jede*n zugänglich machen.</p><p>Die Anwendung enthält folgende Bestandteile:</p>')
st.subheader('1. Die SUZANNA-Erhebung: eine sozialwissenschaftliche Basis')
st.html('<p>Die Basis des Projektes ist eine repräsentative Online-Erhebung aus September 2022 unter dem Namen „Wie kann ein gutes Leben innerhalb ökologischer Grenzen gelingen?“. Die Erhebung hatte das Ziel, die vielfältigen Vorstellungen der Menschen zu erfassen, was ein gutes Leben in verschiedenen Lebensbereichen ausmacht. Gleichzeitig sollten strukturelle Barrieren identifiziert werden, die die Umsetzung eines solchen Lebensstils erschweren. Besonderes Augenmerk lag dabei auf der Ermittlung potenzieller Ansätze für einen nachhaltigeren und umweltfreundlicheren Lebensstil. Dabei wurden folgende Handlungsfelder betrachtet:</p><ul><li>Mobilität</li><li>Wohnen und Energie</li><li>Konsum und Ernährung</li><li>Erwerbsarbeitszeit</li></ul><p>In der App können die Ergebnisse dieser Befragung eingesehen und interaktiv ausgewertet werden.</p>')

with st.expander('Rahmendaten der Befragung'):
    st.html('''
    <p>Der Fragebogen, strukturiert in 80 Fragen mit 412 Items, erfasst die individuellen Lebensbilder, Werthaltungen und sozialen Faktoren. Die Auswahl der Befragten (n=3088) erfolgte mittels Quotierung auf sechs Merkmale, die der Wohnbevölkerung im Alter von 16 bis 75 Jahren entsprechen:</p>
    <ul>
        <li>Geschlecht (männlich/weiblich/divers)</li>
        <li>Alter</li>
        <li>Wohnort</li>
        <li>Schulabschluss</li>
        <li>Haushalts-Netto-Einkommen</li>
        <li>Regionale Verteilung</li>
    </ul>
    <p>Diese Quotierung ermöglicht eine gezielte Repräsentation verschiedener demografischer Kategorien innerhalb der Stichprobe. Über diese Kategorien hinausgehende soziale Merkmale wurden in der Erhebung zusätzlich abgefragt:</p>
    <ul>
        <li>Alter und Anzahl von Kindern im Haushalt</li>
        <li>Zeitliche Verteilung von Sorgeverantwortung</li>
        <li>Pflegeverantwortung, Erwerbstätigkeit</li>
        <li>Arbeitszeitmodell</li>
        <li>Vermögen</li>
        <li>Prekäre Beschäftigung</li>
        <li>Religion</li>
        <li>Anzahl der Personen im Haushalt</li>
    </ul> 
    ''')

st.subheader('2. Milieus: Suche nach Hebelpunkten für Klimaschutz in den Lebensbedürfnissen')
st.html('<p>Die Auswertung der Befragungsergebnisse ermöglicht die Identifikation verschiedener Milieus bzw. Lebensbilder, die sich aufgrund sozialstruktureller Daten, Werthaltungen sowie Verhaltensweisen unterscheiden lassen. Dabei konnten wir Ansatz- bzw. Hebelpunkte (leverage points) für Suffizienz (Leventon et al. 2021; Meadows 1999) in den Lebensbildern der Menschen identifizieren. Dies ermöglicht es, direkt an den Lebensbedürfnissen, bzw. den individuellen Vorstellungen vom guten Leben anzusetzen. Die Ergebnisse zu den Milieus werden im Erbnisbereich unter "Milieus" dargestellt.</p>')

st.subheader('3. Suffizienz-fördernde Dienstleistungsangebote')
st.html('<p>Dienstleisten sind eine Möglichkeit, um suffiziente Lebens- und Wirtschaftsweisen in verschiedenen Bevölkerungsgruppen zu unterstützen und zu fördern. Basierend auf einer umfangreichen Literaturrecherche bietet diese App zudem einen Überblick über bestehende Angebote in den Bereichen Konsum, Mobilität, Wohnen und Energie. Diese werden daraufhin bewertet, wie sie direkt oder indirekt Suffizienz-orientierte Lebensverhalten fördern können. Die Ergebnisse dazu stehen unter dem Bereich "Steckbriefe" zur Verfügung.</p>')

st.subheader('Nutzung der Daten')
st.html('<p>Die hier dargestellten Inhalte und Daten sind öffentlich zugänglich unter: <a href="https://github.com/IZESgGmbH/suzanna-app">https://github.com/IZESgGmbH/suzanna-app</a></p><p>Eine <i>Nutzung der Daten</i> ist unter den dort angegebenen Lizenzbedingungen möglich.</p>')