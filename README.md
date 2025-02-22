
VendorFlow is a comprehensive platform for managing vending machines and smart home appliances through the MQTT protocol. It allows users to monitor, control, and perform CRUD operations on their devices.

## Table of Contents
- [Installation](#installation)
- [Technologies Used](#technologies-used)
- [Project Overview](#project-overview)
  - [Vending Machines](#vending-machines)
  - [Smart Home Appliances](#smart-home-appliances)
- [Running the Project](#running-the-project)
- [Contributing](#contributing)
- [License](#license)
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

#### Features
- **Real-time Data Transfer**: Sales and transaction records are sent to the website in real-time.
- **CRUD Operations**: Users can create, read, update, and delete records of their vending machines.
- **User Authentication**: Secure login for vending machine owners to access their data.
- **Reporting**: Generate detailed reports on vending machine performance.

#### Instructions
1. Acquire a vending machine from our retail store.
2. Go to the website and add a new device using the serial number (a 24-character word) found on the vending machine.
3. Once added, the machine will start transferring data to the website automatically.

### Smart Home Appliances

The smart home section is designed to connect IoT devices to the website through an MQTT client. This enables users to monitor and control their devices remotely.

#### Features
- **Device Monitoring**: View the status of connected smart home devices.
- **Remote Control**: Turn devices on or off, adjust settings, and more.
- **Alerts & Notifications**: Receive alerts for any unusual activity or issues with devices.

## Running the Project

For running the project, follow these steps:

1. Install the dependencies using the instructions provided in the Installation section.
2. Run the project using the command:
   ```sh
   python3 manage.py runserver
   ```
3. Register your vending machine on the website by adding a new device with its serial number.
4. For smart home devices, connect them through the MQTT client and configure the settings on the website.

## Contributing

We welcome contributions to VendorFlow! To contribute, follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or support, please contact Shadrack Andare:
- **Website**: [VendorFlow](https://vendorflow.vercel.app)
- **GitHub**: [andareomondi](https://github.com/andareomondi)
- **Phone**: 0741716609
```

Feel free to review and let me know if there are any additional details or adjustments needed!
