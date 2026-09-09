# 1:10 onroad RC car for speeds over 100 km/h

This project covers the system architecture and configuration of an 1:10 scale on-road touring car with the design goal of a consistently repeatable top speed of over 100 km/h without risking the car to be damaged or destroyed. The focus is on maximizing drive power while ensuring reliability and cost efficiency.

The technical challenge primarily results from the chosen scale and the limited tire diameter of 64 millimeters. While vehicles from 1:8+ scale have strong physical advantages due to higher mass inertia, larger rolling circumferences, and a longer wheelbase, the 1:10 scale requires significantly higher rotor speeds. This leads to high mechanical stresses in the drivetrain. The low vehicle weight also requires precise aerodynamic and suspension tuning to ensure driving stability at high speeds.

The artefacts of this repository are:
* Architecture decision records (ADRs) in the `/architecture` directory
* System specification in the `specs/full_spec.yml` file
* Vehicle setup configurations in the `/setup_sheets` directory

<img src="https://raw.githubusercontent.com/kleinnconrad/small-scale-rc-speedrun/main/photos/PXL_20260903_135619761.jpg" alt="RC Car Photo 1" width="49%"> <img src="https://raw.githubusercontent.com/kleinnconrad/small-scale-rc-speedrun/main/photos/PXL_20260903_135638335.jpg" alt="RC Car Photo 2" width="49%">

