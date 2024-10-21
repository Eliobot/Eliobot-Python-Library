### Eliobot Library - Release Notes
**Version 3.0 - 2023**  
**ELIO SAS**

We are pleased to announce the release of version 3.0 of the Eliobot Library. This update focuses on improving the structure of the library and integrating new functionality to enhance the user experience.

**Project Home:**  
[Eliobot.com](https://eliobot.com)

#### **Key Changes:**
1. **IR Remote Control Integration:**
    - **New IR Remote Support:** Eliobot now supports infrared (IR) remote control functionality. You can control your Eliobot using a IR remote, making it easier to manage the robot remotely.
    - **Signal Decoding:** The library includes methods to decode IR signals, allowing you to map remote buttons to specific actions on the robot.

2. **Refactoring of the Eliobot Class:**
    - **Class Separation:** The previously monolithic `Eliobot` class has been refactored into smaller, more manageable subclasses. This change enhances code readability, maintenance, and allows for more modular usage of the library.
    - **Dedicated Subclasses:** Functions related to motors, sensors, and connectivity have been moved into their respective classes (`Motors`, `Buzzer`, `ObstacleSensor`, `LineSensor`, `WiFiConnectivity`, and `IRRemote`). This separation makes it easier to work on specific functionalities without dealing with the entire library at once.

#### **Why This Matters:**
- **Better Code Organization:** By separating the `Eliobot` class into smaller components, developers can focus on individual modules, reducing complexity and making it easier to understand and modify the code.
- **IR Remote Control:** Adding IR remote functionality provides a convenient way to control Eliobot remotely, making it more versatile in different scenarios.

#### **Installation:**
As usual, you can update your Eliobot library through the Eliobloc app. The app will check if you have the latest version and prompt you to update if needed.

#### **Support:**
For further assistance, feedback, or questions, please visit our website or reach out to our support team.

Enjoy the improved structure and new remote control capabilities in version 3.0 of the Eliobot Library!