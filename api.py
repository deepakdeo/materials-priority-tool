"""REST API for Materials Priority Tool.

A lightweight FastAPI server that exposes material rankings as JSON endpoints.

Usage:
    # Install FastAPI dependencies
    pip install fastapi uvicorn

    # Run the API server
    uvicorn api:app --reload --port 8000

    # Or run with Python
    python api.py

Endpoints:
    GET /                   - API info and available endpoints
    GET /rankings           - All materials with scores and ranks
    GET /rankings/{material} - Single material details
    GET /rankings/top/{n}   - Top N materials
    GET /health             - Health check
"""

import json
from pathlib import Path
from typing import Optional

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    import uvicorn
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    print("FastAPI not installed. Run: pip install fastapi uvicorn")

import pandas as pd

# Data path
DATA_PATH = Path(__file__).parent / "data" / "processed" / "materials_master.csv"


def load_data() -> pd.DataFrame:
    """Load materials data."""
    if DATA_PATH.exists():
        return pd.read_csv(DATA_PATH)
    raise FileNotFoundError(f"Data file not found: {DATA_PATH}")


if FASTAPI_AVAILABLE:
    # Create FastAPI app
    app = FastAPI(
        title="Materials Priority Tool API",
        description="REST API for accessing critical materials rankings and scores",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Enable CORS for cross-origin requests
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    async def root():
        """API root - returns available endpoints."""
        return {
            "name": "Materials Priority Tool API",
            "version": "1.0.0",
            "endpoints": {
                "/rankings": "Get all materials with scores and ranks",
                "/rankings/{material}": "Get single material details",
                "/rankings/top/{n}": "Get top N materials",
                "/health": "Health check",
                "/docs": "Interactive API documentation (Swagger)",
                "/redoc": "API documentation (ReDoc)",
            }
        }

    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        try:
            df = load_data()
            return {
                "status": "healthy",
                "materials_count": len(df),
                "data_available": True,
            }
        except Exception as e:
            return JSONResponse(
                status_code=503,
                content={"status": "unhealthy", "error": str(e)}
            )

    @app.get("/rankings")
    async def get_all_rankings(
        sort_by: str = "rank",
        ascending: bool = True,
        fields: Optional[str] = None,
    ):
        """Get all materials with rankings.

        Args:
            sort_by: Field to sort by (default: rank)
            ascending: Sort ascending (default: True)
            fields: Comma-separated list of fields to include (default: all)
        """
        try:
            df = load_data()

            # Sort
            if sort_by in df.columns:
                df = df.sort_values(sort_by, ascending=ascending)

            # Filter fields
            if fields:
                field_list = [f.strip() for f in fields.split(",")]
                valid_fields = [f for f in field_list if f in df.columns]
                if valid_fields:
                    df = df[valid_fields]

            return {
                "count": len(df),
                "materials": df.to_dict(orient="records"),
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/rankings/top/{n}")
    async def get_top_rankings(n: int = 5):
        """Get top N ranked materials.

        Args:
            n: Number of top materials to return (default: 5)
        """
        try:
            df = load_data()
            df = df.sort_values("rank").head(n)

            return {
                "count": len(df),
                "materials": df.to_dict(orient="records"),
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/rankings/{material}")
    async def get_material(material: str):
        """Get details for a specific material.

        Args:
            material: Material name (case-insensitive)
        """
        try:
            df = load_data()

            # Case-insensitive match
            match = df[df["material"].str.lower() == material.lower()]

            if match.empty:
                available = df["material"].tolist()
                raise HTTPException(
                    status_code=404,
                    detail=f"Material '{material}' not found. Available: {available}"
                )

            record = match.iloc[0].to_dict()

            # Add score breakdown
            record["score_breakdown"] = {
                "supply_risk": {
                    "score": record.get("supply_risk_score"),
                    "weight": "25%",
                    "weighted": record.get("supply_risk_score", 0) * 0.25,
                },
                "market_opportunity": {
                    "score": record.get("market_opportunity_score"),
                    "weight": "20%",
                    "weighted": record.get("market_opportunity_score", 0) * 0.20,
                },
                "kc_advantage": {
                    "score": record.get("kc_advantage_score"),
                    "weight": "15%",
                    "weighted": record.get("kc_advantage_score", 0) * 0.15,
                },
                "production_feasibility": {
                    "score": record.get("production_feasibility_score"),
                    "weight": "20%",
                    "weighted": record.get("production_feasibility_score", 0) * 0.20,
                },
                "strategic_alignment": {
                    "score": record.get("strategic_alignment_score"),
                    "weight": "20%",
                    "weighted": record.get("strategic_alignment_score", 0) * 0.20,
                },
            }

            return record
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/compare")
    async def compare_materials(materials: str):
        """Compare multiple materials side by side.

        Args:
            materials: Comma-separated list of material names
        """
        try:
            df = load_data()
            material_list = [m.strip() for m in materials.split(",")]

            results = []
            for mat in material_list:
                match = df[df["material"].str.lower() == mat.lower()]
                if not match.empty:
                    results.append(match.iloc[0].to_dict())

            if not results:
                raise HTTPException(
                    status_code=404,
                    detail=f"No matching materials found for: {material_list}"
                )

            return {
                "count": len(results),
                "comparison": results,
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    if FASTAPI_AVAILABLE:
        print("Starting Materials Priority Tool API...")
        print("API docs available at: http://localhost:8000/docs")
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        print("FastAPI not available. Install with: pip install fastapi uvicorn")
