# API Reference

Base URL: `http://localhost:5000` (local) or your deployed service URL.

## `GET /`

Serves the frontend UI (single-URL app).

## `GET /health`

Health check.

**Response `200`:**
```json
{ "message": "Marketing Copy AI Backend Running" }
```

## `POST /generate-email`

Generates a personalized marketing email.

### Request body (all required)

| Field               | Constraints                                            |
|---------------------|--------------------------------------------------------|
| `customer_name`     | Max 80 characters                                      |
| `age`               | 18 - 100                                               |
| `gender`            | `Male`, `Female`, `Other`                              |
| `location`          | Max 120 characters                                     |
| `purchase_history`  | Max 2000 characters (newline-separated)                |
| `favorite_category` | `Fashion`, `Electronics`, `Books`, `Sports`, `Home Decor`, `Beauty` |
| `total_spending`    | Greater than 0                                         |
| `tone`              | One of the 16 supported tones                          |

### Example request

```json
{
  "customer_name": "Priya",
  "age": 32,
  "gender": "Female",
  "location": "Bangalore",
  "purchase_history": "Designer Dress\nHeels",
  "favorite_category": "Fashion",
  "total_spending": 70000,
  "tone": "Luxury"
}
```

### Example response `200`

```json
{
  "success": true,
  "subject": "An Exclusive Luxury Collection Awaits You, Priya",
  "email": "Dear Priya,\n\nAt ShopEasy, we believe you deserve nothing less than the extraordinary..."
}
```

### Errors

| Status | Meaning                                        |
|--------|------------------------------------------------|
| `400`  | Invalid field(s) or AI output could not be parsed |
| `413`  | Request body too large                         |
| `415`  | Wrong Content-Type (must be `application/json`) |
| `500`  | AI / server error                              |

