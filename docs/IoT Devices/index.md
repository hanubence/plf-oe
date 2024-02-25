## The IoT Devices

### Goals
Implementation of the IoT devices that drive data collection in remote locations, for long periods of time

### The Moometer ESP32

- This device serves the purpose of collecting data about the animal it's attached to

- Ideally we have as many of these devices as possible to scale up our data collection, while keeping in mind cost limitations

<div class="grid cards" markdown>

-   :fontawesome-solid-gear:{ .lg .middle } __Components__

    ---

    Sensors, microcontrollers, power source, communication modules

    [:octicons-arrow-right-24: Components](components.md)

-   :fontawesome-solid-database:{ .lg .middle } __Data Collection__

    ---

    Protocols, types of data, frequency, edge processing considerations

    [:octicons-arrow-right-24: Data Collection](#)

-   :fontawesome-solid-car-battery:{ .lg .middle } __Power Management__

    ---

    Strategies for optimizing power in remote locations

    [:octicons-arrow-right-24: Power Management](#)

-   :fontawesome-solid-box:{ .lg .middle } __Enclosure and Deployment__

    ---

    Protection against environment, placement in the field etc.

    [:octicons-arrow-right-24: Enclosure](enclosure.md)

</div>

### The Big Moo

- This device serves the purpose of collecting and aggregating data from the Moometers, then sending the data home.

- The Big Moo connects to the Moometers when they are in range to do data transfers, making short range data transfers. It also has a connection to the outside world, allowing it to send home the collected data.

- This device will ideally have more processing power than the Moometers

<div class="grid cards" markdown>

-   :material-signal-3g:{ .lg .middle } __Communication Technologies__

    ---

    LoRaWAN, Cellular, etc.

    [:octicons-arrow-right-24: Communication](components.md)

-   :fontawesome-solid-wifi:{ .lg .middle } __Connectivity__

    ---

    Connectivity challenges and solutions to potential signal issues in remote locations

    [:octicons-arrow-right-24: Connectivity](components.md)

-   :fontawesome-solid-database:{ .lg .middle } __Data Storage__

    ---

    Type of database, scalability for future growth

    [:octicons-arrow-right-24: Storage](components.md)

-   :fontawesome-solid-lock:{ .lg .middle } __Data Security__

    ---

    Measures to protect sensitive livestock data

    [:octicons-arrow-right-24: Security](components.md)

</div>