## Overview
Inventory tracking system that combines RFID technology with an LCD verification system to ensure efficient stock management. It is designed to minimize human errors, reduce inventory loss, and improve tracking accuracy.

## Features
- **RFID-Based Tracking**: Detects items placed on or removed from shelves using RFID tags.
- **LCD Verification System**: Displays item movements and allows users to confirm transactions.
- **Wi-Fi Connectivity**: Communicates with a central server for real-time inventory updates.
- **Automated Notifications**: Alerts managers in case of discrepancies.
- **User Authentication**: Differentiates between general users and administrators.

## System Components
### Hardware
- ESP32 Microcontroller
- RFID Reader (MFRC522)
- LCD Screen
- Verification Buttons (YES/NO)
- Wi-Fi Module (built-in)
- MDF Enclosure

### Software
- MicroPython for ESP32
- Flask-based Web Server
- RFID Tag Management System
- LCD Display Interaction Code

## Installation & Setup
### Hardware Assembly
1. Assemble the RFID and LCD units into their respective enclosures.
2. Connect the RFID reader to the ESP32 microcontroller.
3. Secure the LCD and control buttons in the exit verification unit.
4. Ensure the microcontroller is powered via a micro-USB cable.

### Software Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/MedChouta/GNG1503
   ```
2. Install dependencies:
   ```sh
   pip install flask
   ```
3. Connect the ESP32 to Wi-Fi:
   - Modify `boot.py` with network credentials.
   - Update the IP address in `Scanner/boot.py` and `Screen/boot.py`. (Temporary)
4. Deploy the server:
   ```sh
   flask --app __init__ run --host=0.0.0.0
   ```

## Usage
1. **Adding Items**: Scan new RFID tags and confirm item details.
2. **Item Removal**: The system detects when an item is taken from a shelf.
3. **Exit Confirmation**: Users confirm item movements at the exit terminal.
4. **Inventory Monitoring**: Administrators can track changes and receive alerts.

## Troubleshooting
- **No Connection to Server**: Ensure the Wi-Fi credentials are correctly configured in `boot.py`.
- **RFID Not Scanning**: Check wiring and ensure RFID tags are functional.
- **LCD Not Displaying Data**: Restart the ESP32 and verify connections.

## Future Improvements
- Integration with a cloud database for remote access.
- Mobile application support for inventory management.
- Enhanced security features for access control.
