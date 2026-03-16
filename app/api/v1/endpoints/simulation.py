from fastapi import APIRouter
from app.services.brownian import (simulate_brownian_motion, simulate_correlated_brownian_motion)
from app.services.gbm import simulate_gbm_paths, simulate_gbm_antihetic, simulate_gbm_euler 
from app.services.heston import simulate_heston_paths


router = APIRouter(prefix="simulation", tags=["simulation"])


@router.post("/monte_carlo")
def simulate_monte_carlo(): #pass correct params
    #call correct function
    #make sure to return summary (to many paths)
    pass


@router.post("/brownian")
def simulate_brownian():
    pass


@router.post("/correlated_brownian")
def simulate_corr_brownian():
    pass


@router.post("/gmb_price")
def simulate_gbm_price_paths():
    pass


@router.post("/antihetic_gbm_price")
def simulate_atihetic_gmb_price_paths():
    pass


@router.post("/gmb_euler_price")
def simulate_euler_gbm_price_paths():
    pass

@router.post("/gbm")
def simulate_gmb():
    pass


@router.post("/heston")
def simulate_heston():
    pass