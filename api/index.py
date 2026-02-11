from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from orthos.micromechanics import RuleOfMixtures, HalpinTsai
from orthos.plate import RectangularPlate, solve_buckling
from orthos.holes import predict_strength_psc, AnisotropicHole

app = FastAPI()

class MicromechanicsInput(BaseModel):
    Ef: float
    Em: float
    vf: float
    xi: float = 2.0

class PlateInput(BaseModel):
    length: float
    width: float
    layup: list[float]
    sym: bool = True
    load: float

class BucklingInput(BaseModel):
    D11: float
    D12: float
    D22: float
    D66: float
    a: float
    b: float
    m: int = 1
    n: int = 1

class HoleInput(BaseModel):
    unnotched_strength: float
    radius: float
    d0: float

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/micromechanics")
def calculate_properties(data: MicromechanicsInput):
    E1 = RuleOfMixtures.calculate_E1(data.Ef, data.Em, data.vf)
    E2 = HalpinTsai.calculate_E2(data.Ef, data.Em, data.vf, data.xi)
    return {"E1": E1, "E2": E2}

@app.post("/api/plate/bending")
def solve_plate_bending(data: PlateInput):
    # Use default Carbon/Epoxy properties as defined in RectangularPlate
    plate = RectangularPlate(data.length, data.width, data.layup, sym=data.sym)
    w = plate.solve_bending(data.load)
    # Return max deflection and center deflection
    return {
        "max_deflection": float(np.max(w)),
        "center_deflection": float(w[w.shape[0]//2, w.shape[1]//2])
    }

@app.post("/api/plate/buckling")
def solve_plate_buckling(data: BucklingInput):
    N_cr = solve_buckling(data.D11, data.D12, data.D22, data.D66, data.a, data.b, data.m, data.n)
    return {"N_cr": N_cr}

@app.post("/api/hole/psc")
def predict_failure(data: HoleInput):
    strength = predict_strength_psc(data.unnotched_strength, data.radius, data.d0)
    return {"predicted_strength": strength}
