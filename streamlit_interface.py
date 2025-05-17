import streamlit as st
import numpy as np
import math

# Funzioni di calcolo

def AH(T, RH):
    Pvs = 6.112 * math.exp((17.62 * T) / (243.12 + T))
    Pv = RH / 100 * Pvs
    AH = (Pv / (461.5 * (273.15 + T))) * 100000
    return AH

def DewPoint(T, RH):
    Tn = 240.7263
    A = 6.116441
    m = 7.591386
    Pws = (A * 10 ** ((m * T) / (T + Tn)))
    Pw = Pws * RH / 100
    Td = Tn / ((m / np.log10(Pw / A)) - 1)
    return Td

# Sidebar per parametri ambientali
st.sidebar.header('Parametri Ambientali')
int_temp = st.sidebar.slider('Temperatura Interna (°C)', min_value=0.0, max_value=40.0, value=15.0, step=0.1)
int_rel_hum = st.sidebar.slider('Umidità Relativa Interna (%)', min_value=0, max_value=100, value=70, step=1)
int_surf_temp = st.sidebar.slider('Temperatura Superficie Interna (°C)', min_value=0.0, max_value=40.0, value=18.4, step=0.1)
ext_temp = st.sidebar.slider('Temperatura Esterna (°C)', min_value=-20.0, max_value=50.0, value=12.0, step=0.1)
ext_rel_hum = st.sidebar.slider('Umidità Relativa Esterna (%)', min_value=0, max_value=100, value=45, step=1)

# Celle per threshold
st.sidebar.header('Soglie di Controllo')
condensation_activation_threshold = st.sidebar.number_input('Soglia attivazione condensa (°C)', value=2.0, step=0.1)
condensation_deactivation_threshold = st.sidebar.number_input('Soglia disattivazione condensa (°C)', value=4.0, step=0.1)
humidity_difference_activation_threshold = st.sidebar.number_input('Soglia attivazione umidità assoluta (g/m3)', value=5.0, step=0.1)
humidity_difference_deactivation_threshold = st.sidebar.number_input('Soglia disattivazione umidità assoluta (g/m3)', value=10.0, step=0.1)

cooling_temp_activation_threshold = st.sidebar.number_input('Soglia attivazione raffreddamento (°C)', value=26.0, step=0.1)
cooling_temp_deactivation_threshold = st.sidebar.number_input('Soglia disattivazione raffreddamento (°C)', value=20.0, step=0.1)
cooling_humidity_activation_threshold = st.sidebar.number_input('Soglia attivazione raffreddamento umidità (%)', value=25.0, step=0.1)
cooling_humidity_deactivation_threshold = st.sidebar.number_input('Soglia disattivazione raffreddamento umidità (%)', value=40.0, step=0.1)

heating_temp_activation_threshold = st.sidebar.number_input('Soglia attivazione riscaldamento (°C)', value=9.0, step=0.1)
heating_temp_deactivation_threshold = st.sidebar.number_input('Soglia disattivazione riscaldamento (°C)', value=17.0, step=0.1)
heating_humidity_activation_threshold = st.sidebar.number_input('Soglia attivazione riscaldamento umidità (%)', value=80.0, step=0.1)
heating_humidity_deactivation_threshold = st.sidebar.number_input('Soglia disattivazione riscaldamento umidità (%)', value=60.0, step=0.1)

dehumifier_humidity_activation_threshold = st.sidebar.number_input('Soglia attivazione deumidificatore (%)', value=80.0, step=0.1)
dehumifier_humidity_deactivation_threshold = st.sidebar.number_input('Soglia disattivazione deumidificatore (%)', value=60.0, step=0.1)

mech_ventilation_low_temp_activation_threshold = st.sidebar.number_input('Soglia attivazione ventilazione bassa T (°C)', value=9.0, step=0.1)
mech_ventilation_low_temp_deactivation_threshold = st.sidebar.number_input('Soglia disattivazione ventilazione bassa T (°C)', value=13.0, step=0.1)
mech_ventilation_high_temp_activation_threshold = st.sidebar.number_input('Soglia attivazione ventilazione alta T (°C)', value=24.0, step=0.1)
mech_ventilation_high_temp_deactivation_threshold = st.sidebar.number_input('Soglia disattivazione ventilazione alta T (°C)', value=17.0, step=0.1)

# Calcoli principali
int_abs_hum = round(AH(int_temp, int_rel_hum), 2)
int_dew_p = round(DewPoint(int_temp, int_rel_hum), 2)
ext_abs_hum = round(AH(ext_temp, ext_rel_hum), 2)
ext_dew_p = round(DewPoint(ext_temp, ext_rel_hum), 2)

st.title('Controllo Unità Climatizzazione')
st.subheader('Condizioni Ambientali')
st.write(f"Temperatura Interna: {int_temp} °C")
st.write(f"Umidità Relativa Interna: {int_rel_hum} %")
st.write(f"Temperatura Superficie Interna: {int_surf_temp} °C")
st.write(f"Umidità Assoluta Interna: {int_abs_hum} g/m3")
st.write(f"Punto di Rugiada Interno: {int_dew_p} °C")
st.write(f"Temperatura Esterna: {ext_temp} °C")
st.write(f"Umidità Relativa Esterna: {ext_rel_hum} %")
st.write(f"Umidità Assoluta Esterna: {ext_abs_hum} g/m3")
st.write(f"Punto di Rugiada Esterno: {ext_dew_p} °C")

