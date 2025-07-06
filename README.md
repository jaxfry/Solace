# Solace

## Description

**What is Solace?**

Solace is a physical extension of [LifeLog](https://github.com/jaxfry/LifeLog) that collects real-world data, displays real-time insights and statistics, and includes a voice assistant that integrates with the LifeLog system.

---

## Why I Made This

I wanted to create a physical device to complement the LifeLog system, providing a way to display data right beside my bed. I also wanted to create a voice assistant to further interact and for voice journal logging, a valuable data source.

---

## Project Pictures

### 3D Model

![3D Model](https://hc-cdn.hel1.your-objectstorage.com/s/v3/e71c8c8a9725e7f2e04a51640a288c6fe2bac134_cleanshot_2025-07-03_at_15.13.48_2x.png)

### Wiring Diagram

![Wiring Diagram](https://hc-cdn.hel1.your-objectstorage.com/s/v3/e425a5f31b265cfcda28de4039f361293901b0a0_circuit_image__1_.png)

Please note that I used a generic buck converter in the diagram, but in the actual device I use a specific one.

### Bill of Materials (BOM)

|Part Name                                            |Quantity|Price (CAD)|Description                                                         |Link                                                                                                |
|-----------------------------------------------------|--------|-----------|--------------------------------------------------------------------|----------------------------------------------------------------------------------------------------|
|PLS-P830985                                          |1       |$30.65     |Speaker                                                             |https://www.digikey.ca/en/products/detail/peerless-by-tymphany/PLS-P830985/6211132                  |
|Raspberry Pi Touch Display V1                        |1       |$85.95     |7-inch touchscreen display for Raspberry Pi                         |https://www.digikey.ca/en/products/detail/raspberry-pi/ASIN-B00X4WHP5E/6211133                      |
|Raspberry Pi 4 2GB                                   |1       |$80.16     |Mini computer                                                       |https://www.amazon.ca/Raspberry-Model-2019-Quad-Bluetooth/dp/B07TD42S27/                            |
|Stereo 20W Class D Audio Amplifier - MAX9744         |1       |$19.95     |Audio amplifier for Raspberry Pi                                    |https://www.digikey.ca/en/products/detail/adafruit-industries-llc/1752/4990780                      |
|GST60A12-P1J                                         |1       |$27.10     |power supply                                                        |https://www.digikey.ca/en/products/detail/mean-well-usa-inc/GST60A12-P1J/7703712                    |
|PJ-037AH                                             |1       |$1.01      |Power Jack                                                          |https://www.digikey.ca/en/products/detail/same-sky-formerly-cui-devices/PJ-037AH/1644547            |
|USB Mini Mic                                         |1       |$6.99      |USB microphone for audio input                                      |https://www.amazon.ca/Mini-Microphone-Skype-Desktop-Laptop/dp/B076BC2Y3W/                           |
|0297005.U                                            |1       |$0.57      |A 5A fuse, so I don't burn my house down                            |https://www.digikey.ca/en/products/detail/littelfuse-inc/0297005-U/3427486                          |
|OKR-T/6-W12-C                                        |1       |$13.89     |Buck converter                                                      |https://www.digikey.ca/en/products/detail/murata-power-solutions-inc/OKR-T-6-W12-C/2199629          |
|Aux Cable 1Ft                                        |1       |$6.99      |A 1ft aux cable to connect the amp to the Raspberry Pi              |https://www.amazon.ca/Tan-QY-Auxiliary-Compatible-Headphones/dp/B08BNMJ3ND/                         |
|PC-ABK006F                                           |1       |$7.11      |Power Cord                                                          |https://www.digikey.ca/en/products/detail/bel-inc/PC-ABK006F/15777826                               |
|MFR-25FBF52-33K                                      |1       |$0.15      |Resistor 33K Ohm 1/4W                                               |https://www.digikey.ca/en/products/detail/yageo/MFR-25FBF52-33K/9138137                             |
|EEU-FC1E101S                                         |1       |$0.55      |Capacitor 100uF 25V                                                 |https://www.digikey.ca/en/products/detail/panasonic-electronic-components/EEU-FC1E101S/266278       |
|EEU-FR1A101                                          |1       |$0.47      |Capacitor 100uF 10V                                                 |https://www.digikey.ca/en/products/detail/panasonic-electronic-components/EEU-FR1A101/2433507       |
|C315C104M5U5TA                                       |2       |$0.41      |Capacitor 0.1uF 50V                                                 |https://www.digikey.ca/en/products/detail/kemet/C315C104M5U5TA/817927                               |
|28A2025-0A2                                          |1       |$3.84      |FERRITE CORE 320 OHM HINGED                                         |https://www.digikey.ca/en/products/detail/laird-signal-integrity-products/28A2025-0A2/242803        |
|2Pack USB 3.0 Male to Female Adapter 7.9inches (20cm)|1       |$7.90      |USB 3.0 extension cable                                             |https://www.amazon.ca/Female-Extension-Cable-Male-Female/dp/B084WPG7QG/                             |
|110991327                                            |1       |$1.54      |Heat sink for the Raspberry Pi 4                                    |https://www.digikey.ca/en/products/detail/seeed-technology-co-ltd/110991327/10451876                |
|0FHM0001ZXJ                                          |1       |$12.74     |Fuse Holder                                                         |https://www.digikey.ca/en/products/detail/littelfuse-commercial-vehicle-products/0FHM0001ZXJ/2004060|
|M2.5 Standoff kit                                    |1       |$9.67      |M2.5 Standoff kit for mounting the Raspberry Pi and other components|https://www.amazon.ca/XLX-Male-Female-Female-Female-Assortment-Stainless/dp/B07FMV5RMG/             |
|FIT0585                                              |1       |$4.55      |18 AWG Wire                                                         |https://www.digikey.ca/en/products/detail/dfrobot/FIT0585/9559254?gQT=1                             |
|DIN7985(M4*12)                                       |1       |$6.75      |M4*12 screws for speaker                                            |https://www.amazon.ca/Hilitand-Stainless-Machine-Threaded-Fastener/dp/B09MFX2SFG/                   |
|Total                                                |        |$328.94    |                                                                    |                                                                                                    |
