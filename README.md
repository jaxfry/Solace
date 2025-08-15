<div align="center">

# Solace

![Solace Build](https://hc-cdn.hel1.your-objectstorage.com/s/v3/b1d7d9f75eed66be460fd089f704f1a9c68dcea9_img_4140_medium.jpeg)

## Description

**What is Solace?**

Solace is a physical extension of [LifeLog](https://github.com/jaxfry/LifeLog) that collects real-world data, displays real-time insights and statistics, and includes a voice assistant that integrates with the LifeLog system.

---

## Why I Made This

I wanted to create a physical device to complement the LifeLog system, providing a way to display data right beside my bed. I also wanted to create a voice assistant to further interact and for voice journal logging, a valuable data source.

---

## Project Pictures

### 3D Model

![3D Model](https://hc-cdn.hel1.your-objectstorage.com/s/v3/2b9eb8abc3eefa078e364038368a2c1ae50b5851_cleanshot_2025-07-08_at_13.30.27_2x.png)

### Wiring Diagram

![Wiring Diagram](https://hc-cdn.hel1.your-objectstorage.com/s/v3/94208fc16c89ac5b3baafca2eabae22fe82fc5b8_cleanshot_2025-07-06_at_00.52.57_2x.png)

Please note that I used a generic buck converter in the diagram, but in the actual device I use a specific one.

### Bill of Materials (BOM)
|Part Name                                            |Quantity|Price (CAD)|Description                                                         |Link                                                                                                |
|-----------------------------------------------------|--------|-----------|--------------------------------------------------------------------|----------------------------------------------------------------------------------------------------|
|PLS-P830985                                          |1       |$30.65     |Speaker                                                             |https://www.digikey.ca/en/products/detail/peerless-by-tymphany/PLS-P830985/6211132                  |
|Raspberry Pi Touch Display V1                        |1       |$85.95     |7-inch touchscreen display for Raspberry Pi                         |https://www.amazon.ca/DAOKAI-TPA3118-Amplifier-Single-Channel/dp/B0BCK9ZRC4/                        |
|Raspberry Pi 4 2GB                                   |1       |$80.16     |Mini computer                                                       |https://www.amazon.ca/Raspberry-Model-2019-Quad-Bluetooth/dp/B07TD42S27/                            |
|DAOKAI 2Pcs TPA3118 Mono Amplifier Board             |1       |$19.95     |Audio amplifier for Raspberry Pi                                    |https://www.digikey.ca/en/products/detail/adafruit-industries-llc/1752/4990780                      |
|TR9CE5000CCP-N(R6B)                                  |1       |$$30.66    |power supply                                                        |https://www.digikey.ca/en/products/detail/mean-well-usa-inc/GST60A12-P1J/7703712                    |
|PJ-037AH                                             |1       |$1.01      |Power Jack                                                          |https://www.digikey.ca/en/products/detail/same-sky-formerly-cui-devices/PJ-037AH/1644547            |
|USB Mini Mic                                         |1       |$6.99      |USB microphone for audio input                                      |https://www.amazon.ca/Mini-Microphone-Skype-Desktop-Laptop/dp/B076BC2Y3W/                           |
|0297005.U                                            |1       |$0.57      |A 5A fuse, so I don't burn my house down                            |https://www.digikey.ca/en/products/detail/littelfuse-inc/0297005-U/3427486                          |
|OKR-T/6-W12-C                                        |1       |$13.89     |Buck converter                                                      |https://www.digikey.ca/en/products/detail/murata-power-solutions-inc/OKR-T-6-W12-C/2199629          |
|Aux Cable 1Ft                                        |1       |$6.99      |A 1ft aux cable to connect the amp to the Raspberry Pi              |https://www.amazon.ca/Tan-QY-Auxiliary-Compatible-Headphones/dp/B08BNMJ3ND/                         |
|3021451F5701(R)                                      |1       |$7.11      |Power Cord                                                          |https://www.digikey.ca/en/products/detail/globtek-inc/3021451F5701-R/8597816                        |
|MFR-25FRF52-2K7                                      |1       |$0.15      |RES 2.7K OHM 1% 1/4W AXIAL                                          |https://www.digikey.ca/en/products/detail/yageo/MFR-25FRF52-2K7/9138955                             |
|EEU-FC1E101S                                         |1       |$0.55      |Capacitor 100uF 25V                                                 |https://www.digikey.ca/en/products/detail/panasonic-electronic-components/EEU-FC1E101S/266278       |
|EEU-FR1A101                                          |1       |$0.47      |Capacitor 100uF 10V                                                 |https://www.digikey.ca/en/products/detail/panasonic-electronic-components/EEU-FR1A101/2433507       |
|C315C104M5U5TA                                       |2       |$0.41      |Capacitor 0.1uF 50V                                                 |https://www.digikey.ca/en/products/detail/kemet/C315C104M5U5TA/817927                               |
|28A2025-0A2                                          |1       |$3.84      |FERRITE CORE 320 OHM HINGED                                         |https://www.digikey.ca/en/products/detail/laird-signal-integrity-products/28A2025-0A2/242803        |
|2Pack USB 3.0 Male to Female Adapter 7.9inches (20cm)|1       |$7.90      |USB 3.0 extension cable                                             |https://www.amazon.ca/Female-Extension-Cable-Male-Female/dp/B084WPG7QG/                             |
|110991327                                            |1       |$1.54      |Heat sink for the Raspberry Pi 4                                    |https://www.digikey.ca/en/products/detail/seeed-technology-co-ltd/110991327/10451876                |
|0FHM0001ZXJ                                          |1       |$12.74     |Fuse Holder                                                         |https://www.digikey.ca/en/products/detail/littelfuse-commercial-vehicle-products/0FHM0001ZXJ/2004060|
|M2.5 Standoff kit                                    |1       |$9.67      |M2.5 Standoff kit for mounting the Raspberry Pi and other components|https://www.amazon.ca/XLX-Male-Female-Female-Female-Assortment-Stainless/dp/B07FMV5RMG/             |
|FIT0585                                              |1       |$4.55      |18 AWG Wire                                                         |https://www.digikey.ca/en/products/detail/dfrobot/FIT0585/9559254?gQT=1                             |
|uxcell                                               |1       |$6.75      |M4*12 screws for speaker                                            |https://www.amazon.ca/gp/product/B0F1YR73PB/                                                        |
|Total                                                |        |$328.94    |                                                                    |                                                                                                    |

### Final Product Pictures
![Final Product](https://hc-cdn.hel1.your-objectstorage.com/s/v3/f3e7e89f0f9093afc290d6db3b98a75e148a24c3_img_4138.jpeg)