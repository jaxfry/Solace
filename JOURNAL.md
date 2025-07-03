---
title: "Solus"
author: "Jaxon"
description: "A DIY Braun DN40-inspired alarm clock that’s also a LifeLog Satellite and smart speaker."
created_at: "2025-06-28"
---
# 28 June 2025 - Project Kick-off (3 Hours)
- Drafted project goals and some technical details
- Flashed Raspberry Pi 3 for testing
- Sucsessfully got display to connect
- Got flutter set up and demo working
- Set up dev enviroment on macbook
- Started (re)Learning Flutter Basics
- Started thinking about the layout of the UI
# 29 June 2025 - Components Research (1 hour)
I was researching different types of displays, but ended up deciding upon a standard raspberry pi display after much concideration for a nice AMOLED screen, it's just too expensive. I'll make a BOM soon!
# 29 June 2025 - Design sketch (30 mins)
- Just sketched a design and wrote about Solace and LifeLog.
![notebook](https://github.com/jaxfry/Solace/blob/main/assets/IMG_3976.jpeg)
# 30 June 2025 - Design Prototype Case (3 hours)
Today I designed two iterations of the case all while rembering how to use Fusion 360, just a very early testing stage with some broken screen (honestly might be a safty hazard if it wasn't hidden by the case) and stuff I've got laying around. I plan to redesign it to fit what ever display I end up choosing. On that note, I've got almost all of the components picked out except the display... I know, I started concidering the OLED screens again.
![Case Prototype](https://hc-cdn.hel1.your-objectstorage.com/s/v3/9558a9376349096f5571a5a9b8c74ab3ac5a25d3_img_3977.jpeg)
# 1 July 2025 - UI Implementation (1 hour)
- Today I was limited on time, but I tested different fonts, spacing, and colors. I also added some nice color gradents depending on what time of day it is. Tomorrow I plan to add pages to the UI, and hook it into the LifeLog API!
![UI](https://hc-cdn.hel1.your-objectstorage.com/s/v3/204a3b8548ccc160edd3fd8c15deb6d1d7d675bf_img_3978.jpeg)
# 1 July into 2 July - Picking Parts, CAD, and Research (past mid-might, 4 hours)
I stayed up until at least 1am doing this. I'm tired.
- I realized I knew very little about the audio world, but through research I figured out that your enclosure size maters when picking a speaker. As a result of this I had to ensure that it would still sound good in my case. I've decided on the PLS-P830985 as it's budget friendly and small enough to fit inside my project. I found a better alternitive, but it was $100, out of my budget.
- On the cad design, I fixed some minor issues like some misalignments.
- Made progress on the BOM!
# 2 July - Finalizing BOM and Research (3.5 hours)
Today we went to a water park, so I had tons of time in the car and when I got home to work on the project.
|Part Name                                            |Quantity|Price (CAD)        |Description                                                                                  |Link                                                                                                            |
|-----------------------------------------------------|--------|-------------------|---------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------|
|PLS-P830985                                          |1       |$30.65             |Speaker                                                                                      |https://www.digikey.ca/en/products/detail/peerless-by-tymphany/PLS-P830985/6211132                              |
|Raspberry Pi Touch Display V1                        |1       |$85.95             |7-inch touchscreen display for Raspberry Pi                                                  |https://www.digikey.ca/en/products/detail/raspberry-pi/ASIN-B00X4WHP5E/6211133                                  |
|Raspberry Pi 4 2GB                                   |1       |$80.16             |Mini computer                                                                                |https://www.amazon.ca/Raspberry-Model-2019-Quad-Bluetooth/dp/B07TD42S27/                                        |
|Stereo 20W Class D Audio Amplifier - MAX9744         |1       |$19.95             |Audio amplifier for Raspberry Pi                                                             |https://www.digikey.ca/en/products/detail/adafruit-industries-llc/1752/4990780                                  |
|GST60A12-P1J                                         |1       |$27.10             |power supply                                                                                 |https://www.digikey.ca/en/products/detail/mean-well-usa-inc/GST60A12-P1J/7703712                                |
|PJ-037AH                                             |1       |$1.01              |Power Jack                                                                                   |https://www.digikey.ca/en/products/detail/same-sky-formerly-cui-devices/PJ-037AH/1644547                        |
|USB Mini Mic                                         |1       |$6.99              |USB microphone for audio input                                                               |https://www.amazon.ca/Mini-Microphone-Skype-Desktop-Laptop/dp/B076BC2Y3W/                                       |
|0297005.U                                            |1       |$0.57              |A 5A fuse, so I don't burn my house down                                                     |https://www.digikey.ca/en/products/detail/littelfuse-inc/0297005-U/3427486                                      |
|OKR-T/6-W12-C                                        |1       |$13.89             |Buck converter                                                                               |https://www.digikey.ca/en/products/detail/murata-power-solutions-inc/OKR-T-6-W12-C/2199629                      |
|Aux Cable 1Ft                                        |1       |$6.99              |A 1ft aux cable to connect the amp to the Raspberry Pi                                       |https://www.amazon.ca/Tan-QY-Auxiliary-Compatible-Headphones/dp/B08BNMJ3ND/                                     |
|4698                                                 |1       |$23.24             |Color Light Sensor                                                                           |https://www.digikey.ca/en/products/detail/adafruit-industries-llc/4698/13162109                                 |
|LSYGXYZ 6 Pieces Acrylic Rods                        |1       |$8.99              |Acrylic rods to have the light sensor inside the case                                        |https://www.amazon.ca/LSYGXYZ-Acrylic-Decorations-Gardening%EF%BC%883mm-Diameter%EF%BC%89/dp/B09M846847/        |
|PC-ABK006F                                           |1       |$7.11              |Power Cord                                                                                   |https://www.digikey.ca/en/products/detail/bel-inc/PC-ABK006F/15777826                                           |
|MFR-25FBF52-33K                                      |1       |$0.15              |Resistor 33K Ohm 1/4W                                                                        |https://www.digikey.ca/en/products/detail/yageo/MFR-25FBF52-33K/9138137                                         |
|EEU-FC1E101S                                         |1       |$0.55              |Capacitor 100uF 25V                                                                          |https://www.digikey.ca/en/products/detail/panasonic-electronic-components/EEU-FC1E101S/266278                   |
|EEU-FR1A101                                          |1       |$0.47              |Capacitor 100uF 10V                                                                          |https://www.digikey.ca/en/products/detail/panasonic-electronic-components/EEU-FR1A101/2433507                   |
|C315C104M5U5TA                                       |2       |$0.41              |Capacitor 0.1uF 50V                                                                          |https://www.digikey.ca/en/products/detail/kemet/C315C104M5U5TA/817927                                           |
|28A2025-0A2                                          |1       |$3.84              |FERRITE CORE 320 OHM HINGED                                                                  |https://www.digikey.ca/en/products/detail/laird-signal-integrity-products/28A2025-0A2/242803                    |
|2Pack USB 3.0 Male to Female Adapter 7.9inches (20cm)|1       |$7.90              |USB 3.0 extension cable                                                                      |https://www.amazon.ca/Female-Extension-Cable-Male-Female/dp/B084WPG7QG/                                         |
|110991327                                            |1       |$1.54              |Heat sink for the Raspberry Pi 4                                                             |https://www.digikey.ca/en/products/detail/seeed-technology-co-ltd/110991327/10451876                            |
|0FHM0001ZXJ                                          |1       |$12.74             |Fuse Holder                                                                                  |https://www.digikey.ca/en/products/detail/littelfuse-commercial-vehicle-products/0FHM0001ZXJ/2004060            |
|M2.5 Standoff kit                                    |1       |$9.67              |M2.5 Standoff kit for mounting the Raspberry Pi and other components                         |https://www.amazon.ca/XLX-Male-Female-Female-Female-Assortment-Stainless/dp/B07FMV5RMG/                         |
|M3 x 10mm                                            |1       |$12.86             |M3 x 10mm Thread Pitch screws for mounting the Raspberry Pi and other components             |https://www.amazon.ca/iexcell-Thread-Socket-Button-Screws/dp/B0CP4BLD7Z/                                        |
|FIT0585                                              |1       |$4.55              |18 AWG Wire                                                                                  |https://www.digikey.ca/en/products/detail/dfrobot/FIT0585/9559254?gQT=1                                         |
|MMOBIEL 20 Gauge Electrical Wire Parallel - 20 AWG   |1       |$11.49             |20 AWG Wire                                                                                  |https://www.amazon.ca/MMOBIEL-Gauge-Electrical-Wire-Parallel/dp/B0DGV5V2SM                                      |
|4397                                                 |1       |$1.38              |STEMMA/Qwiic cable                                                                           |https://www.digikey.ca/en/products/detail/adafruit-industries-llc/4397/10824270                                 |

Everything is crazy expensive :sob:, good thing I already have the display and pi!
