# VendorFlow

VendorFlow is a comprehensive platform for managing vending machines and smart home appliances through MQTT protocol. It allows users to monitor, control, and perform CRUD operations on their devices.

## Table of Contents
- [Installation](#installation)
- [Technologies Used](#technologies-used)
- [Project Overview](#project-overview)
  - [Vending Machines](#vending-machines)
  - [Smart Home Appliances](#smart-home-appliances)
- [Running the Project](#running-the-project)
- [Contact](#contact)

## Installation

To install the necessary dependencies, run the following command:
```sh
pip install -r requirements.txt
```

To start the project, navigate to the root of the project directory and run:
```sh
python3 manage.py runserver
```

## Technologies Used

- **Backend**: Django, Python
- **Frontend**: HTML, CSS, JavaScript, Django Templates, Bootstrap
- **MQTT**: Paho-MQTT
- **Forms**: Django-Crispy-Forms

## Project Overview

### Vending Machines

VendorFlow allows users to manage their vending machines through the website. The vending machines are equipped with built-in SIM cards that transfer sales and transaction records to the website via MQTT. 

#### Instructions
1. Acquire a vending machine from our retail store.
2. Go to the website and add a new device using the serial number (a 24-character word) found on the vending machine.

### Smart Home Appliances

The smart home section is designed to connect IoT devices to the website through an MQTT client. This enables users to monitor and control their devices remotely.

## Running the Project

For running the project, follow these steps:

1. Install the dependencies using the instructions provided in the Installation section.
2. Run the project using the command:
   ```sh
   python3 manage.py runserver
   ```
3. Register your vending machine on the website by adding a new device with its serial number.

## Contact

For any questions or support, please contact Shadrack Andare:
- **Website**: [VendorFlow](https://vendorflow.vercel.app)
- **GitHub**: [andareomondi](https://github.com/andareomondi)
- **Phone**: 0741716609
```

Feel free to copy and paste this into your README.md file on GitHub. Let me know if you need any further adjustments or additions!
