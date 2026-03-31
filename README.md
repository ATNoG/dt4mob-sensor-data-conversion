# sensor-data-conversion

This service converts OutSight messages into the A-to-Be object structure.

### Overview

The A-to-Be format requires specific fields for each object, such as:

- **Dimensions** - length, width, height
- **Local coordinates** - of the corner with the smallest coordinate values relative to the ORT tracking camera
- **Absolute coordinates** - geographic position of the same point as local coordinates
- **Speed**
- **Object ID**
- **Measurement timestamp**

Although OutSight messages contain all necessary information, some fields are not directly available and must be derived.

---

## Supported Fields

### Directly Mapped

The following fields are available directly from OutSight messages:

- **Object ID**
- **Measurement timestamp**
- **Speed**

These values are extracted without transformation.

---

## Derived Fields

### Dimensions

OutSight messages include a bounding box defined in local coordinates. While **height** is directly available, **length** and **width** are not explicitly provided.

To derive length and width:

1. Identify the coordinates of the corners of the bounding box.
2. Compute distances between corresponding corner pairs for each side.
3. Average the distances of opposite sides to obtain consistent length and width values.

This approach assumes that bounding box corners follow a consistent ordering, which seems to be the case.

---

### Local and Absolute Coordinates

OutSight and A-to-Be use different reference systems, although both share the same scale.

To compute coordinates:

1. **Convert OutSight coordinates to ENU (East-North-Up)** using the origin defined by the A-to-Be reference system.
2. **Transform ENU coordinates to A-to-Be local coordinates** via matrix multiplication.
3. Use the intermediate ENU position to compute **absolute geographic coordinates** (latitude/longitude) before generating the final local coordinates.

In practice, this process involves two matrix multiplications. While one could combine these into a single transformation, the intermediate ENU values are reused to calculate absolute coordinates efficiently.

---

## Summary

| Field                | Source                       |
| -------------------- | ---------------------------- |
| Object ID            | Direct from OutSight         |
| Timestamp            | Direct from OutSight         |
| Speed                | Direct from OutSight         |
| Height               | From OutSight message        |
| Length & Width       | Computed from bounding box   |
| Local coordinates    | Converted via ENU to A-to-Be |
| Absolute coordinates | Derived from ENU             |

---

> Notes:
>
> - The conversion assumes consistent bounding box corner ordering.
> - Geographic coordinate conversion leverages the ENU intermediate for accuracy and simplicity. There is some distortion associated with this, but at the small scales we are working with it is negligible.
