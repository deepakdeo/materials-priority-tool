# API Guide

The Materials Priority Tool includes an optional REST API for programmatic access to rankings data.

## Setup

The API requires FastAPI and Uvicorn (not included in base requirements):

```bash
pip install fastapi uvicorn
```

## Running the API

```bash
# Using uvicorn directly
uvicorn api:app --reload --port 8000

# Or using Python
python api.py
```

The API will be available at `http://localhost:8000`

## Endpoints

### Root
```
GET /
```
Returns API info and available endpoints.

### Health Check
```
GET /health
```
Returns API health status and data availability.

### All Rankings
```
GET /rankings
GET /rankings?sort_by=composite_score&ascending=false
GET /rankings?fields=material,rank,composite_score
```

Parameters:
- `sort_by` - Field to sort by (default: rank)
- `ascending` - Sort direction (default: true)
- `fields` - Comma-separated fields to include

### Top N Rankings
```
GET /rankings/top/3
GET /rankings/top/5
```

Returns the top N ranked materials.

### Single Material
```
GET /rankings/lithium
GET /rankings/Graphite
```

Returns detailed information for a specific material (case-insensitive).

### Compare Materials
```
GET /compare?materials=lithium,graphite,cobalt
```

Returns side-by-side comparison of multiple materials.

## Example Responses

### GET /rankings/top/3
```json
{
  "count": 3,
  "materials": [
    {
      "material": "Lithium",
      "rank": 1,
      "composite_score": 6.82,
      "supply_risk_score": 4.7,
      "market_opportunity_score": 8.6,
      "criticality_category": "Near-Critical"
    },
    {
      "material": "Graphite",
      "rank": 2,
      "composite_score": 6.76,
      ...
    },
    ...
  ]
}
```

### GET /rankings/lithium
```json
{
  "material": "Lithium",
  "rank": 1,
  "composite_score": 6.82,
  "import_reliance_pct": 25,
  "top_producer": "Australia",
  "criticality_category": "Near-Critical",
  "score_breakdown": {
    "supply_risk": {
      "score": 4.7,
      "weight": "25%",
      "weighted": 1.175
    },
    "market_opportunity": {
      "score": 8.6,
      "weight": "20%",
      "weighted": 1.72
    },
    ...
  }
}
```

## Interactive Documentation

When the API is running, interactive docs are available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## CORS

The API allows cross-origin requests from any domain, making it suitable for frontend integrations.

## Integration Examples

### Python
```python
import requests

response = requests.get("http://localhost:8000/rankings/top/5")
data = response.json()

for material in data["materials"]:
    print(f"{material['rank']}. {material['material']}: {material['composite_score']}")
```

### JavaScript
```javascript
fetch("http://localhost:8000/rankings/top/5")
  .then(response => response.json())
  .then(data => {
    data.materials.forEach(m => {
      console.log(`${m.rank}. ${m.material}: ${m.composite_score}`);
    });
  });
```

### cURL
```bash
curl http://localhost:8000/rankings/top/5 | jq
```

## Deployment

For production deployment, consider:
- Running behind a reverse proxy (nginx)
- Adding rate limiting
- Enabling authentication (API keys)
- Deploying to a cloud platform (Railway, Render, etc.)