# Controlli
condensation_check = False
absolute_humidity_check = False
condensation_diff = int_surf_temp - int_dew_p
humidity_diff = int_abs_hum - ext_abs_hum
if condensation_diff <= condensation_activation_threshold:
    condensation_check = True
elif condensation_check and condensation_diff >= condensation_deactivation_threshold:
    condensation_check = False
if humidity_diff >= humidity_difference_activation_threshold:
    absolute_humidity_check = True
elif absolute_humidity_check and humidity_diff <= humidity_difference_deactivation_threshold:
    absolute_humidity_check = False

st.subheader('Controlli')
st.write(f"Rischio Condensa: {'SI' if condensation_check else 'NO'}")
st.write(f"Possibile Ventilazione: {'SI' if absolute_humidity_check else 'NO'}")

# Unità
power_values = {
    "Heating": 3400,
    "Cooling": 2500,
    "Dehumidifier": 500,
    "Mechanical Ventilation": 150
}

# Cooling
cooling_system_active = False
cooling_reasons = []
if int_temp > cooling_temp_activation_threshold:
    cooling_system_active = True
    cooling_reasons.append("Alta temperatura")
if int_rel_hum < cooling_humidity_activation_threshold:
    cooling_system_active = True
    cooling_reasons.append("Bassa umidità relativa")
if cooling_system_active and (int_temp <= cooling_temp_deactivation_threshold and int_rel_hum >= cooling_humidity_deactivation_threshold):
    cooling_system_active = False
    cooling_reasons = []

# Heating
heating_system_active = False
heating_reasons = []
if condensation_check:
    heating_system_active = True
    heating_reasons.append("Condensa rilevata")
if int_temp < heating_temp_activation_threshold:
    heating_system_active = True
    heating_reasons.append("Bassa temperatura")
if int_rel_hum > heating_humidity_activation_threshold:
    heating_system_active = True
    heating_reasons.append("Alta umidità relativa")
if heating_system_active and (int_temp >= heating_temp_deactivation_threshold and int_rel_hum <= heating_humidity_deactivation_threshold):
    heating_system_active = False
    heating_reasons = []

# Dehumidifier
dehumifier_system_active = False
dehu_reasons = []
if condensation_check:
    dehumifier_system_active = True
    dehu_reasons.append("Condensa rilevata")
if int_rel_hum > dehumifier_humidity_activation_threshold:
    dehumifier_system_active = True
    dehu_reasons.append("Alta umidità relativa")
if dehumifier_system_active and int_rel_hum <= dehumifier_humidity_deactivation_threshold:
    dehumifier_system_active = False
    dehu_reasons = []

# Mechanical Ventilation
mech_ventilation_system_active = False
mech_reasons = []
if condensation_check:
    mech_ventilation_system_active = True
    mech_reasons.append("Condensa rilevata")
if absolute_humidity_check:
    mech_ventilation_system_active = True
    mech_reasons.append("Umidità assoluta esterna inferiore")
if int_temp < mech_ventilation_low_temp_activation_threshold and ext_temp > mech_ventilation_low_temp_deactivation_threshold:
    mech_ventilation_system_active = True
    mech_reasons.append("Bassa T interna e alta T esterna")
elif int_temp > mech_ventilation_high_temp_activation_threshold and ext_temp < mech_ventilation_high_temp_deactivation_threshold:
    mech_ventilation_system_active = True
    mech_reasons.append("Alta T interna e bassa T esterna")
if mech_ventilation_system_active and mech_ventilation_low_temp_deactivation_threshold <= int_temp <= mech_ventilation_high_temp_deactivation_threshold:
    mech_ventilation_system_active = False
    mech_reasons = []

# Output stato unità
st.subheader('Stato Unità')
st.write(f"Raffreddamento: {'ATTIVO' if cooling_system_active else 'SPENTO'}")
if cooling_system_active:
    st.write(f"Motivi: {', '.join(cooling_reasons)}")
st.write(f"Riscaldamento: {'ATTIVO' if heating_system_active else 'SPENTO'}")
if heating_system_active:
    st.write(f"Motivi: {', '.join(heating_reasons)}")
st.write(f"Deumidificatore: {'ATTIVO' if dehumifier_system_active else 'SPENTO'}")
if dehumifier_system_active:
    st.write(f"Motivi: {', '.join(dehu_reasons)}")
st.write(f"Ventilazione Meccanica: {'ATTIVA' if mech_ventilation_system_active else 'SPENTA'}")
if mech_ventilation_system_active:
    st.write(f"Motivi: {', '.join(mech_reasons)}")

# Calcolo consumo minimo
power_consumption = {
    "Riscaldamento": (heating_system_active, power_values["Heating"]),
    "Raffreddamento": (cooling_system_active, power_values["Cooling"]),
    "Deumidificatore": (dehumifier_system_active, power_values["Dehumidifier"]),
    "Ventilazione Meccanica": (mech_ventilation_system_active, power_values["Mechanical Ventilation"])
}
active_units = {system: power for system, (active, power) in power_consumption.items() if active}
if active_units:
    lowest_power_unit = min(active_units, key=active_units.get)
    st.success(f"L'unità attiva con il minor consumo è: {lowest_power_unit} (Consumo: {active_units[lowest_power_unit]} Watt)")
else:
    st.info("Nessuna unità è attualmente attiva.")
