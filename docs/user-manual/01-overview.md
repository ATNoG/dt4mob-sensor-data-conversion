# Sensor Data Conversion - User Manual

## Overview

Sensor Data Conversion is a bridge service that converts vehicle detection data with the OutSight format into the ORT Tracking format. It consumes OutSight-formatted messages containing bounding box detections with local coordinates, transforms them into ORT Tracking messages with properly computed dimensions, geographic coordinates, and local positions, and publishes the converted output to an MQTT broker.

**Problem it solves:** OutSight sensors and ORT Tracking systems use different data formats and coordinate reference systems. OutSight provides raw bounding box corners in a local coordinate system, while ORT Tracking expects dimensions (length, width, height), local coordinates relative to a reference camera, and absolute geographic coordinates (latitude/longitude). This service handles the coordinate transformations and field derivations automatically, enabling seamless integration between the two systems.

**Primary use case:** Runs as a long-lived service in a toll gantry or road monitoring deployment, continuously converting real-time and historical vehicle detection messages from producers using the OutSight format into ORT Tracking format for downstream processing by the gantry-service and digital twin platform.
