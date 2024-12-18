import streamlit as st

# Load style css
with open('style.css') as f:
	st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.header('Weitere Projektinformationen')
st.html('<p>Diese Seite entstand im Rahmen des Projektes „Entwicklung von Suffizienzgeleiteten Angeboten und Narrativen als Teil der Energiewende auf Grundlage einer konsumorientierten Bedürfnisanalyse“.</p>')

col1, col2 = st.columns([1,8])
with col1:
	st.html('''
	<p class="no-margin"><b>Kurzform</b>:</p>
	<p class="no-margin"><b>FKZ</b>:</p>
	<p><b>Laufzeit</b>:</p>
	''')
with col2:
	st.html('''
	<p class="no-margin">SuzAnNa</p>
	<p class="no-margin">03EI5222</p>
	<p>Januar 2022 – Dezember 2024</p>
	''')

st.image('https://www.innovation-beratung-foerderung.de/INNO/Redaktion/DE/Bilder/Titelbilder/titel_foerderlogo_bmwi.png?__blob=normal&v=1', width=210)

st.html('''
        <p>Verantwortlich für diese Seite ist die IZES gGmbH.</p>        
        <p><b>IZES gGmbH</b><br>Altenkesseler Str. 17, Geb. A1<br>66115 Saarbrücken</p>
        <p>Als Projektpartner in dem Forschungsvorhaben sind zudem beteiligt:</p>
        <p><b>Arepo GmbH</b><br>Albrechtstraße 22<br>10117 Berlin</p>
        <p><b>IKEM – Institut für Klimaschutz, Energie und Mobilität</b><br>Magazinstraße 15–16<br>10179 Berlin</p>
        <p>Kontaktperson für das Projekt ist Frau Zheng, forschungsdaten(at)izes.de.
        <p>Weitere Informationen zum Vorhaben sind auf der Projektseite zu finden: <a href='https://izes.eu/projektportfolio/suzanna/'>https://izes.eu/projektportfolio/suzanna/</a></p>
''')




