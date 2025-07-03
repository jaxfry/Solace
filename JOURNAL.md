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
| Part Name                        | Quantity | Price (CAD) | Description                                      | Link                                                                 |
|----------------------------------|----------|-------------|--------------------------------------------------|----------------------------------------------------------------------|
| PLS-P830985                      | 1        | $30.65      | Speaker                                          | [Digikey](https://www.digikey.ca/en/products/detail/peerless-by-tymphany/PLS-P830985/6211132) |
| Raspberry Pi Touch Display V1    | 1        | $85.95      | 7-inch touchscreen display for Raspberry Pi     | [Digikey](https://www.digikey.ca/en/products/detail/raspberry-pi/ASIN-B00X4WHP5E/6211133) |
| Raspberry Pi 5 4GB               | 1        | $109.95     | Mini computer                                   | [Amazon](https://www.amazon.ca/Raspberry-Pi-4GB-2023-Processor/dp/B0CK3L9WD3/) |
| Stereo 20W Class D Audio Amplifier - MAX9744 | 1 | $19.95 | Audio amplifier for Raspberry Pi                | [Digikey](https://www.digikey.ca/en/products/detail/adafruit-industries-llc/1752/4990780) |
| VER36US120-JA                    | 1        | $30.04      | Wall adapter                                    | [Digikey](https://www.digikey.ca/en/products/detail/xp-power/VER36US120-JA/6220859) |
| PJ-037AH                         | 1        | $1.01       | Power Jack                                      | [Digikey](https://www.digikey.ca/en/products/detail/same-sky-formerly-cui-devices/PJ-037AH/1644547) |
| USB Mini Mic                     | 1        | $6.99       | USB microphone for audio input                  | [Amazon](https://www.amazon.ca/Mini-Microphone-Skype-Desktop-Laptop/dp/B076BC2Y3W/) |
| 0297003.U                        | 1        | $0.57       | A 3A fuse, so I don't burn my house down        | [Digikey](https://www.digikey.ca/en/products/detail/littelfuse-inc/0297003-U/3427703) |
| UGREEN USB Audio Adapter         | 1        | $14.39      | A USB audio dongle                              | [Amazon](https://www.amazon.ca/UGREEN-Adapter-Support-Headphone-Compatible-dp-B08Y8CZB2S/dp/B08Y8CZB2S/ref=dp_ob_title_ce) |
| LC78_05-3.0                      | 1        | $19.52      | A 5V 3A power supply for the Raspberry Pi       | [Digikey](https://www.digikey.ca/en/products/detail/gaptec-electronic/LC78-05-3-0/13692361) |
| Aux Cable 1Ft                    | 1        | $6.99       | A 1ft aux cable to connect the amp to the Raspberry Pi | [Amazon](https://www.amazon.ca/Tan-QY-Auxiliary-Compatible-Headphones/dp/B08BNMJ3ND/) |
| 5183                             | 1        | $6.99       | Temperature and humidity sensor                 | [Amazon](https://www.amazon.ca/Temperature-Humidity-Sensor-Module-5V/dp/B07Z3X9F6H/ref=sr_1_4?crid=1K2Q0W7J8Y2X&dib=eyJ2IjoiMSJ9.0b3gkqj4d) |
| 4698                             | 1        | $23.24      | Color Light Sensor                              | [Digikey](https://www.digikey.ca/en/products/detail/adafruit-industries-llc/4698/13162109) |
| LSYGXYZ 6 Pieces Acrylic Rods    | 1        | $8.99       | Acrylic rods to have the light sensor inside the case | [Amazon](https://www.amazon.ca/LSYGXYZ-Acrylic-Decorations-Gardening%EF%BC%883mm-Diameter%EF%BC%89/dp/B09M846847/) |
| **Total**                        |          | **$365.23 CAD** |                                                  |                                                                      |

Displays and Pis are crazy expensive, good thing I already have the display!