## Table of contents
* [Repository structure](#repository-structure)
* [Artefacts (ADR, specs, setup sheets)](#artefacts-adr-specs-setup-sheets)
* [Calculation models for drivetrain design](#calculation-models-for-drivetrain-design)
* [Learnings & modifications](#learnings--modifications)
* [Repository automation](#repository-automation)
* [Follow-up project: Telemetry system](#follow-up-project-telemetry-system)
* [Licensing](#licensing)

## Repository structure
* **`/architecture`**: Documentation of basic system designs
* **`/docs`**: Static web dashboard for visualizing the latest setup configurations
* **`/photos`**: Central directory for all image files
* **`/project`**: General project information
  * **`/costs`**: Cost tracking
  * **`/follow_up_projects`**: Documentation of related follow-up projects
* **`/scripts`**: Automation scripts
  * **`/calc`**: Calculation scripts
  * **`/plots`**: Generated plots
* **`/setup_sheets`**: Vehicle setup configurations
* **`/specs`**: Specifications of the vehicle components
  * **`/electronics`**: Selection and specification of electronic components such as motors, electronic speed controllers, and batteries
  * **`/mechanics`**: Chassis design, construction data, and specification of physical components
* **`/testing`**: Test results and performance measurement data
  * **`/error_list`**: Error logs and their resolutions
  * **`/tests`**: Logs and data of test drives

## Artefacts (ADR, specs, setup sheets)
The documentation of architecture decisions (ADRs), the specifications of all mechanical and electronic components, and the vehicle setup configurations are consistently maintained as structured YAML files (`.yml` or `.yaml`). The formal hierarchical structure of these artefacts is standardized as follows:

```mermaid
classDiagram
    class adr {
        +id: String
        +title: String
        +status: String
        +date: Date
        +context: Text
        +decision: String
        +rationale: Text
        +consequences: List
    }
    class adr_alternative {
        +option_id: Integer
        +name: String
        +type: String
        +evaluation: Text
    }
    adr *-- adr_alternative : considered_alternatives
    
    class spec {
        +properties: Object
        +integration_notes: Object
    }
    class spec_meta {
        +brand: String
        +model: String
        +type: String
    }
    spec *-- spec_meta : meta

    class setup {
    }
    class setup_meta {
        +date: Date
        +description: String
        +version: String
        +top_speed_kmh: Float
    }
    class setup_properties {
        +suspension_and_geometry: Object
        +drivetrain: Object
        +electronics_and_control: Object
    }
    setup *-- setup_meta : meta
    setup *-- setup_properties : properties
```

## Calculation models for drivetrain design
To avoid thermal or mechanical overload of the electronic components, custom-developed calculation models are used:
* **Gearing calculator (`scripts/calc/getriebe_calc.py`)**: Simulates the mechanical wheel load for the motor based on tire diameter and target speed, depending on available motor pinions. Setups are categorized into load zones for the defined drive system.
* **Limit calculator (`scripts/calc/max_speed.py`)**: Calculates the achievable top speed considering specific motor data, battery voltage, and defined thermal tolerance limits based on physical hardware specifications.

## Learnings & modifications (so far...)
This section documents the findings from previous tests & speedruns in 1:10 scale as well as the resulting modifications to the vehicle.

| Driving operation & environment |
|:---|
| **[L] Track selection**<br>A suitable track is crucial for success. Clean asphalt is absolutely necessary. The track should preferably not be bordered by walls or curbs. A minimum width of 8 meters is required. |
| **[L] Weather**<br>The weather is also important. Ensure there is no wind and conditions are dry. |
| **[L] Safety**<br>If the conditions are not right and you don't have a good feeling, no speedrun should be undertaken. |
| **[L] Driving practice**<br>You must learn to drive. It is necessary to familiarize yourself with the vehicle and the acceleration curve. It is important to steer the vehicle smoothly when it is far away. |

| Suspension & geometry |
|:---|
| **[M] Dampers & springs**<br>Very viscous shock oil was used and spring preload maximized. Stiff suspension is absolutely necessary to prevent loss of control due to diving. |
| **[M] Suspension geometry**<br>Rear toe-in of 2.5 degrees and 0 degrees camber. Front 0 degrees toe-in and 0 degrees camber. No experiments should be made here. |
| **[M] Sway bars**<br>The sway bars were removed. They are unnecessary for speedruns and pose a potential source of error. |
| **[M] Droop screws**<br>The droop screws were removed. Since the track is not manually cleaned, further lowering is not constructive. The screws are unnecessary for the regular 1:10 speedrun. |
| **[L] Weight distribution**<br>Care must be taken to ensure an even left/right weight distribution. Furthermore, the front must not be too light. |

| Drivetrain |
|:---|
| **[L] Motorization**<br>Sufficient motorization is less of a problem than often assumed. You shouldn't invest too much here. |
| **[M] Motor & gearing**<br>Use of a 3660 motor with a tall gear ratio instead of the usual 3650 motor. The motorization must be adapted to the available track. |
| **[M] Differential (front)**<br>A front spool was installed. During straight-line running at maximum speed, diff-out must be absolutely avoided; speed compensation is not desired. |
| **[L] Differential (rear)**<br>Making the rear differential stiffer is not necessary. The front spool is sufficient. |
| **[L] Thermal management**<br>Problems with ESC and motor temperature have not occurred yet. The problem is apparently overrated. |

| Electronics & control |
|:---|
| **[L] Control components**<br>**Do not skimp on the remote control and servo**. Lack of precision makes steering corrections a game of chance. You must invest in a remote control with hall sensors and a decent digital servo. |
| **[L] Assistance systems**<br>**Using a Gyro really makes a difference** and is highly recommended. |
| **[L] Steering mechanics**<br>The steering mechanism must move without resistance when disconnected from the servo. Mechanical resistance prevents the servo from returning precisely to the neutral position during slow steering inputs. In this state, the servo stops visibly but continues to draw current, indicated by audible noise, as it attempts to reach the neutral position. |
| **[L] `Steering Exponential Curve` (cubic polynomial)**<br>The steering exponential curve requires precise configuration. A setting of approximately -30 is recommended. |
| **[L] `Throttle Exponential Curve` (cubic polynomial)**<br>The throttle exponential curve requires precise configuration. A setting of approximately -40 is recommended. |

| Chassis & assembly |
|:---|
| **[L] Material selection**<br>Not all plastic parts should be replaced with aluminum. You must consider which parts are allowed to be destroyed in a crash. If easily replaceable plastic parts are replaced with aluminum, the impact energy finds more unfavorable paths. |
| **[L] Threadlocker**<br>Loctite on metal connections is absolutely mandatory. |
| **[L] Body**<br>The body should not be painted. A clear body allows a necessary view of the technology at all times. |
| **[L] Aerodynamics**<br>A wedge shape of the vehicle is necessary for efficient aerodynamics. To achieve this, the front body posts must be shortened as much as possible. |
| **[M] C-hub assembly**<br>The mounting screws of the C-hubs were loosened to eliminate mechanical resistance. Excessive tightening prevents the steering from moving freely, resulting in the previously described issue of an inaccurate servo neutral return. |
| **[M] Servo saver**<br>The servo saver was removed and an aluminum servo horn was mounted directly. This increases the risk of damage to the servo in the event of a crash. The servo saver was identified as a source of failure (steering oscillation) during speedruns. |

*(Legend: **[L]** = learning, **[M]** = modification)*

## Repository automation
Maintaining the specifications and architecture decisions formatted as YAML files triggers automated processes:
* **Aggregation of specifications**: Individual hardware specifications are merged into a central specification file in the root directory.
* **Cost overview**: Bill of materials and shopping lists are automatically derived from the specifications and updated.
* **Decision log**: Architecture decisions are automatically compiled into a chronological log.

## Follow-up project: Telemetry system
This project is followed by an independent project concerned with the development of a telemetry data system based on an ESP32 microcontroller. The goal is the sensory recording and transmission of driving dynamics parameters of the RC vehicle.

[![GitHub repo](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/kleinnconrad/carten_telemetrie)

## Licensing
* The source code of the calculation models is subject to the MIT license.
* The hardware design, documentation, specifications, and test results are released under the Creative Commons attribution 4.0 international license. Own adaptations and commercial use are permitted, provided authorship is acknowledged.
